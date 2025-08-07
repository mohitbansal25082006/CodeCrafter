# CodeCrafter

AI-Powered Code Generation Assistant

![CodeCrafter Logo](https://img.shields.io/badge/CodeCrafter-AI%20Powered-blue)

## Overview

CodeCrafter is a full-stack Generative AI-powered coding assistant designed to help developers generate, optimize, document, and review code. It uses Large Language Models (LLMs) integrated with LangChain agents, vector databases, and developer tools to deliver context-aware, high-quality coding solutions.

## Features

### Code Generation
- Convert natural language prompts into fully functional code
- Generate code with comments and docstrings
- Analyze time and space complexity

### Code Explanation
- Detailed line-by-line logic explanation
- Complexity analysis
- Use cases & edge cases identification

### Test Case Generation
- Automatically generate unit tests
- Support for multiple testing frameworks (pytest, unittest, Jest, JUnit)
- Boundary and edge case testing

### Code Snippet Storage
- Store reusable snippets in ChromaDB vector database
- Semantic search for previously generated code
- Metadata tracking (language, purpose, complexity)

### LangChain Agents
- **Bug Detection Agent**: Identify and fix bugs
- **Code Optimization Agent**: Improve performance, security, and readability
- **Documentation Agent**: Generate docstrings, comments, and markdown documentation

### GitHub Integration
- Analyze pull requests
- Generate AI-powered review comments
- Post comments directly to GitHub

## Technology Stack

- **Frontend**: Streamlit
- **Backend**: Python
- **LLM Integration**: OpenAI GPT-4 / LangChain
- **Vector Database**: ChromaDB
- **API Integration**: GitHub REST API

## Installation

### Local Development

1. Clone the repository:
```bash
git clone https://github.com/yourusername/codecrafter.git
cd codecrafter