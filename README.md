# FastAPI DDD Template

A clean, production-ready Domain-Driven Design + Hexagonal Architecture template for FastAPI.

Built with modern best practices (2025):

- FastAPI (async)
- SQLAlchemy 2.0 + async session
- Pure DDD: Entities, Value Objects, Domain Events, Aggregates
- Hexagonal / Clean Architecture
- Unit of Work + Repository pattern
- Dependency inversion via Protocols
- Argon2id password hashing
- Explicit, type-safe, and fully testable structure

Designed to serve as:
- A learning reference for advanced backend architecture
- A solid foundation for microservices and long-lived projects
- A template you can clone and extend confidently

### Project structure

```
app/
├── domain/          # Pure business logic (no framework imports)
├── application/     # Use cases, commands, handlers
├── infrastructure/  # Database, external adapters, implementations
└── presentation/    # FastAPI routers, DTOs, dependencies
```

### Features

- 100% async
- Zero hidden magic
- Easy to test (no database in unit tests)
- Ready for gRPC, CQRS, Event Sourcing, Docker, etc.
- Follows patterns used in high-scale production systems

### Status

Actively maintained · Work in progress · Continuously improved

Feel free to fork, study, and use as your personal architecture playground.

Contributions and stars are highly appreciated!

---
Made with passion for clean, maintainable, and scalable code.