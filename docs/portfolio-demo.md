# CAIEL Portfolio Demo

## Demo goal

Show that CAIEL does more than generate a clinical answer: it evaluates the system, preserves the evidence trail, identifies failures, and produces a reproducible research report.

**Target demo time:** 5 minutes.

## Demo sequence

### 1. Start at the dashboard — 20 seconds

Show the CAIEL interface and introduce the project:

> CAIEL is an evaluation platform for AI systems that answer clinical questions. The interesting part is not just the answer; it is understanding how the system arrived at it and how reliable that process was.

### 2. Clinical QA — 30 seconds

Open **Clinical QA** and ask:

```text
What are common symptoms of depression?
```

Point out that the system retrieves evidence before generating the answer.

Do not present this as clinical advice.

### 3. Experiment Library — 45 seconds

Open **Experiments** and select the baseline experiment.

Show:

- benchmark
- Top K
- model / embedding configuration
- retriever configuration
- reproducibility hash
- completed runs

Key message:

> Every evaluation run belongs to an explicit experiment configuration rather than being an isolated chatbot interaction.

### 4. Run a benchmark question — 45 seconds

Run `cq-001`:

```text
What clinical features are central to diagnosing a depressive episode?
```

Wait for completion.

Point out that the run records evaluation metrics, latency, token usage, and failure signals.

### 5. Evidence Explorer — 60 seconds

Open the completed run in **Evidence Explorer**.

Show the trace:

```text
Question
  ↓
Answer
  ↓
Claim
  ↓
Citation
  ↓
Retrieved chunk
  ↓
Source document
```

Highlight the distinction between:

- **Cited**
- **Retrieved only**

Key message:

> We can inspect not only what the model said, but exactly which retrieved evidence was used to support it.

### 6. Failure Observatory — 45 seconds

Open the experiment's **Failure Observatory**.

Show:

- failure category
- failure type
- severity
- metric signal
- experiment-level analysis

Key message:

> A failure is treated as an observable engineering event, not just a bad answer.

If the current experiment has no failures, say so. Do not invent one for the demo.

### 7. Research Report — 45 seconds

Open the **Research Report**.

Show:

- experiment identity
- reproducibility hash
- evaluator versions
- aggregate metrics
- failure signals
- methodology
- limitations

Close with:

> The output is a research artifact that can be inspected and compared, rather than a single model response.

## What to emphasize

### The core differentiator

**Typical RAG demo:**

> Can the model answer?

**CAIEL:**

> How well did retrieval work?  
> Were the claims grounded?  
> What evidence was used?  
> What failed?  
> Can we reproduce and compare the experiment?

### Engineering story

The project demonstrates:

- RAG
- evaluation engineering
- failure analysis
- experiment infrastructure
- reproducibility
- evidence traceability
- API/database integration
- local model infrastructure
- Dockerized deployment

## Demo rules

- Use local Ollama models.
- Use the controlled benchmark.
- Do not claim clinical validation.
- Do not present engineering metrics as clinical risk scores.
- Do not invent benchmark results.
- If a live model response differs from an earlier run, show the actual result and explain that local model output is not guaranteed to be bit-for-bit reproducible.

## Portfolio takeaway

The project should be presented as:

> **A platform for systematically evaluating, tracing, comparing, and investigating AI systems instead of simply trusting their outputs.**
