# User Guide

**Project:** CompileDoctor – Intelligent Compiler Error Diagnosis & Recovery System

**Version:** 1.0

**Audience**
- Students
- Faculty
- Teaching Assistants
- Project Evaluators

---

# Table of Contents

1. Introduction
2. System Requirements
3. Installation
4. Launching the Application
5. User Interface Overview
6. Using CompileDoctor
7. Understanding Compiler Outputs
8. Example Workflow
9. Troubleshooting
10. Frequently Asked Questions
11. Best Practices
12. Limitations
13. Future Enhancements
14. Contact

---

# 1. Introduction

CompileDoctor is an educational compiler front-end designed to help students understand compiler errors through clear explanations and visual representations of the compilation process.

Unlike traditional compilers that simply report errors, CompileDoctor explains:

- What the error is
- Where it occurred
- Which compiler phase detected it
- Why it occurred
- How it can be corrected

The application also visualizes compiler artifacts such as the Abstract Syntax Tree (AST) and Symbol Table to reinforce Compiler Construction concepts.

---

# 2. System Requirements

## Minimum Requirements

| Component | Requirement |
|-----------|-------------|
| Operating System | Windows, Linux, or macOS |
| Python | 3.10 or later |
| RAM | 8 GB |
| Storage | 200 MB free space |
| Browser | Chrome, Edge, Firefox |

---

# 3. Installation

## Step 1

Clone the repository.

```bash
git clone https://github.com/yourusername/CompileDoctor.git
```

---

## Step 2

Navigate to the project.

```bash
cd CompileDoctor
```

---

## Step 3

Create a virtual environment.

```bash
python -m venv venv
```

---

## Step 4

Activate the environment.

### Windows

```bash
venv\Scripts\activate
```

### Linux / macOS

```bash
source venv/bin/activate
```

---

## Step 5

Install dependencies.

```bash
pip install -r requirements.txt
```

---

## Step 6

Run the application.

```bash
python app.py
```

Open:

```
http://localhost:5000
```

---

# 4. Launching the Application

After starting the application, the home page opens in the browser.

The interface contains:

- Source Code Editor
- Analyze Button
- Compiler Pipeline
- Token Viewer
- AST Viewer
- Symbol Table
- Diagnostics Panel

---

# 5. User Interface Overview

## Source Code Editor

Used to enter or paste a program for analysis.

---

## Analyze Button

Starts the compilation process.

---

## Compiler Pipeline

Displays the active compiler phases:

```
Lexer
↓

Parser
↓

AST

↓

Semantic Analysis

↓

Diagnostics

↓

Error Recovery
```

---

## Diagnostics Panel

Displays compiler messages.

Each message includes:

- Error Type
- Compiler Phase
- Line Number
- Description
- Suggested Correction

---

## AST Viewer

Displays the generated Abstract Syntax Tree for syntactically valid programs.

---

## Symbol Table

Displays declared identifiers together with their associated information.

---

# 6. Using CompileDoctor

## Step 1

Launch the application.

---

## Step 2

Enter source code into the editor.

Example:

```c
int main() {
    int a = 10;
    return 0;
}
```

---

## Step 3

Click **Analyze**.

---

## Step 4

Review the generated:

- Tokens
- AST
- Symbol Table
- Diagnostics

---

## Step 5

Correct reported errors.

---

## Step 6

Analyze again until the program is error-free.

---

# 7. Understanding Compiler Outputs

## Token Stream

Shows how the lexer converts source code into tokens.

Example:

```
KEYWORD
IDENTIFIER
OPERATOR
NUMBER
DELIMITER
```

---

## Abstract Syntax Tree

Represents the logical program structure.

The AST removes unnecessary grammar symbols while preserving semantic meaning.

---

## Symbol Table

Stores information about declared identifiers.

Typical information includes:

- Name
- Type
- Scope

---

## Diagnostics

Diagnostics contain:

- Compiler phase
- Error category
- Error location
- Explanation
- Suggested correction

---

## Error Recovery

If supported, the compiler continues analysis after certain syntax errors so that multiple issues can be reported during a single execution.

---

# 8. Example Workflow

### Source Code

```c
int main()
{
    int x
    y = 5;

    return 0;
}
```

---

### Compiler Processing

```
Lexer

↓

Parser

↓

AST

↓

Semantic Analysis

↓

Diagnostics
```

---

### Generated Diagnostics

```
Syntax Error

Missing ';'

Line 3

Suggested Fix

Insert ';'
```

```
Semantic Error

Undeclared Identifier

Variable: y

Suggested Fix

Declare y before use.
```

---

The corrected program can then be analyzed again.

---

# 9. Troubleshooting

## Application does not start

Verify:

- Python is installed.
- Dependencies are installed.
- Virtual environment is activated.

---

## AST is not displayed

Possible reasons:

- Syntax errors prevented AST generation.
- Graphviz is unavailable.
- Parser terminated early.

---

## No diagnostics appear

Verify that the Analyze button was pressed and valid source code was entered.

---

# 10. Frequently Asked Questions

### Does CompileDoctor generate executable code?

No.

It focuses on compiler front-end concepts.

---

### Does it support multiple programming languages?

No.

The current version targets a simplified educational language.

---

### Can it optimize code?

No.

Optimization is outside the project scope.

---

### Is it intended to replace a production compiler?

No.

It is an educational learning tool.

---

# 11. Best Practices

- Start with small programs.
- Fix lexical errors before syntax errors.
- Resolve syntax errors before semantic errors.
- Observe the AST after every successful parse.
- Study the Symbol Table to understand identifier management.
- Read the explanations rather than only the suggested fixes.

---

# 12. Limitations

Current limitations include:

- Compiler front-end only
- Single source program analysis
- Simplified educational grammar
- Static AST visualization
- Limited error recovery strategies

These limitations are intentional and align with the educational scope of the project.

---

# 13. Future Enhancements

Future versions may include:

- Parse Tree visualization
- Multiple language support
- Intermediate Representation (IR)
- Code optimization demonstrations
- Interactive AST exploration
- IDE integration
- Enhanced diagnostics

---

# 14. Contact

For questions regarding the project, please contact the project developer through the associated GitHub repository or academic supervisor.

---

# Appendix A – Compiler Pipeline Summary

| Phase | Purpose |
|---------|---------|
| Lexer | Converts source code into tokens |
| Parser | Validates grammar |
| AST | Represents program structure |
| Semantic Analysis | Checks semantic correctness |
| Diagnostics | Generates educational compiler messages |
| Error Recovery | Continues analysis after supported syntax errors |

---

# Appendix B – Recommended Learning Order

Students new to compiler construction are encouraged to explore CompileDoctor in the following sequence:

1. Learn tokenization.
2. Study grammar validation.
3. Observe the Abstract Syntax Tree.
4. Understand the Symbol Table.
5. Explore semantic analysis.
6. Interpret compiler diagnostics.
7. Examine error recovery behaviour.

Following this progression provides a structured understanding of how a compiler processes source code from raw text to meaningful diagnostics.