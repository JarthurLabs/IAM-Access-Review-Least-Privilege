# Final Report: IAM Access Review & Least Privilege Remediation

## Executive Summary

A simulated identity and access management review showing how to assess user permissions, identify excessive access, recommend role-based access control, and document offboarding controls.

The main purpose of this project is to demonstrate practical cybersecurity judgment. The project uses synthetic data and a realistic small-business scenario to show how security work should be documented: scope, evidence, findings, impact, and recommendations.

## Scope

- Environment: Synthetic small-business environment
- Data classification: Public-safe simulated data
- Objective: Identify security risks and produce actionable recommendations
- Out of scope: Real client data, exploitation, malware execution, unauthorized scanning

## Methodology

1. Reviewed the scenario and defined the security objective.
2. Examined the provided synthetic data.
3. Identified findings and assigned practical severity.
4. Documented impact in plain business language.
5. Recommended remediation steps.
6. Summarized how the work maps to entry-level cybersecurity responsibilities.

## Findings

### Finding 1: Former contractor account still active

- **Severity / Type:** High
- **Impact:** Offboarding gap creates unauthorized access risk.
- **Recommended Action:** Validate the issue, assign an owner, prioritize based on business impact, document remediation, and retest.

### Finding 2: Sales user has admin access

- **Severity / Type:** High
- **Impact:** Permission does not match job function.
- **Recommended Action:** Validate the issue, assign an owner, prioritize based on business impact, document remediation, and retest.

### Finding 3: Shared admin account exists

- **Severity / Type:** Medium
- **Impact:** No accountability or user-level audit trail.
- **Recommended Action:** Validate the issue, assign an owner, prioritize based on business impact, document remediation, and retest.

### Finding 4: Finance role can access support tickets

- **Severity / Type:** Medium
- **Impact:** Possible exposure to unnecessary customer data.
- **Recommended Action:** Validate the issue, assign an owner, prioritize based on business impact, document remediation, and retest.

### Finding 5: Naming convention inconsistent

- **Severity / Type:** Low
- **Impact:** Makes access review harder and increases operational error.
- **Recommended Action:** Validate the issue, assign an owner, prioritize based on business impact, document remediation, and retest.

## Recommendations

- Prioritize high-impact issues first.
- Assign each finding to a clear owner.
- Track remediation status.
- Retest after changes are made.
- Keep documentation concise enough for business stakeholders and detailed enough for technical follow-up.

## What This Demonstrates to Employers

This project shows I understand the business side of security: people need access to work, but excessive access creates risk. I can document who has access, why it matters, and how to fix it without breaking operations.

## Resume Bullet Option

Built a cybersecurity portfolio project simulating iam access review & least privilege remediation, documenting scope, evidence, findings, risk impact, and remediation recommendations using public-safe synthetic data.
