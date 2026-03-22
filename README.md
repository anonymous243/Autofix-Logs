# 🚀 AutoFix Logs

![Python](https://img.shields.io/badge/Python-3.9+-blue)
![License](https://img.shields.io/badge/License-MIT-green)
![CLI](https://img.shields.io/badge/Tool-CLI-orange)
![Status](https://img.shields.io/badge/Status-Active-success)

**Open-source AI-powered CLI tool to analyze logs and suggest fixes instantly.**

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
pip install autofix-logs

or

pipx install autofix-logs
```

---

### Local Installation

```bash
git clone https://github.com/anonymous243/Autofix-Logs
cd Autofix-Logs
pip install .
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
autofix analyze <filename.log>
```

### ⚡ Quick mode

```bash
autofix analyze <filename.log> --quick
```
### 📊 Summary mode

```bash
autofix analyze <filename> --summary
```
### 👀 Watch logs in real-time
```bash
autofix watch <filename>
```

### 🧰 Check system setup
```bash
autofix doctor
```

### 📌 Version
```bash
autofix version
```
---

## 🧪 Example

### Input

```
autofix analyze <filename.log>
```

### Output

```
🚨 Error Detected

Type: ModuleNotFoundError
Confidence: High (100%)

💡 Cause:
The 'requests' package is not installed

📖 Explanation:
Python could not find the 'requests' module...

⚡ Fix Command:
pip install requests
```

---
## Demo

```CLI
```
<img width="718" height="362" alt="autofix" src="https://github.com/user-attachments/assets/1e29da93-c5c6-474b-bf3a-d2286ccb97a4" />

```Error detection
```
<img width="697" height="378" alt="autofix op" src="https://github.com/user-attachments/assets/26b8bb78-23f5-49d0-8404-9f619b02afe3" />



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

1. Extracts error blocks from logs
2. Filters noise and prioritizes real issues
3. Sends optimized input to AI
4. Returns structured fixes instantly

---

## 🔮 Roadmap

* 📡 Watch mode (real-time logs)
* Smarter error ranking
* 🧩 Multi-error detection
* 🐳 Docker support
* 📴 Offline AI models

---

## 🤝 Contributing
Contributions are welcome!

1. Fork repo
2. Create branch
3. Commit changes
4. Open PR

---

## 📜 License

[MIT License](LICENSE)

---

## 🌟 Support

⭐ Star the repo
🐛 Open issues
💡 Suggest features

---

## 👨‍💻 Author

Built by **Amar**

---
