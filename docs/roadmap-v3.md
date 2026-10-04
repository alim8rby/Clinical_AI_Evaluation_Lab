# V3 Roadmap — Failure Observatory

## Goal

Turn V2 evaluation signals into a structured system for classification, inspection, analysis, and regression testing.

## V3 status

**V3.0–V3.10: COMPLETE AND FROZEN**

The phase remains local and UI-independent at the domain boundary. Production infrastructure is intentionally deferred to V4.

## Completed scope

- Failure architecture and contract
- Failure model and deterministic serialization
- Deterministic classification
- Severity and triage
- Local JSON persistence
- Failure analysis and filtering
- Known-failure regression suite
- Observatory query layer
- Failure Observatory UI
- End-to-end workflow integration
- V3 audit and freeze

## Freeze boundary

V3 does not introduce PostgreSQL, production APIs, authentication, deployment, Kubernetes, real patient data, autonomous clinical decisions, additional clinical domains, fine-tuning, or multi-agent systems.

## Next phase

**V4 — Productionization**

The next implementation boundary is the production API and persistence layer. V3 domain contracts should be treated as frozen inputs to that work.
