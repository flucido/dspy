# Research: Reliable Backend API for Aeries Data Retrieval

## Decision: Scale/Scope
Decision: Small scale, 10k users, 1M LOC, 50 screens.

Rationale: Based on typical school data retrieval system, as not specified in spec.

Alternatives considered: Large scale (100k users, 10M LOC), but rejected due to lack of specification.

## Decision: Best practices for Python dependencies
Decision: Use standard libraries for requests, pandas, pymssql.

Rationale: They are well-maintained and fit the requirements.

Alternatives considered: Custom libraries, but rejected for simplicity.

## Decision: Integration patterns for Aeries API
Decision: Use REST API with certificate authentication.

Rationale: Matches the spec's security requirements.

Alternatives considered: GraphQL, but rejected for simplicity.
