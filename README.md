# 📋 SOP → AI Training System

An AI-powered web application that converts any Standard Operating Procedure (SOP) into structured training content instantly.

## 🚀 Live Demo
[Click here to try the app](https://sop-ai-training-system.streamlit.app)

## 🎯 Problem Statement
Built for **Nutrabay AI Automation Intern Assessment — Problem 4: SOP → AI Training System**

## ✨ Features
- **Structured Summary** — Purpose, scope, and key points extracted automatically
- **Step-by-step Training Content** — Each step with description and action checklist
- **Evaluation Quiz** — 4 auto-generated questions with answers
- **Export** — Download full training package as .txt file

## 🖥️ How to Use
1. Get a free API key at [console.groq.com](https://console.groq.com)
2. Paste any SOP document (or load the sample)
3. Click "Generate Training Content"
4. Browse Summary → Training Content → Quiz tabs
5. Download the training package

## 🛠️ Tech Stack
- Python
- Streamlit
- Groq API (LLaMA 3.1)
- Requests

## ⚙️ Run Locally
```bash
git clone https://github.com/sonu-kumar-singh-lpu/sop-ai-training-system
cd sop-ai-training-system
pip install streamlit requests
streamlit run app.py
```

## 📁 Project Structure
```
sop-ai-training-system/
├── app.py            # Main application
├── requirements.txt  # Dependencies
└── README.md         # Project description
```
