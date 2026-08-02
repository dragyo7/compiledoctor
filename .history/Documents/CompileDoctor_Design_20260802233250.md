The requested Design Document is too large to fit within a single response while preserving complete Mermaid diagrams and section integrity as you requested. Following your stopping rules, I will begin with the first logical portion and stop only after a complete section boundary.

Using the approved PRD together with the Version 1 documentation and Audit Report as the authoritative sources, this Design Document:

* resolves every Design Document audit finding,
* removes implementation-specific content (APIs, technology stack, database implementation, deployment, folder structure),
* adds the required architectural, component, sequence, interaction, and data flow diagrams,
* includes design rationale and textual wireframes,
* keeps the scope appropriate for a single-student 6–8 week Compiler Construction mini project, and
* remains consistent with the approved PRD.  

# Design Document

## 1. Cover Page

**Project Title**

# CompileDoctor – Intelligent Compiler Error Diagnosis & Recovery System

**Document**

Design Document

**Project Type**

Semester Mini Project

**Academic Discipline**

Compiler Construction

**Project Duration**

6–8 Weeks

**Project Category**

Educational Compiler Front-End

**Version**

2.0

---

# 2. Document Control

| Item              | Description                                                                                     |
| ----------------- | ----------------------------------------------------------------------------------------------- |
| Document Name     | Design Document                                                                                 |
| Project           | CompileDoctor                                                                                   |
| Version           | 2.0                                                                                             |
| Status            | Approved Design Baseline                                                                        |
| Prepared For      | Semester Mini Project                                                                           |
| Related Documents | Product Requirements Document (PRD), Technical Requirements Document (TRD), Implementation Plan |
| Scope             | System Design Only                                                                              |

---

# 3. Introduction

The Design Document describes the conceptual architecture and overall system design of CompileDoctor.

Unlike the Product Requirements Document, which defines **what** the system must achieve, this document explains **how the overall system is organized** from a design perspective without discussing implementation technologies.

The design emphasizes educational clarity by modelling the compiler as a sequence of well-defined phases:

* Lexer
* Parser
* AST Construction
* Semantic Analysis
* Diagnostics
* Error Recovery

Each phase is represented as an independent conceptual module, making the system easier to understand, maintain, and extend.

The design intentionally mirrors the compiler pipeline taught in Compiler Construction courses so that students can directly relate theoretical concepts to software components.

---

# 4. Purpose

The purpose of this document is to:

* describe the overall system architecture;
* explain interactions between major modules;
* present conceptual data movement throughout compilation;
* define navigation and user interaction;
* document important design decisions;
* provide visual models of the proposed system;
* establish a stable architectural reference for implementation.

This document does **not** define implementation technologies, APIs, deployment strategies, programming languages, or software libraries.

---

# 5. Design Goals

The system has been designed around the following goals.

## 5.1 Educational Clarity

Every compiler phase should be visible and understandable to learners.

The design prioritizes explanation over optimization.

---

## 5.2 Modular Architecture

Each compiler phase is represented as an independent module with a clearly defined responsibility.

This separation improves readability and simplifies future enhancement.

---

## 5.3 Progressive Processing

Source code flows through compiler phases in the same order taught academically.

This creates a natural learning experience.

---

## 5.4 Explainable Diagnostics

Errors should not only be detected but also explained in language suitable for beginners.

---

## 5.5 Recoverable Analysis

Where practical, the system should continue analysis after recoverable syntax errors so multiple diagnostics can be presented during one execution.

---

## 5.6 Maintainable Design

The architecture should allow future compiler phases to be incorporated without redesigning existing modules.

---

# 6. Research Summary

The design of CompileDoctor is informed by educational compiler research and compiler construction principles summarized in the project sources.

The research highlights several recurring observations:

* Beginner programmers struggle more with understanding compiler diagnostics than locating them.
* Traditional compiler messages are often too technical for novice learners.
* Visual representations of compiler phases improve conceptual understanding.
* Structured diagnostics significantly improve debugging efficiency.
* Error recovery enables learners to discover multiple issues within a single compilation rather than correcting one error at a time.
* Visualizing internal compiler structures such as ASTs and Symbol Tables reinforces classroom learning.

These findings directly influenced the design philosophy adopted throughout this document.

---

# 7. Similar Existing Systems

The purpose of this comparison is to identify the educational gap addressed by CompileDoctor.

