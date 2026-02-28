<div align="center">

# VEXIS-1.1

[![Python](https://img.shields.io/badge/Python-3.9%2B-blue?style=flat-square&logo=python)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)](LICENSE)
[![Status](https://img.shields.io/badge/Status-Experimental-orange?style=flat-square)]()

**Your AI agent that watches your screen and automates everything**

[Features](#features) • [Installation](#installation) • [Usage](#usage) • [Requirements](#requirements)

</div>

---

## About

**VEXIS-1.1** is a personal AI desktop agent that observes your screen in real-time to make decisions and automate operations on your OS. Whether it's clicking buttons, filling forms, browsing the web, or managing files, just describe what you want and let the AI handle it.

Powered by [Google's Gemini 3](https://deepmind.google/technologies/gemini/) for intelligent decision-making.

> **Note:** This is an experimental project. It works great for many tasks but may surprise you sometimes. Use with curiosity!

---

## Features

- **Screen-based decision making** - Analyzes screenshots to understand context
- **Full OS control** - Mouse clicks, keyboard input, app interactions
- **Web automation** - Search, fill forms, navigate sites automatically  
- **File operations** - Create, move, organize files and folders
- **One-liner execution** - Simple command: `python3 run.py "do something"`

---

## Requirements

| Requirement | Details |
|----------|---------|
| **Python** | 3.9 or higher |
| **OS** | Windows, macOS, or Linux |
| **API Key** | Gemini 3 series (get from [Google AI Studio](https://aistudio.google.com)) |
| **Optional** | ollama account for Gemini 3 Flash cloud model |

---

## Installation

```bash
# Clone the repository
git clone https://github.com/AInohogosya/VEXIS-1.1.git
cd VEXIS-1.1

# Install dependencies (optional but recommended)
pip install -r requirements.txt
