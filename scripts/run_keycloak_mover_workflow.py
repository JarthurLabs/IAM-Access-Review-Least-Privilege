#!/usr/bin/env python3
"""Execute and verify a least-privilege mover workflow in a live Keycloak realm."""

from __future__ import annotations

import argparse
import json
import time
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path


def request(method, url, *, token=None, json_body=None, form_body=None, expected=(200, 201, 204)):
    headers = {"Accept": "application/json"}
    body = None
    if token:
        headers["Authorization"] = f"Bearer {token}"
    if json_body is not None:
        body = json.dumps(json_body).encode("utf-8")
        headers["Content-Type"] = "application/json"
    elif form_body is not None:
        body = urllib.parse.urlencode(form_body).encode("utf-8")
        headers["Content-Type"] = "application/x-www-form-urlencoded"
    req = urllib.request.Request(url, data=body, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req, timeout=30) as response:
            raw = response.read().decode("utf-8")
            if response.status not in expected:
                raise RuntimeError(f"Unexpected HTTP {response.status} for {method} {url}")
            parsed = json.loads(raw) if raw else None
            return parsed, dict(response.headers)
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"HTTP {exc.code} for {method} {url}: {detail}") from exc


def admin_token(base_url, username, password):
    payload, _ = request(
        "POST",
        f"{base_url}/realms/master/protocol/openid-connect/token",
        form_body={
            "client_id": "admin-cli",
            "username": username,
            "password": password,
            "grant_type": "password",
        },
        expected=(200,),
    )
    return payload["access_token"]


def get_user(base_url, token, realm, username):
    query = urllib.parse.urlencode({"username": username, "exact": "true"})
    users, _ = request("GET", f"{base_url}/admin/realms/{realm}/users?{query}", token=token, expected=(200,))
    if len(users) != 1:
        raise RuntimeError(f"Expected one user named {username}; got {len(users)}")
    user, _ = request(
        "GET",
        f"{base_url}/admin/realms/{realm}/users/{users[0]['id']}",
        token=token,
        expected=(200,),
    )
    return user


def enable_admin_managed_attributes(base_url, token, realm):
    """Allow realm administrators to manage lab-only custom attributes.

    Keycloak disables unmanaged user attributes by default.  The mover lab uses
    department and title as administrator-controlled directory attributes, so
    ADMIN_EDIT is the narrow policy that permits those writes without exposing
    unmanaged attributes to end-user profile contexts.
    """
    profile, _ = request(
        "GET",
        f"{base_url}/admin/realms/{realm}/users/profile",
        token=token,
        expected=(200,),
    )
    profile["unmanagedAttributePolicy"] = "ADMIN_EDIT"
    request(
        "PUT",
        f"{base_url}/admin/realms/{realm}/users/profile",
        token=token,
        json_body=profile,
        expected=(200,),
    )


def get_group(base_url, token, realm, name):
    groups, _ = request("GET", f"{base_url}/admin/realms/{realm}/groups", token=token, expected=(200,))
    matches = [group for group in groups if group.get("name") == name]
    if len(matches) != 1:
        raise RuntimeError(f"Expected one group named {name}; got {len(matches)}")
    return matches[0]


def get_memberships(base_url, token, realm, user_id):
    groups, _ = request(
        "GET",
        f"{base_url}/admin/realms/{realm}/users/{user_id}/groups",
        token=token,
        expected=(200,),
    )
    return sorted(group["name"] for group in groups)


def sanitize_resource_path(path, replacements):
    result = path or ""
    for raw, label in replacements.items():
        result = result.replace(raw, label)
    return result