| System                            | Strength                   | Limitation                   | CompileDoctor Contribution           |
| --------------------------------- | -------------------------- | ---------------------------- | ------------------------------------ |
| Traditional C Compiler            | Fast compilation           | Difficult error messages     | Beginner-oriented explanations       |
| Educational Parser Visualizers    | Good grammar visualization | Limited semantic analysis    | End-to-end compiler pipeline         |
| Online Code Editors               | Immediate syntax checking  | Minimal educational guidance | Compiler-phase explanations          |
| University Compiler Demonstrators | Academic demonstrations    | Limited interaction          | Interactive diagnostics and recovery |

CompileDoctor is not intended to replace existing compilers.

Instead, it functions as an educational layer that explains compiler behaviour.

---

# 8. High-Level System Architecture

The following diagram illustrates the conceptual architecture of CompileDoctor.

It emphasizes the separation between user interaction and compiler processing while avoiding implementation-specific details.

```mermaid
flowchart LR

User[User]

UI[User Interface]

Pipeline[Compiler Pipeline]

Lexer[Lexer]

Parser[Parser]

AST[AST Construction]

Semantic[Semantic Analysis]

Diagnostics[Diagnostics]

Recovery[Error Recovery]

Output[Results Presentation]

User --> UI

UI --> Pipeline

Pipeline --> Lexer

Lexer --> Parser

Parser --> AST

AST --> Semantic

Semantic --> Diagnostics

Diagnostics --> Recovery

Recovery --> Output

Output --> User
```

### Design Rationale

The architecture follows the natural progression of compiler phases.

Each module performs one primary responsibility before passing structured information to the next stage.

This improves understandability while preserving clear separation of concerns.

---

# 9. Component Diagram

The following component diagram illustrates the major logical components and their relationships.

```mermaid
flowchart TB

UI[User Interface]

Editor[Code Editor]

Visualizer[Visualization Module]

Compiler[Compiler Controller]

Lexer[Lexer]

Parser[Parser]

AST[AST Generator]

Semantic[Semantic Analyzer]

SymbolTable[Symbol Table]

Diagnostics[Diagnostics Engine]

Recovery[Error Recovery]

Results[Results View]

UI --> Editor

Editor --> Compiler

Compiler --> Lexer

Lexer --> Parser

Parser --> AST

AST --> Semantic

Semantic --> SymbolTable

Semantic --> Diagnostics

Diagnostics --> Recovery

Recovery --> Results

Results --> Visualizer
```

### Design Rationale

The architecture separates interaction, compiler processing, visualization, and presentation.

Each component owns one responsibility, making the overall design easier to understand and maintain.

---

# 10. Data Flow Diagram

The following Data Flow Diagram illustrates how information moves through the compiler pipeline.

```mermaid
flowchart LR

Source[Source Code]

Tokens[Token Stream]

Syntax[Syntax Structure]

ASTData[Abstract Syntax Tree]

Symbols[Symbol Table]

Diagnostics[Diagnostics]

Recovered[Recovered Analysis]

Output[User Output]

Source --> Tokens

Tokens --> Syntax

Syntax --> ASTData

ASTData --> Symbols

Symbols --> Diagnostics

Diagnostics --> Recovered

Recovered --> Output
```

### Design Rationale

Rather than moving executable data, the system transforms increasingly structured representations of the user's source code.

Each compiler phase enriches the information available for later diagnostics.

---

# 11. Sequence Diagram

The following sequence diagram demonstrates the interaction between the user and the conceptual compiler modules during a typical analysis.

```mermaid
sequenceDiagram

actor User

participant UI

participant Lexer

participant Parser

participant AST

participant Semantic

participant Diagnostics

participant Recovery

User->>UI: Submit source program

UI->>Lexer: Begin lexical analysis

Lexer->>Parser: Token stream

Parser->>AST: Build syntax structure

AST->>Semantic: Perform semantic analysis

Semantic->>Diagnostics: Report findings

Diagnostics->>Recovery: Attempt recovery if required

Recovery-->>UI: Analysis results

UI-->>User: Display diagnostics and visualizations
```

### Design Rationale

The sequence reflects the educational order of compiler execution rather than implementation timing.

Each participant represents one conceptual compiler phase.

---

# 12. Entity Relationship Diagram (Conceptual)

The following conceptual ER diagram illustrates the logical information handled by the system.

It is **not** intended to represent a database schema.

```mermaid
erDiagram

SOURCE_PROGRAM ||--o{ TOKEN : generates

SOURCE_PROGRAM ||--|| AST : produces

AST ||--o{ SYMBOL : contains

AST ||--o{ DIAGNOSTIC : generates

DIAGNOSTIC ||--o{ RECOVERY_ACTION : may_trigger
```

### Design Rationale

The entities represent educational compiler artifacts rather than persistent storage.

Their relationships illustrate how information evolves throughout compilation.

---

---

END OF PART 1

## Reply with **Continue** to generate Part 2.
