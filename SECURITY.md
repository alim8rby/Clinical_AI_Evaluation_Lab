# Security Policy

## Scope

CAIEL is a public portfolio/research project and is intentionally **not a production clinical system**.

Do not submit real patient data, protected health information, credentials, API keys, or other sensitive information to the demo application or repository.

## Supported versions

Only the current `main` branch is considered supported.

## Reporting a vulnerability

If you discover a security issue in CAIEL, please report it privately to the repository owner rather than opening a public issue with exploit details.

Include:

- a short description of the issue
- affected component or file
- reproduction steps, if available
- potential impact
- any suggested mitigation

Please do not include real patient information or other sensitive data in the report.

## Known non-production boundaries

The V5 audit documents known limitations including:

- no authentication or authorization
- no rate limiting
- no TLS/production ingress
- local Ollama runtime
- no hosted deployment or production secret-management system

These limitations are intentional boundaries of the portfolio/demo scope and should not be interpreted as claims of production security.

## Responsible use

CAIEL is for engineering research, evaluation, and demonstration. Its outputs must not be used as autonomous clinical decisions or as a substitute for professional medical judgment.
