# CompileDoctor – Intelligent Compiler Error Diagnosis & Recovery System

> An educational compiler front-end that transforms compiler errors into beginner-friendly explanations while visualizing the compilation pipeline.

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![Flask](https://img.shields.io/badge/Flask-Web%20Framework-black)
![PLY](https://img.shields.io/badge/PLY-Lex%20%26%20Yacc-orange)
![License](https://img.shields.io/badge/License-MIT-green)
![Status](https://img.shields.io/badge/Status-Academic%20Mini%20Project-success)

---

# Problem Statement

Compiler error messages are often difficult for beginner programmers to understand. Traditional compilers typically report *what* went wrong but provide limited guidance on *why* the error occurred or *how* to resolve it.

CompileDoctor addresses this challenge by providing educational compiler diagnostics that explain compiler errors in simple language while visualizing each stage of the compilation process.

---

# Objectives

* Provide beginner-friendly compiler diagnostics.
* Demonstrate the major phases of compiler construction.
* Visualize compiler artifacts such as the Abstract Syntax Tree (AST) and Symbol Table.
* Detect lexical, syntax, and semantic errors.
* Support basic error recovery for educational purposes.
* Improve students' understanding of compiler internals through interactive learning.

---

# Features

* Source code editor
* Lexical Analysis (Tokenization)
* Syntax Analysis (Parsing)
* Abstract Syntax Tree (AST) Generation
* Symbol Table Generation
* Semantic Analysis
* Educational Compiler Diagnostics
* Error Recovery
* Compiler Pipeline Visualization
* Sample Programs for Demonstration

---

# System Architecture (Summary)

The system follows the traditional compiler front-end pipeline:

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
 Results & Visualization
```

The architecture is modular, allowing each compiler phase to operate independently while producing structured information for subsequent stages.

---

# Technology Stack

| Category             | Technology            |
| -------------------- | --------------------- |
| Programming Language | Python                |
| Backend              | Flask                 |
| Compiler Framework   | PLY (Python Lex-Yacc) |
| Frontend             | HTML, CSS, JavaScript |
| Visualization        | Graphviz              |
| Optional Storage     | SQLite                |
| Version Control      | Git                   |
| Documentation        | Markdown              |

---

# Project Structure

```text
CompileDoctor/
│
├── backend/
│   ├── lexer/
│   ├── parser/
│   ├── semantic/
│   ├── diagnostics/
│   ├── recovery/
│   ├── ast/
│   ├── symbol_table/
│   └── server/
│
├── frontend/
│   ├── editor/
│   ├── visualizer/
│   ├── components/
│   └── assets/
│
├── database/          # Optional persistence
├── examples/
├── tests/
├── documentation/
│
├── README.md
└── requirements.txt
```

---

# Installation

## Clone the Repository

```bash
git clone https://github.com/<your-username>/CompileDoctor.git
cd CompileDoctor
```

## Create a Virtual Environment

```bash
python -m venv venv
```

### Windows

```bash
venv\Scripts\activate
```

### Linux/macOS

```bash
source venv/bin/activate
```

## Install Dependencies

```bash
pip install -r requirements.txt
```

## Run the Application

```bash
python app.py
```

Open your browser and navigate to:

```text
http://localhost:5000
```

---

# Usage

1. Launch the application.
2. Enter or paste a program into the editor.
3. Click **Analyze**.
4. View:

   * Token Stream
   * Abstract Syntax Tree
   * Symbol Table
   * Compiler Diagnostics
   * Error Recovery Information
5. Correct the program and analyze again.

---

# Screenshots

> Replace these placeholders with actual project screenshots.

```text
docs/screenshots/home.png
docs/screenshots/tokenizer.png
docs/screenshots/ast.png
docs/screenshots/errors.png
docs/screenshots/symbol-table.png
```

---

# Future Scope

Potential future enhancements include:

* Parse Tree visualization
* Intermediate Representation (IR)
* Three-Address Code generation
* Compiler optimization demonstrations
* Multiple language support
* Interactive compiler visualizations
* IDE integration
* Enhanced educational diagnostics

---

# Documentation

Project documentation includes:

* Product Requirements Document (PRD)
* Design Document
* Technical Requirements Document (TRD)
* Implementation Plan

These documents describe the project requirements, architecture, technical implementation, and execution roadmap.

---

# Contributors

**Abhyudaya Aware**

*Computer Engineering Student*

Semester Mini Project — Compiler Construction

---

# License

This project is developed for academic and educational purposes.

You may choose to release it under the **MIT License** by adding an appropriate `LICENSE` file to the repository.

---

## Acknowledgements

* Compiler Construction course syllabus
* Faculty guidance and academic review
* Python PLY (Python Lex-Yacc) community
* Flask community
* Graphviz project

---

> **CompileDoctor** is designed to bridge the gap between compiler theory and practical learning by making compiler diagnostics more understandable, visual, and educational.
