---
layout: home
permalink: index.html

repository-name: e20-4yp-Automated-Code-Smell-Detection-and-Refactoring-with-LLMs
title: Automated Code Smell Detection and Refactoring with LLMs
---

# SmellSense AI - Automated Code Smell Detection and Refactoring with LLMs

![SmellSense AI](images/logo.png)

## Team

- E/20/062, Dhananji K.S., [email](mailto:e20062@eng.pdn.ac.lk)
- E/20/357, Senavirathna D.B.C.M., [email](mailto:e20367@eng.pdn.ac.lk)
- E/20/350, Sandamali J.P.D.N., [email](mailto:e20350@eng.pdn.ac.lk)

#### Table of Contents

1. [Introduction](#introduction)
2. [Solution Architecture](#solution-architecture)
3. [Detection & Analysis Module](#detection--analysis-module)
4. [Refactoring Module](#refactoring-module-llm-based)
5. [Key Features](#key-features)
6. [Getting Started](#getting-started)
7. [Outputs](#outputs)
8. [Project Goal](#project-goal)
9. [Links](#links)

---

## Introduction

SmellSense AI is a research-based intelligent software engineering system designed to automatically detect, analyze, prioritize, and refactor code smells using a combination of static analysis techniques, software metrics, and Large Language Models (LLMs).

The system aims to improve software maintainability and code quality by identifying problematic code patterns and generating intelligent refactoring suggestions. By combining traditional software engineering techniques with AI-driven analysis, SmellSense AI provides developers with context-aware insights and automated improvements for cleaner and more maintainable codebases.

---

## Solution Architecture

![High level diagram](images/HighLevelArchitecture.jpg)

The architecture consists of multiple integrated components that work together to provide an end-to-end automated code smell detection and refactoring pipeline.

- **Frontend Interface** – Provides an interactive UI for developers to upload projects, analyze code smells, and review refactoring suggestions.
- **Backend API Service** – Handles detection requests, orchestrates analysis pipelines, and communicates with LLM-based refactoring modules.
- **Detection Engine** – Uses static analysis, software metrics, and AI-assisted detection methods to identify code smells.
- **LLM Refactoring Engine** – Generates intelligent refactoring solutions based on detected smells and validation feedback.
- **Output Management System** – Stores prioritized smells and refactoring outputs in structured JSON files.

### Workflow

- User submits source code through the frontend interface.
- Detection engines analyze the codebase using static analysis, metrics, and LLM-assisted evaluation.
- Detected smells are prioritized and stored in a structured format.
- The refactoring engine selects appropriate refactoring strategies using a smell catalog.
- Generated refactored code is validated and repaired automatically if necessary.
- Final outputs and recommendations are presented to the user.

---

## Detection & Analysis Module

### Features

- Multi-engine detection (Static Analysis + Metrics + LLM-based analysis)
- Parallel processing pipeline for faster analysis
- Context-aware AI-generated explanations
- Prioritized code smell generation

### Output

Generated prioritized smell list:

```text
data/priority_list.json
```
