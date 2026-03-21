# 🚀 AutoFix Logs

![Python](https://img.shields.io/badge/Python-3.9+-blue)
![License](https://img.shields.io/badge/License-MIT-green)
![CLI](https://img.shields.io/badge/Tool-CLI-orange)
![Status](https://img.shields.io/badge/Status-Active-success)

**AI-powered CLI tool to analyze logs and suggest fixes instantly.**

AutoFix Logs helps developers quickly understand errors from logs by providing structured explanations, root causes, and exact fix commands — directly in your terminal.

---

## ✨ Features

* 🔍 **Smart Log Parsing** – Extracts meaningful error segments from logs
* 🧠 **AI-Powered Analysis** – Uses Gemini AI for root cause detection
* ⚡ **Instant Fix Suggestions** – Provides exact commands to resolve issues
* 💻 **CLI-Based Workflow** – Works directly in your terminal
* 🔐 **Secure** – Uses environment variables for API keys

---

## 📦 Installation

### Install from GitHub

```bash
pip install git+https://github.com/anonymous243/Autofix-Logs.git
```

---

### Local Installation

```bash
git clone https://github.com/anonymous243/Autofix-Logs.git
cd Autofix-Logs
pip install -e .
```

---

## 🔐 Setup

Create a `.env` file:

```env
GEMINI_API_KEY=your_api_key_here
```

---

## 🚀 Usage

```bash
autofix analyze app.log
```

### Quick Mode

```bash
autofix analyze app.log --quick
```

---

## 🧪 Example

### Input

```
ModuleNotFoundError: No module named 'requests'
```

### Output

```
Error Type: ModuleNotFoundError
Fix: pip install requests
```

---

## 📁 Project Structure

```
autofix/
├── cli.py
├── main.py
├── parser.py
├── extractor.py
├── ai.py
├── formatter.py
├── watcher.py
├── utils.py
├── config.py
└── __init__.py
```

---

## ⚙️ Requirements

* Python 3.9+
* Internet connection

---

## 🧠 How It Works

1. Reads log file
2. Extracts error segments
3. Sends to AI (Gemini)
4. Parses structured JSON
5. Displays formatted output

---

## 🔮 Roadmap

* 📡 Watch mode (real-time logs)
* 🧩 Multi-error detection
* 🌐 Web dashboard (SaaS)
* 🐳 Docker support
* 📴 Offline AI models

---

## 🤝 Contributing

1. Fork repo
2. Create branch
3. Commit changes
4. Open PR

---

## 📜 License

MIT License

---

## 🌟 Support

⭐ Star the repo
🐛 Open issues
💡 Suggest features

---

## 👨‍💻 Author

Built by **Amar**

---

## 🔥 Vision

To become a **developer-first AI debugging assistant** integrated into real-world workflows.

---
