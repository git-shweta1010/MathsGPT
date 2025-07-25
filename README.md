
# 🧠 MathsGPT - Ask Anything, Solve Everything

MathsGPT is an intelligent math assistant and general knowledge helper powered by the **LLaMA 3** model via **Groq API** and enhanced with reasoning capabilities and tools like **Wikipedia** search. It provides detailed, step-by-step solutions to math problems and can also answer general queries using LangChain agents.

---

## 🚀 Features

* 🧮 **Math Problem Solving**: Step-by-step logical breakdown of math problems using custom reasoning prompts.
* 🌍 **General Knowledge**: Uses Wikipedia to fetch and respond to questions on current events or general topics.
* 🧠 **Multi-Tool Agent**: Combines LLM, Wikipedia search, and math reasoning with LangChain’s `initialize_agent`.
* 💬 **Chat Interface**: Interactive chat-like interface built with Streamlit.
* 🔐 **Secure API Input**: API key input via sidebar for user security.

---

## 🛠️ Tech Stack

* **[Streamlit](https://streamlit.io/)** – Frontend interface
* **[LangChain](https://www.langchain.com/)** – Agent orchestration
* **[Groq API](https://console.groq.com/)** – LLM inference using LLaMA 3
* **[WikipediaAPIWrapper](https://python.langchain.com/docs/integrations/tools/wikipedia/)** – General knowledge support
* **Python** – Core programming language

---

## 🧰 Installation

1. **Clone the repository**

   ```bash
   git clone https://github.com/your-username/MathsGPT.git
   cd MathsGPT
   ```

2. **Create a virtual environment (optional but recommended)**

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Create a `.env` file**

   ```bash
   touch .env
   ```

5. **Run the app**

   ```bash
   streamlit run app.py
   ```

---

## 🔑 Environment Variables

You can also use a `.env` file to store your Groq API key:

```env
GROQ_API_KEY=your_groq_api_key_here
```

> Alternatively, you can input it manually through the Streamlit sidebar.

---

## 📦 Required Libraries (`requirements.txt`)

```txt
streamlit
langchain
langchain-groq
python-dotenv
```

---

## 🧪 Example Queries

* `Solve: 2x + 3 = 11`
* `What is the capital of Sweden?`
* `Factorize: x^2 - 5x + 6`
* `Give me step-by-step solution of (3x+2)(2x-5)`

---

