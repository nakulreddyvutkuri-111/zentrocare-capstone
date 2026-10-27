# ZentroCare — Evidence-first customer support capstone

A runnable, offline **text-support prototype** for the supplied fictional ZentroMart dataset. This is an extractive retrieval system with deterministic order workflows, not an LLM-powered production agent. No paid API keys required.

## Quick start
Python 3.11+ recommended. In this folder:

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
python app.py
```
Open `http://localhost:8501` in your browser. The server binds to localhost deliberately; it is not a public demo. Use Reset between customers.

## Reproduce the evidence
```bash
python dataset/validate_dataset.py
python -m unittest discover -s tests -v
python evaluate.py
python build_report.py
```
The report builder also creates dataset summaries and charts. Evaluation reads practice labels **only in the evaluation script**, never in the agent. It measures macro policy-section recall and truncated reciprocal rank, not answer correctness. All supplied practice data are development/diagnostic data, not a held-out benchmark.

## Demo walkthrough
1. Ask `How fast are refunds to the ZentroMart Wallet?` — inspect REF-2.
2. Enter `8978 2837` — no order information is revealed.
3. Enter synthetic registered phone suffix `4533` — verification succeeds. This proof is supplied solely for local synthetic demonstration; never use this authentication scheme for real accounts.
4. Ask `What is the status?` — verified order state is used.
5. Ask `Please connect me to a human agent` — a local mock ticket is created.
6. Reset. Enter the same order and give `0000` twice, then the correct suffix — the session refuses another attempt for that active order.
7. Ask `The battery has a burning smell` — immediate safety instruction and mock escalation.

## Structure
- `src/agent.py`: retrieval, date helpers, guarded state machine.
- `app.py`: local browser chat using the Python HTTP server.
- `tests/`: automated component/security-regression tests.
- `evaluate.py`: policy evidence evaluation on original and ASR-like text.
- `build_report.py`: reproducible PDF and analysis builder.
- `reports/`: PDF, metrics, row-level retrieval results, test log, and charts.
- `dataset/`: original supplied data, knowledge base, tools and validator.

## Implemented
- Markdown section chunks retaining IDs, document status and effective date.
- Current-document filtering; current RET-3 retains the historical electronics exception.
- Word/character TF-IDF hybrid retrieval, authority weights and small business-concept priors.
- Limited Hindi/Hinglish synonym expansion; English-first output.
- Verified lookup, retry gate, per-browser-session state, reset, secret-free tool summaries.
- Verified order status; cancellation guidance; return-date/holiday-aware refund calculations.
- Selected safety, legal, unauthorized activity, repeat-contact, high-value damage and overdue-refund escalation rules.
- Genuine mock-tool ticket creation; no claims of real order modification.

## Explicit limitations / incomplete brief requirements
- Gnani WebSocket STT/TTS is **not implemented or tested**. ASR-text evaluation is not a voice test.
- Replies are mostly excerpts, not fluent multilingual responses. Language coverage is limited.
- No full 96-turn conversation scoring or native-language review has been completed.
- Generic retrieval can miss evidence, retrieve conflicting lower-authority text, and mishandle unsupported requests. Authority weighting is not full conflict resolution.
- The 0.12 abstention threshold is heuristic, not a calibrated safety classifier. Concept priors can defeat abstention on unrelated questions.
- Policy excerpts show general rules; they do not approve refunds. Return deadline is delivery date plus N calendar days, an explicit boundary convention pending reviewer confirmation.
- Session retry count is for the active order only; switching orders or resetting can bypass it. No persistent anti-abuse control.
- Mock suffix/pincode checking is **not real authentication**; session store is memory-only, limited to 100 sessions and cleared at capacity.
- Ticket summaries omit free-form customer detail to avoid secret leakage; they do not fully satisfy every ESC-3 handover-detail requirement.
- HTTP server has no production TLS, CSRF protection, durable sessions or distributed concurrency. Do not expose it publicly unchanged.
- No public repository, live URL, or evaluation-portal submission is included or claimed.

## Publication / submission
See SUBMISSION_GUIDE.md. Supplied data are declared synthetic, but no redistribution license is supplied: verify your course permits public dataset upload before publishing. Do not commit generated tickets, credentials or real personal data. No project license is asserted over supplied material.

## Academic integrity
AI-assisted implementation and documentation. Review, run, personalize and disclose assistance according to your course rules. Do not describe unimplemented functionality as finished.
