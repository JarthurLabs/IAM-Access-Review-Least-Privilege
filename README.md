# IAM Access Review & Least Privilege Remediation

## Overview

This is an IAM governance lab for a simulated small business. It reviews user access, role fit, MFA requirements, privileged access, and offboarding gaps.

The project is intentionally practical. It is less about theory and more about the kind of access cleanup that happens in real SaaS environments: someone changed roles, a contractor stayed active too long, a user has more access than they need, and admin access needs a better approval trail.

All names, systems, and access decisions are synthetic.

---

## What I reviewed

| Evidence | Location |
|---|---|
| Access review sample | `data/access-review-sample.csv` |
| RBAC matrix | `data/rbac-matrix.csv` |
| MFA enforcement matrix | `data/mfa-enforcement-matrix.csv` |
| Privileged access register | `data/privileged-access-register.csv` |
| JML workflow | `iam-governance/joiner-mover-leaver-workflow.md` |
| Quarterly review process | `iam-governance/quarterly-access-review-process.md` |

---

## Initial observations

The first pass looked mostly normal until the former contractor account appeared. That changed the priority. A former user with active access is usually more urgent than a current employee with slightly excessive permissions.

The second issue was privileged access. Admin access was not automatically wrong, but it needed clearer approval evidence and review timing.

---

## Screenshots

### JML workflow

![JML Workflow](./screenshots/jml-workflow.svg)

### Access review dashboard

![Access Review Dashboard](./screenshots/access-review-dashboard.svg)

### RBAC matrix

![RBAC Matrix](./screenshots/rbac-matrix.svg)

### MFA enforcement matrix

![MFA Enforcement Matrix](./screenshots/mfa-enforcement-matrix.svg)

### Privileged access register

![Privileged Access Register](./screenshots/privileged-access-register.svg)

---

## Access decisions

| Decision | Analyst reasoning |
|---|---|
| Keep | Access matched role and business need |
| Reduce | User still needed access, but not at the current permission level |
| Remove | Access no longer had a valid business reason |
| Approve | Privileged access was justified but needed explicit documentation |
| Investigate | More context would be needed before changing access |

---

## What I could confirm

- The access review process identifies keep/reduce/remove decisions.
- Role-based access examples are documented.
- MFA requirements are mapped by system.
- Privileged access is separated from standard access.

## What I could not confirm

- No real SaaS admin export was reviewed.
- No live identity provider was checked.
- The access review does not prove SOX compliance.
- The RBAC matrix is a starting point and would need business owner validation.

---

## Next steps

1. Add a lab export from Google Workspace, Microsoft Entra, Okta, or another SaaS admin console.
2. Track one access review cycle from request to remediation.
3. Add evidence of removed or reduced access.
4. Add temporary access expiration examples.
