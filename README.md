# VEXIS-1.1

**VEXIS-1.1** is a desktop AI agent that observes your screen to make decisions and automate operations on your OS (app interactions, file operations, browser actions, etc.).  
It can be configured to use Google's latest model, *Gemini 3*, as its base model.

---

## Features

- Decision-making and operations based on screen captures
- Supports mouse operations and keyboard input
- Automates browser and application operations
- Executable with a single command line (format: `python3 run.py "command"`)

---

## Requirements

- Python 3.9 or higher
- OS: Windows / macOS / Desktop Linux
- API key (required when using Gemini 3 series models)
- ollama account (required when running Gemini 3 Flash as a cloud model)

---

## Installation

```bash
git clone https://github.com/AInohogosya/VEXIS-1.1.git
cd VEXIS-1.1
````

---

## Usage

```bash
python run.py "Natural language instructions for desired actions"
```

The AI will perform actions while viewing the screen.

---

## Capabilities

* Web search and auto-fill
* Folder and file operations
* Basic operations in various applications

> ※ Results may vary depending on usage and environment.

---

## Precautions

* Currently experimental; potential for incorrect operations.
* Use only after thorough verification for critical tasks.

---

## Author

AInohogosya
