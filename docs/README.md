---
layout: home
permalink: index.html

repository-name: e20-4yp-Automated-Code-Smell-Detection-and-Refactoring-with-LLMs
title: SmellSense AI
---

![SmellSense AI](images/logo.png)

## Team

- E/20/062, K.S. Dhananji, [email](mailto:e20062@eng.pdn.ac.lk)
- E/20/367, Binuri Senavirathna, [email](mailto:e20367@eng.pdn.ac.lk)
- E/20/350, J.P.D.N. Sandamali, [email](mailto:e20350@eng.pdn.ac.lk)

### Supervisors

- Mr. Biswajith Dissanayake — Lecturer (Prob)
- Mr. Thilina Gunarathne — Lecturer (Prob)

---

## Table of Contents

1. [Introduction](#introduction)
2. [Research Problem](#research-problem)
3. [Objectives](#objectives)
4. [Proposed Solution](#proposed-solution)
5. [System Architecture](#system-architecture)
6. [Methodology](#methodology)
7. [Detection & Analysis Module](#detection--analysis-module)
8. [Refactoring Module](#refactoring-module)
9. [Results](#results)
10. [Impact & Limitations](#impact--limitations)
11. [Future Work](#future-work)
12. [Getting Started](#getting-started)
13. [Outputs](#outputs)
14. [Links](#links)

---

## Introduction

Modern software systems continue to grow rapidly in size and complexity. As projects evolve, maintaining clean and understandable code becomes increasingly difficult. Poor coding practices often introduce **code smells**, which are indicators of deeper structural and maintainability problems in software systems. Refactoring helps improve software quality by restructuring code without changing its external behavior.

SmellSense AI is a research-based intelligent system designed to automatically detect, explain, prioritize, and refactor code smells using a hybrid combination of:

- Static analysis
- Software metrics
- Machine learning techniques
- Large Language Models (LLMs)

The system provides an end-to-end workflow that assists developers in improving code quality and maintainability through intelligent automated refactoring.

---

## Research Problem

Manual code smell detection is often time-consuming, inconsistent, and difficult to scale across large projects. Traditional static analysis tools are mainly rule-based and usually lack explanation capabilities and severity analysis. Existing solutions also fail to provide a complete end-to-end workflow from detection to automated refactoring.

Although LLMs can generate refactoring suggestions, they often suffer from:

- Inconsistent outputs
- Invalid or unverified refactoring
- Lack of structured prioritization

SmellSense AI addresses these limitations through a hybrid intelligent pipeline.

---

## Objectives

The main objectives of the project are:

- Detect code smells using multiple detection engines
- Explain detected smells and assess their severity
- Automatically generate safe refactoring solutions
- Provide a complete end-to-end workflow for developers

---

## Proposed Solution

SmellSense AI introduces a fully integrated LLM-powered pipeline that:

- Detects up to 30 different code smells
- Automatically explains detected smells
- Prioritizes smells based on severity
- Generates automated refactoring suggestions
- Provides an interactive chatbot interface for developers

---

## System Architecture

The system consists of several integrated components working together to provide intelligent code analysis and refactoring support.

### Main Components

- **Frontend Chatbot Interface**
  - Upload or paste source code
  - Display detected smells and refactored output

- **Backend API Server**
  - Request routing
  - Session management
  - Pipeline orchestration

- **Feature Extraction Engine**
  - Extracts metrics such as:
    - CBO
    - LCOM
    - OOP metrics

- **Detection Engines**
  - Static analysis engine
  - Metric-based analysis
  - LLM-based semantic analysis

- **Refactoring Engine**
  - Strategy selection
  - Smell-aware refactoring generation
  - Validation and repair pipeline

---

## Methodology

![Methodology](images/methodology.png)

The project methodology consists of four major stages.

### 1. Data Acquisition

![Data Acquisition](images/dataAquisition.png)

The dataset preparation pipeline includes:

- Downloading source datasets
- Extracting and cleaning source code
- Mining Java projects from GitHub
- Recovering software metrics using static analysis tools
- Preparing datasets for ML training and LLM contextualization

### 2. Code Smell Detection

![Code Smell Detection](images/smellDetection.png)

The detection pipeline includes:

- Feature extraction
- Static analysis
- Regex parsing
- Metrics analysis
- AI-based semantic analysis

The system combines multiple engines to improve detection quality and coverage.

### 3. Smell Explanation & Prioritization

![Smell Explanation & Prioritization](images/prioritization.png)

Detected smells are processed through an LLM-based explanation engine which:

- Generates human-readable explanations
- Predicts severity levels
- Assigns priority scores
- Produces ranked smell lists

### 4. Automated Refactoring

![Automated Refactoring](images/refactoring.png)

The refactoring pipeline includes:

- Refactoring decision engine
- Smell-to-strategy mapping
- Prompt engineering
- Validation and repair mechanisms
- Compilation and syntax validation

### 5. Model Evaluation

![Model Evaluation](images/modelEvaluation.png)

Evaluation focuses on:

- Detection accuracy
- Severity assessment quality
- Refactoring validation
- Runtime performance
- End-to-end workflow efficiency

### 6. Chatbot Development

![Chatbot Development](images/deployChatbot.png)

The chatbot interface allows developers to:

- Upload or paste source code
- View detected smells with explanations
- See severity scores and rankings
- Access generated refactored code

---

## Detection & Analysis Module

### Features

- Multi-engine smell detection
- Parallel processing pipeline
- Context-aware AI explanations
- Severity prediction and prioritization
- Structured JSON outputs

### Detection Output

Generated output file:

```text
data/priority_list.json
```
