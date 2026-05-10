# NextCure Intelligence System v0.9

Interpretation Engine iteration on top of v0.8.7.

## What changed

- Added `engines/synthesis_engine.py`, a higher-order executive synthesis layer that sits above the existing technical, catalyst, capital-flow, activation, and strategy engines.
- Added an **Interpretation Engine** dashboard page focused on meaning, trend interpretation, emerging competitive edges, and operating recommendations.
- Added synthesized signal cards for market participation, catalyst recognition, technical read-through, and visibility/attention.
- Added a patent/grant intelligence roadmap table that prepares the schema and executive questions for future ingestion without pretending live patent/grant automation is already complete.
- Wired synthesis output into the Executive Summary so Michael immediately sees synthesized meaning before granular charts.
- Preserved the one-button operating model and existing modular architecture.
- Added a regression test for the synthesis engine.

## Run

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Audit

```bash
PYTHONPATH=. pytest -q
python -m compileall .
```
