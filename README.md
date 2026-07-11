<div align="center">

# IAM Access Review & Least Privilege Remediation

**Live Keycloak mover workflow + access governance analysis + auditable evidence**

![Platform](https://img.shields.io/badge/Platform-Keycloak-blue)
![Workflow](https://img.shields.io/badge/Workflow-Live%20Mover-brightgreen)
![Focus](https://img.shields.io/badge/Focus-Least%20Privilege-purple)
![Automation](https://img.shields.io/badge/Automation-GitHub%20Actions-black)

</div>

## What this project demonstrates

This repository combines two related forms of IAM evidence:

1. A **live, automated Keycloak realm workflow** that creates a controlled user,
   performs a Sales-to-Security Operations mover change, removes obsolete access,
   grants a least-privilege group, verifies the result, and captures admin events.
2. A **synthetic governance analysis** covering access reviews, RBAC, MFA posture,
   privileged access, and joiner-mover-leaver process design.

The live workflow provides real identity-platform administration evidence without
requiring access to an employer tenant or involving external users.

## Live mover result

The controlled user `lab.mover01` begins with:

- Department: Sales
- Title: Account Executive
- Group: `APP-CRM-Editors`

The workflow executes and validates this approved change:

- Department becomes Security Operations.
- Title becomes SOC Analyst.
- `APP-CRM-Editors` is removed.
- `SEC-SIEM-Readers` is added.
- Keycloak admin events are collected and sanitized.

The automation fails if any before/after expectation is not met. After a successful
run, GitHub Actions commits the evidence JSON and change record under
`live-tenant/evidence/`.

## Live workflow evidence

| Evidence | Location |
|---|---|
| Workflow explanation and controls | `live-tenant/keycloak-mover-workflow.md` |
| Admin API implementation | `scripts/run_keycloak_mover_workflow.py` |
| GitHub Actions execution | `.github/workflows/live-keycloak-iam.yml` |
| Verified before/after evidence | `live-tenant/evidence/keycloak_mover_evidence.json` |
| Change-closure record | `live-tenant/evidence/keycloak_change_record.md` |

## Supporting governance analysis

| Evidence | Location |
|---|---|
| Synthetic access-review sample | `data/access-review-sample.csv` |
| RBAC matrix | `data/rbac-matrix.csv` |
| MFA enforcement matrix | `data/mfa-enforcement-matrix.csv` |
| Privileged-access register | `data/privileged-access-register.csv` |
| Joiner-mover-leaver process | `iam-governance/joiner-mover-leaver-workflow.md` |
| Quarterly access-review process | `iam-governance/quarterly-access-review-process.md` |

The supporting CSVs remain explicitly synthetic. They show governance reasoning;
they are not represented as tenant exports.

## Skills demonstrated

- Live IAM realm administration through the Keycloak Admin API
- Joiner-mover-leaver execution and least-privilege remediation
- RBAC and group-entitlement management
- Before/after access validation
- IAM audit-event collection and evidence handling
- GitHub Actions automation
- Access-review, MFA, and privileged-access governance
- Clear control limitations and privacy safeguards

## Run manually

The GitHub Actions workflow is the easiest reproducible path. A local run requires
Docker and Python 3:

```bash
docker run -d --name keycloak -p 8080:8080 \
  -e KC_BOOTSTRAP_ADMIN_USERNAME=admin \
  -e KC_BOOTSTRAP_ADMIN_PASSWORD=change-me \
  quay.io/keycloak/keycloak:26.0.7 start-dev

python3 scripts/run_keycloak_mover_workflow.py \
  --admin-user admin \
  --admin-password change-me \
  --output-dir live-tenant/evidence
```

Use a unique password and never commit it.

## Limitations

- The live realm is ephemeral and contains only controlled lab identities.
- Keycloak is platform-neutral and does not prove Microsoft Entra or Okta experience.
- The same lab operator performs the request, approval, and execution steps; production
  separation of duties is documented but not demonstrated.
- This project demonstrates hands-on IAM lab administration, not production IAM employment.
