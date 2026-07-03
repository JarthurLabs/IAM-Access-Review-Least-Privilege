# Analyst Journal

This project came out of a very practical question: who has access, why do they have it, and would I be comfortable explaining that access to a manager or auditor?

## First pass

My first review focused too much on permission names. I looked for admin access, broad access, and missing MFA. That was useful, but it missed the bigger IAM story.

An account can look normal in a permissions table and still be risky if the person is no longer with the company, changed roles, or has no clear owner.

## Correction

I changed the review to look at four things together:

- employment or contractor status
- role fit
- MFA requirement
- approval and review evidence

That made the former contractor account stand out faster than some of the more obvious admin-access items.

## Threshold I reconsidered

At first I wanted to treat every admin account as a remove decision. That is too blunt. Admin access is sometimes valid. The better question is whether it is approved, reviewed, protected by MFA, and limited to the person who actually needs it.

So the project uses a few different outcomes: keep, reduce, remove, approve, and investigate.

## Small lesson

Least privilege is not about making everyone miserable. It is about making access easier to explain and harder to abuse. There is a difference, and it matters.