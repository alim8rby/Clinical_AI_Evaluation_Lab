# V1.5 — LLM Generation

## Scope

V1.5 establishes the generation boundary between retrieved evidence and a structured CAIEL Answer.

## Contract

A GenerationProvider receives a clinical question and EvidenceSet and returns an Answer containing:

- answer text;
- structured claims;
- citation indices referring to supplied evidence;
- uncertainty;
- model identifier;
- prompt version.

## Grounding policy

The generation prompt instructs the model to answer only from supplied evidence, avoid invented citations, expose uncertainty, and associate substantive claims with evidence.

## Provider abstraction

Provider-specific SDKs must remain behind GenerationProvider. The V1 implementation includes MockGenerationProvider so the pipeline can be tested without paid external APIs.

A real LLM provider is intentionally deferred to the provider integration increment.

## Excluded

External provider SDK implementation, streaming, tool calling, autonomous clinical decisions, patient data, and evaluation metrics.
