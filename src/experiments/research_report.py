"""Deterministic research-report rendering for experiment results."""

def render_research_report(*, experiment, sample_count, metrics, failures):
    snapshot = experiment.config.reproducibility_snapshot().as_dict()
    lines = [
        f"# Research Report — {experiment.name}",
        "",
        "## Executive summary",
        "",
        experiment.description or "No experiment description was provided.",
        "",
        f"- Experiment ID: `{experiment.experiment_id}`",
        f"- Benchmark: `{experiment.config.benchmark_version}`",
        f"- Completed runs: **{sample_count}**",
        f"- Reproducibility hash: `{snapshot['config_hash']}`",
        "",
        "## Reproducibility configuration",
        "",
        "| Dimension | Version |",
        "|---|---|",
        f"| Model | {snapshot['model_version']} |",
        f"| Embedding | {snapshot['embedding_version']} |",
        f"| Retriever | {snapshot['retriever_version']} |",
        f"| Prompt | {snapshot['prompt_version']} |",
        f"| Benchmark | {snapshot['benchmark_version']} |",
        f"| Runtime | {snapshot['runtime_version']} |",
        f"| Schema | {snapshot['schema_version']} |",
        "",
        "### Evaluators",
        "",
    ]
    evaluators = snapshot["evaluator_versions"]
    if evaluators:
        lines.extend(f"- {name}: {version}" for name, version in sorted(evaluators.items()))
    else:
        lines.append("- None recorded")
    lines.extend([
        "",
        "## Configuration",
        "",
        f"- Top K: **{experiment.config.top_k}**",
        f"- Model config: `{_compact(experiment.config.model_config)}`",
        f"- Embedding config: `{_compact(experiment.config.embedding_config)}`",
        f"- Retriever config: `{_compact(experiment.config.retriever_config)}`",
        "",
        "## Evaluation results",
        "",
    ])
    if metrics:
        lines.extend([
            "| Metric | Value |",
            "|---|---:|",
            *[f"| {name} | {value:.6f} |" for name, value in sorted(metrics.items())],
        ])
    else:
        lines.append("No completed evaluation metrics are available for this experiment.")
    lines.extend([
        "",
        "## Failure signals",
        "",
        f"Recorded failures: **{len(failures)}**",
        "",
    ])
    if failures:
        counts = {}
        for failure in failures:
            category = failure.get("category", "UNKNOWN")
            counts[category] = counts.get(category, 0) + 1
        lines.extend(["| Category | Failures |", "|---|---:|", *[f"| {k} | {v} |" for k, v in sorted(counts.items())]])
    else:
        lines.append("No recorded failures are associated with this experiment.")
    lines.extend([
        "",
        "## Methodology",
        "",
        "Results are produced by the frozen CAIEL evaluation pipeline using the experiment's recorded benchmark, retrieval, generation, grounding, reliability, and evaluator configuration.",
        "",
        "Metrics are engineering evaluation signals. They are not clinical validation, clinical risk scores, or evidence of clinical superiority.",
        "",
        "## Limitations",
        "",
        "- The current benchmark and evidence corpus are compact engineering datasets.",
        "- Model-assisted evaluation is not human clinical ground truth.",
        "- Local model and embedding behavior can vary by provider/runtime.",
        "- Reproducibility configuration identity does not guarantee bit-for-bit model output reproducibility.",
        "- Historical experiments created before V5.9 may contain explicit compatibility values such as `unspecified`.",
        "",
    ])
    return "\n".join(lines)

def _compact(value):
    import json
    return json.dumps(value, sort_keys=True, separators=(",", ":"))