def write_change_record(evidence, path):
    before = evidence["before"]
    after = evidence["after"]
    lines = [
        "# Keycloak Mover Workflow Change Record",
        "",
        f"- Workflow status: **{evidence['validation']['status']}**",
        f"- Executed UTC: **{evidence['executed_utc']}**",
        f"- Platform: **{evidence['platform']}**",
        f"- Realm: **{evidence['realm']}**",
        f"- Subject: **{evidence['subject']}**",
        "",
        "## Approved change",
        "",
        "Move the lab user from Sales to Security Operations, remove obsolete CRM editor access, "
        "and grant the role-aligned SIEM reader group.",
        "",
        "## Before",
        "",
        f"- Department: `{before['department']}`",
        f"- Title: `{before['title']}`",
        f"- Groups: `{', '.join(before['groups'])}`",
        "",
        "## After",
        "",
        f"- Department: `{after['department']}`",
        f"- Title: `{after['title']}`",
        f"- Groups: `{', '.join(after['groups'])}`",
        "",
        "## Validation",
        "",
        "- Obsolete `APP-CRM-Editors` membership removed.",
        "- Role-aligned `SEC-SIEM-Readers` membership added.",
        "- User attributes updated to Security Operations / SOC Analyst.",
        f"- Keycloak admin events captured: **{evidence['admin_event_count']}**.",
        "",
        "## Control limitations",
        "",
        "This is an ephemeral lab realm containing only controlled test identities. The same operator acts as "
        "requester, approver, and executor, so separation of duties is documented but not demonstrated. "
        "The workflow proves live IAM administration and auditability, not production tenant experience.",
    ]
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--base-url", default="http://localhost:8080")
    parser.add_argument("--admin-user", required=True)
    parser.add_argument("--admin-password", required=True)
    parser.add_argument("--output-dir", type=Path, default=Path("live-tenant/evidence"))
    args = parser.parse_args()
    base_url = args.base_url.rstrip("/")
    realm = "iam-lab"
    username = "lab.mover01"
    old_group_name = "APP-CRM-Editors"
    new_group_name = "SEC-SIEM-Readers"
    token = admin_token(base_url, args.admin_user, args.admin_password)

    request(
        "POST",
        f"{base_url}/admin/realms",
        token=token,
        json_body={
            "realm": realm,
            "enabled": True,
            "eventsEnabled": True,
            "adminEventsEnabled": True,
            "adminEventsDetailsEnabled": True,
        },
        expected=(201,),
    )
    enable_admin_managed_attributes(base_url, token, realm)
    for group_name in (old_group_name, new_group_name):
        request(
            "POST",
            f"{base_url}/admin/realms/{realm}/groups",
            token=token,
            json_body={"name": group_name},
            expected=(201,),
        )
    request(
        "POST",
        f"{base_url}/admin/realms/{realm}/users",
        token=token,
        json_body={
            "username": username,
            "enabled": True,
            "firstName": "Lab",
            "lastName": "Mover",
            "attributes": {"department": ["Sales"], "title": ["Account Executive"]},
        },
        expected=(201,),
    )
    user = get_user(base_url, token, realm, username)
    user_id = user["id"]
    old_group = get_group(base_url, token, realm, old_group_name)
    new_group = get_group(base_url, token, realm, new_group_name)
    request(
        "PUT",
        f"{base_url}/admin/realms/{realm}/users/{user_id}/groups/{old_group['id']}",
        token=token,
        expected=(204,),
    )
    before_user = get_user(base_url, token, realm, username)
    before_groups = get_memberships(base_url, token, realm, user_id)

    updated_user = dict(before_user)
    updated_user["attributes"] = {"department": ["Security Operations"], "title": ["SOC Analyst"]}
    request(
        "PUT",
        f"{base_url}/admin/realms/{realm}/users/{user_id}",
        token=token,
        json_body=updated_user,
        expected=(204,),
    )
    request(
        "DELETE",
        f"{base_url}/admin/realms/{realm}/users/{user_id}/groups/{old_group['id']}",
        token=token,
        expected=(204,),
    )
    request(
        "PUT",
        f"{base_url}/admin/realms/{realm}/users/{user_id}/groups/{new_group['id']}",
        token=token,
        expected=(204,),
    )
    after_user = get_user(base_url, token, realm, username)
    after_groups = get_memberships(base_url, token, realm, user_id)

    before_department = before_user.get("attributes", {}).get("department", [""])[0]
    before_title = before_user.get("attributes", {}).get("title", [""])[0]
    after_department = after_user.get("attributes", {}).get("department", [""])[0]
    after_title = after_user.get("attributes", {}).get("title", [""])[0]
    checks = {
        "before_department_sales": before_department == "Sales",
        "before_title_account_executive": before_title == "Account Executive",
        "before_old_group_present": old_group_name in before_groups,
        "before_new_group_absent": new_group_name not in before_groups,
        "after_old_group_absent": old_group_name not in after_groups,
        "after_new_group_present": new_group_name in after_groups,
        "department_updated": after_department == "Security Operations",
        "title_updated": after_title == "SOC Analyst",
    }
    if not all(checks.values()):
        raise RuntimeError(f"Mover validation failed: {checks}")

    # Allow Keycloak to finish writing admin events before retrieval.
    time.sleep(1)
    events, _ = request(
        "GET",
        f"{base_url}/admin/realms/{realm}/admin-events?max=100",
        token=token,
        expected=(200,),
    )
    replacements = {
        user_id: "<LAB_USER_ID>",
        old_group["id"]: "<OLD_GROUP_ID>",
        new_group["id"]: "<NEW_GROUP_ID>",
    }
    public_events = [
        {
            "operation_type": event.get("operationType", ""),
            "resource_type": event.get("resourceType", ""),
            "resource_path": sanitize_resource_path(event.get("resourcePath", ""), replacements),
        }
        for event in events
    ]
    evidence = {
        "workflow": "live_keycloak_mover_least_privilege",
        "executed_utc": datetime.now(timezone.utc).isoformat(),
        "platform": "Keycloak 26.0.7 (ephemeral GitHub Actions container)",
        "realm": realm,
        "subject": username,
        "custom_attribute_policy": "ADMIN_EDIT (administrator context only)",
        "before": {"department": before_department, "title": before_title, "groups": before_groups},
        "approved_change": {
            "department": "Security Operations",
            "title": "SOC Analyst",
            "remove_group": old_group_name,
            "add_group": new_group_name,
        },
        "after": {"department": after_department, "title": after_title, "groups": after_groups},
        "validation": {"status": "passed", "checks": checks},
        "admin_event_count": len(public_events),
        "admin_events": public_events,
        "privacy": "All identities and entitlements are controlled lab objects; admin credentials are ephemeral and are not retained.",
    }
    args.output_dir.mkdir(parents=True, exist_ok=True)
    json_path = args.output_dir / "keycloak_mover_evidence.json"
    md_path = args.output_dir / "keycloak_change_record.md"
    json_path.write_text(json.dumps(evidence, indent=2) + "\n", encoding="utf-8")
    write_change_record(evidence, md_path)
    print(json.dumps({"status": "passed", "evidence": str(json_path), "change_record": str(md_path)}, indent=2))


if __name__ == "__main__":
    main()
