# SmartFit360 Team Repository

SmartFit360 is a proposed customer and independent-tailor workflow built around a reviewed measurement profile. This repository holds the team's coursework research, planning documents, diagrams and presentation artefacts.

The current snapshot does **not** contain a working SmartFit360 application, validated measurement station or tested pattern generator. Documents describe proposals and reported progress; they are not evidence that the corresponding product feature works.

## Proposed product

- **SmartMeasure:** manual measurement entry first, with assisted phone-camera and ToF sensor capture investigated through staged tests. The proposed sensor arrangement studies width and depth at a selected level; it does not establish automatic body girths or a full 3D scan.
- **SmartFit Online:** compare reviewed measurements with a supplied clothing size chart and explain the result. Start with explicit rules and a limited clothing category.
- **SmartPattern:** check the required inputs for one reviewed pattern template and produce a full-scale A1 PDF. PDF scale, drafting correctness and garment fit need separate checks.

The proposed stack is Flutter/Dart, Python FastAPI and PostgreSQL, with a local Python/OpenCV/MediaPipe station and ESP32 C++ firmware. These are design choices, not a claim that these components have been implemented or integrated.

## Team artefacts

The existing folder names are retained from the supplied archive. A folder groups material for review; it does not establish authorship of every file inside it.

| Member | Focus recorded in the working agreement | Artefacts | GitHub account |
| --- | --- | --- | --- |
| Damiru | Team lead and planning | [damiru/](damiru/) | [damirul2003-web](https://github.com/damirul2003-web) |
| Sachith | IoT and architecture | [sachith/](sachith/) | [sachithpamoda](https://github.com/sachithpamoda) |
| Thisen | Requirements and feature flow | [thisen/](thisen/) | [Thissa-D](https://github.com/Thissa-D) (invitation pending) |
| Paramee | Risk, testing and ethics | [parami/](parami/) | [paramiv0217-cloud](https://github.com/paramiv0217-cloud) |
| Sasmitha | Prototype, landing page and portfolio coordination | [sasmith/](sasmith/) | [sasmitha-z](https://github.com/sasmitha-z) |

The working agreement is in [damiru/smartfit_Team_Working_Agreement.docx](damiru/smartfit_Team_Working_Agreement.docx). All members share responsibility for reviewing work, integration and understanding the project.

Browse the [artefact index](docs/artefact-index.md) for individual files and the
[repository setup checklist](docs/repository-setup.md) for access, review and
coursework evidence still to confirm.

All 15 artefacts from the supplied archive are included. Thirteen are unchanged;
the technical report and workflow PDF were revised on 23 November 2026 to match
the current coursework hardware plan, stack and LKR 91,600 budget. See the
artefact index for the revision record.

The [team task list](docs/team-tasks.md) links eight open GitHub issues with
acceptance criteria. Tasks with confirmed responsibilities are assigned; the
team must agree owners for the remaining implementation tasks.

## Version control

Read [CONTRIBUTING.md](CONTRIBUTING.md) before making changes. Use short task branches, meaningful commits by the actual author and a pull request checked by another teammate before merging. Link changes to the relevant task card and requirement or design item.

The repository owner should confirm each member's access, provide the supervisor's required access and configure protection for `main` where available. These settings must be checked in GitHub; this README does not claim they are enabled.

An initial archive import records who imported the files. It does not recreate the original authors' Git history. Individual contribution evidence must come from genuine subsequent changes, reviews, task records and Google Document history.

## Implementation and evidence

There is no application setup, build or test command for this artefact snapshot. Add source code, reproducible setup instructions, dependencies and relevant tests when implementation begins. The marketing website's source also belongs in the team repository when available.

Keep editable source alongside exported diagrams or documents where available. Record actual test results with the version, tester, date and evidence link. Mark planned or unexecuted checks clearly; do not report a test as passed without a recorded result.

Do not upload secrets, account credentials, participant records, raw body images or identifiable measurements. Check document contents and image metadata before adding files to this public repository. Retain citations and record AI assistance as required by the coursework.
