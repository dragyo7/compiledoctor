# Development Guide

> This document serves as the implementation roadmap for **CompileDoctor – Intelligent Compiler Error Diagnosis & Recovery System**. It outlines the development workflow, coding standards, project milestones, and best practices to ensure the implementation remains aligned with the approved project documentation.

---

# Project Overview

CompileDoctor is an educational compiler front-end designed to help beginner programmers understand compiler errors through simplified diagnostics and visualization of the compiler pipeline.

The project is implemented as a **6–8 week semester mini project** for the Compiler Construction course.

---

# Development Philosophy

The project follows these guiding principles:

- Keep the implementation simple and modular.
- Build incrementally.
- Test every module before proceeding.
- Prioritize readability over optimization.
- Focus on educational value rather than production-grade complexity.
- Maintain consistency with the approved PRD, Design Document, TRD, and Implementation Plan.

---

# Compiler Pipeline

The implementation follows the traditional compiler front-end pipeline:

```text
Source Code
     │
     ▼
Lexer
     │
     ▼
Parser
     │
     ▼
AST Construction
     │
     ▼
Semantic Analysis
     │
     ▼
Diagnostics
     │
     ▼
Error Recovery
     │
     ▼
Visualization
```

Each stage should be completed and tested before moving to the next.

---

# Development Phases

## Phase 1 – Project Bootstrap

### Objectives

- Verify project structure.
- Configure virtual environment.
- Install dependencies.
- Verify Flask application starts successfully.
- Configure Git repository.

### Deliverables

- Working project structure
- Flask running locally
- Git initialized
- Dependencies installed

---

## Phase 2 – Lexical Analysis

### Objectives

Implement:

- Reserved keywords
- Identifiers
- Numbers
- Operators
- Delimiters
- Comments
- Whitespace handling

### Deliverables

- Functional lexer
- Token stream generation
- Lexer test cases

---

## Phase 3 – Syntax Analysis

### Objectives

Implement:

- Grammar rules
- Operator precedence
- Parser
- Syntax error detection

### Deliverables

- Parse validation
- Syntax error reporting
- Parser tests

---

## Phase 4 – AST Construction

### Objectives

Implement:

- AST node classes
- AST generation
- Tree visualization

### Deliverables

- AST builder
- AST visualization

---

## Phase 5 – Semantic Analysis

### Objectives

Implement:

- Symbol table
- Scope checking
- Variable declaration validation
- Type checking

### Deliverables

- Semantic analyzer
- Symbol table visualization
- Semantic error detection

---

## Phase 6 – Educational Diagnostics

### Objectives

Generate beginner-friendly explanations for compiler errors.

Each error should include:

- Error type
- Description
- Cause
- Suggested fix
- Example correction

### Deliverables

- Diagnostic engine
- Error explanation library

---

## Phase 7 – Error Recovery

### Objectives

Implement recoverable parsing to continue analysis after encountering errors.

### Deliverables

- Multiple diagnostics in one run
- Basic recovery strategies

---

## Phase 8 – Frontend Integration

### Objectives

Develop:

- Code editor
- Analyze button
- Result panels
- AST visualization
- Diagnostic display

### Deliverables

- Interactive web interface

---

## Phase 9 – System Integration

### Objectives

Connect:

- Frontend
- Backend
- Compiler pipeline
- Visualizations

### Deliverables

- End-to-end working application

---

## Phase 10 – Testing and Refinement

### Objectives

Perform:

- Unit testing
- Integration testing
- Bug fixes
- UI improvements
- Documentation review

### Deliverables

- Stable project
- Final demo version

---

# Coding Standards

Follow:

- PEP 8
- Meaningful variable names
- Small, focused functions
- Modular design
- Consistent formatting

Avoid:

- Unused code
- Global variables where unnecessary
- Duplicate logic
- Premature optimization

---

# Folder Responsibilities

## backend/

Contains compiler implementation.

### lexer/

Lexical analysis.

### parser/

Grammar and parsing.

### ast/

AST generation.

### semantic/

Semantic analysis and symbol table.

### diagnostics/

Educational error explanations.

### recovery/

Error recovery logic.

### utils/

Shared helper functions.

---

## frontend/

Contains the web interface.

### templates/

HTML templates.

### static/

CSS, JavaScript, images.

---

## examples/

Sample programs.

- valid/
- invalid/

---

## tests/

Unit and integration tests.

---

## docs/

Project documentation.

---

# Testing Strategy

Every completed module should include:

- Unit tests
- Example inputs
- Expected outputs
- Invalid inputs
- Edge cases

No module should be considered complete until tested.

---

# Git Workflow

Commit after each major milestone.

Example commit messages:

```text
Initial project setup
Implemented lexer
Added lexer tests
Implemented parser
AST generation completed
Semantic analyzer implemented
Diagnostics engine completed
Frontend integration
Project ready for final demonstration
```

---

# Development Checklist

## Before Starting a Module

- Review relevant documentation.
- Understand requirements.
- Identify dependencies.

---

## During Development

- Implement incrementally.
- Test frequently.
- Commit meaningful progress.

---

## Before Completing a Module

- Code reviewed.
- Tests passing.
- Documentation updated.
- No known critical bugs.

---

# Definition of Done

A module is considered complete when:

- Functionality is implemented.
- Unit tests pass.
- Code follows project standards.
- Documentation is updated.
- Integration with previous modules works correctly.

---

# References

Implementation should remain consistent with:

- Product Requirements Document (PRD)
- Design Document
- Technical Requirements Document (TRD)
- Implementation Plan
- Engineering Decisions
- Compiler Construction syllabus

---

# Notes

This guide is intended to keep the project focused, manageable, and aligned with its educational objectives.

Any significant architectural or technological changes should be evaluated against the approved documentation before implementation.