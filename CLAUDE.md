# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

AiFinanceTracker is a multi-service financial tracking application with three services:
- **Backend** (`../backend/`): ASP.NET Core Web API (.NET 10.0) — central "Gatekeeper" for security and data integrity
- **Frontend** (`../frontend/`): Angular 21 SPA with Vitest
- **AI Service** (`../ai-service/`): Python FastAPI + LangChain for RAG-based transaction classification

## Architecture

Clean Architecture with four projects (solution: `FamilyFinance.slnx`):

- **FamilyFinance.Domain** — Domain entities with self-validating constructors, no external dependencies
- **FamilyFinance.Application** — Use cases, interfaces (e.g., `IDocumentProcessor`), application logic
- **FamilyFinance.Infrastructure** — EF Core, external service implementations
- **FamilyFinance.Api** — Controllers, DI configuration, middleware

Dependency flow: Api → Application → Domain; Infrastructure → Application → Domain.

### Key Design Decisions
- Hybrid "Dual Memory" storage: SQL for transactions/amounts, Vector DB (ChromaDB) for unstructured content (receipts, contracts)
- Rule-based classification first (regex/hardcoded), AI fallback — saves tokens and guarantees accuracy for known patterns
- MCP (Model Context Protocol) for LLM tool integration
- REST API between services (ports & adapters pattern for future migration to message queues)

## Build & Run Commands

### Backend (.NET)
```bash
dotnet restore                              # restore NuGet packages
dotnet build                                # build solution
dotnet run --project FamilyFinance.Api      # run API (http://localhost:5225, https://localhost:7007)
```

### Frontend (Angular)
```bash
cd ../frontend
npm install
npm start       # ng serve (http://localhost:4200)
npm test        # vitest via ng test
npm run build
```

### AI Service (Python)
```bash
cd ../ai-service
conda env create -f environment.yml
conda activate family-finance
```

## Code Style

Enforced via `.editorconfig` — key conventions for C#:
- 4-space indentation, 120 char max line length, file-scoped namespaces
- Private fields: `_camelCase`, private static fields: `s_camelCase`
- Interfaces: `IPascalCase`, type parameters: `TPascalCase`
- `using` directives outside namespace (enforced as error)
- Prefer `var` when type is apparent; use explicit types otherwise
- Readonly fields enforced as warning
- Allman-style braces (opening brace on new line)

Frontend uses Prettier: 100 char print width, single quotes for TS, angular parser for HTML templates.
