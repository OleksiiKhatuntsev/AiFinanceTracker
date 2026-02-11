# 📄 Architecture Decision Log: Family Finance RAG
Status: Draft / Approved Date: 2026-02-11

## Frontend: Angular
#### Decision: 
Use Angular (latest version) for the frontend application.

#### Justification:

- **Professional Development:** Strategic goal to enhance skills and portfolio (Resume Driven Development).

- **Architecture:** Angular's strict modularity, dependency injection, and TypeScript support are superior for building complex dashboards with data visualization, compared to more lightweight libraries.

## Backend Core: C# (.NET)
#### Decision: 
ASP.NET Core Web API as the central backend service.

#### Justification:

- **Security:** Acts as the system's "Gatekeeper". Built-in mechanisms for Identity, JWT, and potential encryption are critical for handling sensitive financial data.

- **Reliability:** Strong typing and a robust ORM (EF Core) ensure transaction integrity. Python is reserved solely for AI tasks where strict typing is less critical than flexibility.

3. AI Service: Python
Decision: Python (FastAPI / LangChain) as a dedicated microservice.

Justification:

Ecosystem: Python is the de facto standard for AI/ML. Libraries for RAG (LlamaIndex, LangChain) and Vector DB drivers are maintained and updated here first.

Isolation: Decoupling AI logic into a separate service allows for updates to RAG models and logic without destabilizing the core C# backend.

4. Data Storage: "Dual Memory" Strategy
Decision: Use a hybrid database approach:

SQL (Relational): For transactions, amounts, dates, and strict categories.

Vector DB (Chroma/Pinecone): For receipt text, contract terms, and unstructured content.

Justification: Solves the "LLM Math Hallucination" problem. Vector DBs cannot perform accurate aggregate functions (e.g., SUM), so precise figures are retrieved via SQL, while semantic context is retrieved via vector search.

5. Inter-service Communication: Ports & Adapters
Decision: REST API (HTTP) for MVP, with strictly defined C# Interfaces (Abstractions).

Justification:

Speed (MVP): HTTP is easier to debug and implement than message queues initially.

Flexibility: Using interfaces (e.g., IDocumentProcessor) enables a future migration to asynchronous communication (RabbitMQ/Kafka) without rewriting business logic (Loose Coupling).

6. Infrastructure: On-Premises (Localhost) -> Cloud Ready
Decision: Docker Compose for local development.

Justification:

Privacy: Financial documents remain within the home network perimeter during the MVP phase.

Scalability: Containerization ensures a seamless transition to cloud providers (Azure/AWS) in the future.

7. AI Protocol: MCP (Model Context Protocol)
Decision: Implement MCP to connect tools to the LLM.

Justification: Standardization. Instead of writing custom "glue code" for function calling, MCP provides a unified protocol. This makes the architecture extensible and allows for easy integration of pre-built tools (e.g., Google Drive, Slack).

8. Data Processing Strategy: Rule-Based First
Decision: Apply deterministic rules (Regex/Hardcoded logic) for known transaction types (e.g., salary, internal transfers) before falling back to AI.

Justification:

Cost Efficiency: Saves tokens on routine operations.

Accuracy: Rules provide 100% classification guarantees for repetitive patterns where probabilistic AI might fail or hallucinate.
