# Architecture Decision Records (ADRs)
## Nexus Research Intelligence Platform

This folder contains Architecture Decision Records (ADRs). 

An ADR is a short text document that captures an important architectural decision made along with its context and consequences.

## Why use ADRs?
In an educational project like Nexus, *why* we built something a certain way is more important than *what* we built. ADRs serve as a historical log of our engineering rationale.

## How to create an ADR
When making a significant architectural choice (e.g., "Choosing PostgreSQL over MongoDB", "Using Pydantic for State Management"), create a new markdown file in this directory following the sequential numbering format: `XXXX-short-title.md` (e.g., `0001-use-clean-architecture.md`).

## ADR Template

```markdown
# ADR [Number]: [Title]

**Date:** YYYY-MM-DD
**Status:** [Proposed | Accepted | Superseded]

## Context
What is the problem we are trying to solve? What are the constraints?

## Decision
What is the change we are making?

## Consequences
What becomes easier or more difficult because of this change? (Positive and Negative impacts)
```
