# Live Keycloak Mover and Least-Privilege Workflow

## Purpose

This workflow creates a real, temporary Keycloak realm and performs an auditable
identity mover change. It exists for users who do not have access to Microsoft
Entra ID, Okta, or Google Workspace tenants.

## Scenario

A controlled lab user, `lab.mover01`, changes departments from Sales to Security
Operations.

Before the change:

- Department: Sales
- Title: Account Executive
- Group: `APP-CRM-Editors`

Approved target state:

- Department: Security Operations
- Title: SOC Analyst
- Remove: `APP-CRM-Editors`
- Add: `SEC-SIEM-Readers`

## Execution

GitHub Actions starts Keycloak 26.0.7 in an ephemeral container. The Python
workflow uses Keycloak's Admin API to:

1. Create a live realm with admin-event auditing enabled.
2. Create two entitlement groups and one controlled user.
3. Assign the user's original Sales access and capture the before state.
4. Update department and title attributes.
5. Remove obsolete CRM editor membership.
6. Add the role-aligned SIEM reader membership.
7. Verify the after state and retrieve Keycloak admin events.
8. Write a sanitized evidence JSON file and change-closure record.

The workflow fails if any expected before/after control is missing.

## Evidence

Successful runs write:

- `live-tenant/evidence/keycloak_mover_evidence.json`
- `live-tenant/evidence/keycloak_change_record.md`
- A 30-day GitHub Actions artifact containing the same evidence

## Security and privacy

- The realm and identities are created solely for the lab.
- No external people or production data are used.
- The bootstrap administrator password is randomly generated for each run,
  masked from logs, kept only in the runner environment, and destroyed with
  the ephemeral container.
- Raw tokens and credentials are never committed.
- Resource identifiers are replaced with labels in the public evidence.

## Limitations

- Keycloak demonstrates platform-neutral IAM administration, not Microsoft Entra expertise.
- The realm is ephemeral rather than a persistent enterprise tenant.
- One operator acts as requester, approver, and executor, so production separation
  of duties is documented but not demonstrated.
- The project does not claim production IAM administration experience.
