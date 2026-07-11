# Keycloak Mover Workflow Change Record

- Workflow status: **passed**
- Executed UTC: **2026-07-11T15:47:53.862323+00:00**
- Platform: **Keycloak 26.0.7 (ephemeral GitHub Actions container)**
- Realm: **iam-lab**
- Subject: **lab.mover01**

## Approved change

Move the lab user from Sales to Security Operations, remove obsolete CRM editor access, and grant the role-aligned SIEM reader group.

## Before

- Department: `Sales`
- Title: `Account Executive`
- Groups: `APP-CRM-Editors`

## After

- Department: `Security Operations`
- Title: `SOC Analyst`
- Groups: `SEC-SIEM-Readers`

## Validation

- Obsolete `APP-CRM-Editors` membership removed.
- Role-aligned `SEC-SIEM-Readers` membership added.
- User attributes updated to Security Operations / SOC Analyst.
- Keycloak admin events captured: **8**.

## Control limitations

This is an ephemeral lab realm containing only controlled test identities. The same operator acts as requester, approver, and executor, so separation of duties is documented but not demonstrated. The workflow proves live IAM administration and auditability, not production tenant experience.
