# Final Report

## Summary

This IAM review identified access that should be kept, reduced, removed, or formally approved. The highest-priority issue was active access for a former contractor. The second priority was privileged access that needed better approval evidence.

## Initial observations

Most access did not look obviously wrong at first. The review became more useful after comparing access against user role and employment status.

## What could not be confirmed

- Whether users actually used the access recently.
- Whether the business owners would approve every RBAC assumption.
- Whether MFA was enforced in a real tenant.
- Whether any access was temporary and should have expired.

## Recommended next steps

1. Remove former contractor access.
2. Reduce unnecessary customer export access.
3. Confirm MFA enforcement for all critical systems.
4. Review privileged access quarterly.
5. Add evidence from a real SaaS admin lab in a future version.
