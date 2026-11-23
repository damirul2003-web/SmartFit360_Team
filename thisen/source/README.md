# Workflow PDF source

This editable ReportLab source builds the nine-page workflow PDF in the parent folder. It contains the same revised A-E design sections and diagrams as the supplied PDF. The requirements pin the ReportLab version used for the revision.

From this folder, install the dependency and build a review copy:

```sh
python -m pip install -r requirements.txt
python build_workflow.py --output workflow-review.pdf
```

The default command `python build_workflow.py` replaces `../SmartFit360_Complete_Project_Workflow.pdf`. Review all pages before committing a regenerated PDF. Keep changes to the source and PDF together.

The default font is built-in Helvetica, so no machine-specific font installation is required. To reproduce the embedded Arial typography of the checked PDF, supply both existing font files:

```sh
python build_workflow.py --font-regular /path/to/arial.ttf --font-bold /path/to/arialbd.ttf --output workflow-review.pdf
```

If either optional font file is absent, the builder reports that it is using Helvetica. Font changes can alter line wrapping. The builder checks paragraph, box and table bounds, but a visual review is still required. PDF rendering tools and optional text-check libraries are quality checks, not runtime dependencies of this source.

The report describes proposed design and reported progress. Retain qualifications and source/version notes when editing; add real test evidence separately. Revision preparation used OpenAI Codex assistance.
