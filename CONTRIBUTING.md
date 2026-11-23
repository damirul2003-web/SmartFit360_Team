# Contributing to SmartFit360

Each member should make and review their own real work through their own GitHub account. Discuss changes that affect another member's work, project scope, hardware choices or agreed responsibilities before replacing existing content.

## Task and branch

1. Start from a current `main` branch and choose a task with one accountable owner.
2. Record the task card and relevant requirement, user story or design item. If an identifier has not been agreed, resolve it with the team rather than inventing an existing reference.
3. Create a short-lived branch for that task. Use a clear name such as `feature/<card-id>-short-description`, `fix/<card-id>-short-description` or `docs/<card-id>-short-description`.
4. Make focused changes. Keep useful teammate content and cite external sources.

Use meaningful commit messages that explain the actual change, for example `docs: clarify capture assumptions (<card-id>)`. Commit under your own author identity. Do not manufacture historical activity or attribute commits and reviews to someone who did not perform them.

## Pull request and review

Open a pull request before merging a task branch into `main`. Include:

- The problem, change and affected files.
- The linked task card and requirement or design item.
- Checks performed, actual outcomes and evidence links.
- Remaining limitations, planned checks and any decision needed from the team.

Ask another teammate to check correctness, consistency with the agreed scope, references, relevant tests and documentation. The reviewer should record their actual review. Resolve feedback before merging. Keep the author and reviewer visible in the pull request history.

The repository owner should configure `main` protection and required review where the repository's GitHub features permit it. Until settings are verified, follow the same team review rule manually; do not describe protection or checks as enabled merely because this guide proposes them. Confirm member access and the supervisor's required access separately.

The proposed [CODEOWNERS file](.github/CODEOWNERS) routes folder reviews to
confirmed collaborators and the repository owner. It records review responsibility,
not original authorship. Thisen's routing must be updated after the invitation is
accepted and write access is checked. Review requests use the CODEOWNERS file on
the pull request's base branch; this proposal takes effect after it is merged.
It does not enable a required-review rule by itself. See GitHub's
[code owner documentation](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-code-owners).

## Code and tests

- **Python:** clear names, small functions or services, useful type hints and separate tests. Record a compatible environment and dependency versions.
- **Flutter/Dart:** use the formatter and analyser, reusable widgets and relevant widget or unit tests.
- **ESP32 C++:** keep sensor handling, message validation and timeouts clear. Record the board, sensor carrier, firmware protocol and dependencies used.
- **Website:** commit the actual source and document how to run or build it when available.

There is no application test suite in the current artefact snapshot. Add runnable checks with the implementation. A test plan is not a completed test. Record the tested commit or build, tester, date, expected result, actual result and evidence; retain failures and link fixes and retests.

Keep a traceable chain from requirement and user story to task, branch or commit, pull request, test and review evidence. Do not add links to missing records or claim an appendix contains evidence that has not been added.

## Documents and binary files

Preserve the existing member folders and filenames unless the team agrees on a move. Folder placement alone does not prove authorship. Tell teammates before editing the same Word, PDF, presentation or image file, because binary changes are difficult to merge.

Keep editable source with its export where available. Describe document or diagram changes in the pull request and check the rendered result. Avoid duplicate copies with unexplained names; record the current version and link the relevant review.

Check files for secrets, participant data and unnecessary personal information before uploading to this public repository. Keep citations, licences for reused material and any required AI-assistance declaration. Do not add a licence for the whole repository without a team decision.

## Completion

For a coursework design item, completion means it meets the brief, agrees with related requirements, has been checked by another member and has linked review evidence. For implementation, also record passing relevant tests, a reviewed merge, setup instructions and limitations. A schematic does not prove a physical device works, and a prototype image does not prove the application is implemented.
