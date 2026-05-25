# Cobalto

Cobalto is an MLOps-oriented credit risk decision engine.

The goal is to build a production-style ML system that estimates probability of default for loan applications and turns model scores into business decisions: approve, reject, or manual review.

## Core Goals

- Build a reproducible data ingestion pipeline.
- Store raw data without modification.
- Create validated training datasets.
- Train and track credit risk models.
- Serve predictions through an API.
- Log predictions and decisions.
- Monitor data drift and model performance.

## First Milestone

The first milestone is the data layer:

- Select a real credit risk dataset.
- Document the source.
- Store raw data in immutable form.
- Define the target variable.
- Identify leakage-prone columns.
- Create a reproducible processed dataset.
