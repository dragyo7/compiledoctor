# Product Requirements Document (PRD)

## Project Title

**CompileDoctor – Intelligent Compiler Error Diagnosis & Recovery System**

---

# 1. Introduction

## 1.1 Purpose

CompileDoctor is an educational web-based application that helps students understand compiler errors through clear explanations, structured diagnostics, and visualization of the compiler pipeline.

Instead of displaying only traditional compiler messages, the system explains:

* what error occurred,
* why it occurred,
* where it occurred,
* which compiler phase detected it,
* and how the user can correct it.

The product is intended as a semester mini project for the Compiler Construction course and is designed to reinforce compiler concepts through interactive learning.

---

## 1.2 Problem Statement

Compiler error messages are often technical and difficult for beginner programmers to understand.

Students frequently spend significant time identifying:

* the actual cause of an error,
* the compiler phase responsible,
* and the appropriate correction.

This slows learning and reduces confidence while studying compiler construction.

CompileDoctor addresses this problem by converting compiler diagnostics into beginner-friendly explanations while illustrating the compilation process.

---

## 1.3 Project Objectives

The project aims to:

* Help students understand compiler errors.
* Demonstrate major compiler phases taught in the syllabus.
* Provide meaningful diagnostics instead of cryptic compiler messages.
* Visualize important compiler data structures.
* Support learning through recoverable error analysis.
* Reduce debugging time for beginners.

---

# 2. Product Vision

CompileDoctor serves as an educational assistant that bridges the gap between compiler theory and practical programming.

The system focuses on learning rather than compilation speed or production-level compilation.

---

# 3. Target Users

The intended users are:

* Compiler Construction students
* Beginner programmers
* Laboratory instructors
* Teaching assistants
* Faculty demonstrating compiler concepts

---

# 4. User Personas

## Persona 1 — Alice (Computer Engineering Student)

Alice is a third-year Computer Engineering student learning Compiler Construction.

She understands basic programming but struggles to interpret compiler errors.

She wants simple explanations that help her understand both the mistake and the compiler concept behind it.

---

## Persona 2 — Bob (Teaching Assistant)

Bob assists laboratory sessions.

He needs a demonstration tool that visually explains compiler phases and helps students understand syntax and semantic errors during practical sessions.

---

# 5. Product Scope

## In Scope (MVP)

The system shall provide:

* Source code input
* Lexical analysis
* Syntax analysis
* AST generation
* Symbol table generation
* Basic semantic analysis
* Compiler diagnostics
* Error recovery
* Educational error explanations
* Compiler pipeline visualization

---

## Optional Features

These features may be implemented if time permits:

* Parse Tree visualization
* Saving analysis history
* Example programs
* Additional visualization improvements

These features are not mandatory for successful project completion.

---

## Future Scope

The following enhancements are outside the semester project scope:

* Support for additional programming languages
* Intermediate code generation
* Code optimization
* Machine code generation
* IDE integration
* AI-assisted error suggestions
* Collaborative learning features

---

# 6. Functional Requirements

## FR-1 Source Code Input

The system shall allow users to enter or paste source code for analysis.

---

## FR-2 Lexical Analysis

The system shall:

* identify tokens,
* classify token types,
* detect lexical errors,
* report the location of lexical errors.

---

## FR-3 Syntax Analysis

The system shall:

* validate grammar rules,
* detect syntax errors,
* identify the location of syntax errors,
* continue analysis using supported recovery techniques whenever possible.

---

## FR-4 Abstract Syntax Tree

The system shall generate an Abstract Syntax Tree (AST) for syntactically valid program structures.

The AST is intended to help users understand program structure rather than represent executable output.

---

## FR-5 Symbol Table

The system shall maintain a symbol table containing declared identifiers and their associated information throughout compilation.

---

## FR-6 Semantic Analysis

The system shall detect common semantic errors including:

* undeclared identifiers,
* redeclarations,
* incompatible assignments,
* basic type mismatches.

---

## FR-7 Compiler Diagnostics

For every detected error, the system shall provide:

* compiler phase,
* error category,
* error location,
* explanation,
* probable cause,
* suggested correction.

---

## FR-8 Error Recovery

The system shall attempt to continue analysis after recoverable syntax errors so that multiple errors can be reported during a single analysis.

---

## FR-9 Compiler Pipeline Visualization

The system shall present the major compiler phases so users can understand where processing is currently occurring.

The visualization is educational and intended to reinforce compiler theory.

---

## FR-10 Educational Feedback

The system shall provide beginner-friendly explanations that simplify compiler terminology without changing its meaning.

---

# 7. Non-Functional Requirements

## Performance

* Analysis should complete within approximately two seconds for typical laboratory programs.

---

## Reliability

* Invalid input shall not cause unexpected application failure.
* Recoverable errors should not terminate analysis immediately.

---

## Usability

The interface should:

* be easy to understand,
* require minimal training,
* clearly distinguish compiler phases,
* present diagnostics in readable language.

---

## Maintainability

The product should be organized so future compiler phases and diagnostics can be extended without major redesign.

---

## Portability

The application should be usable through a standard web browser.

---

# 8. User Stories

### US-1

As a student,

I want to submit my source code,

so that I can identify compiler errors.

---

### US-2

As a beginner,

I want understandable explanations,

so that I can learn why an error occurred.

---

### US-3

As a student,

I want to view compiler phases,

so that I understand how compilation works.

---

### US-4

As a teaching assistant,

I want visual compiler outputs,

so that I can demonstrate compiler concepts during laboratory sessions.

---

### US-5

As a learner,

I want the compiler to continue after recoverable errors,

so that I can discover multiple problems in one analysis.

---

# 9. Product Features

## MVP Features

* Source code editor
* Lexical analysis
* Syntax analysis
* Abstract Syntax Tree
* Symbol table
* Semantic analysis
* Compiler diagnostics
* Error recovery
* Educational explanations
* Compiler pipeline visualization

---

## Optional Features

* Parse Tree visualization
* Sample programs
* Session history
* Additional educational examples

---

## Future Enhancements

* Multi-language support
* Intermediate code generation
* Optimization demonstrations
* IDE integration
* Intelligent recommendation engine

---

# 10. Assumptions

* The project targets a simplified educational programming language.
* Programs are analyzed individually.
* The system focuses on compiler front-end concepts.
* The project duration is approximately 6–8 weeks.
* The application is intended primarily for educational use.

---

# 11. Constraints

* Single-student implementation.
* Semester mini project.
* Must align with Compiler Construction syllabus.
* Scope must remain practical and demonstrable.
* Emphasis is on educational value rather than production compiler capabilities.

---

# 12. Success Criteria

The project will be considered successful if it can:

* identify lexical, syntax, and semantic errors,
* generate understandable compiler diagnostics,
* demonstrate the compiler pipeline,
* generate an AST,
* generate a symbol table,
* recover from supported syntax errors,
* assist beginners in understanding compiler behaviour.

---

# 13. Acceptance Criteria

The product shall be accepted when:

1. Source code can be analyzed successfully.

2. Lexical errors are identified correctly.

3. Syntax errors are reported with meaningful explanations.

4. Semantic errors are detected correctly.

5. The AST is generated for valid program structures.

6. The symbol table is generated correctly.

7. Multiple recoverable syntax errors can be reported during one analysis where applicable.

8. Compiler diagnostics include:

   * compiler phase,
   * error category,
   * location,
   * explanation,
   * suggested correction.

9. The compiler pipeline is presented to the user in an educational manner.

10. The overall product demonstrates the compiler concepts required by the Compiler Construction syllabus.


