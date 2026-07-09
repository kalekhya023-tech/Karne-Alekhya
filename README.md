#Karne-Alekhya
# 🎓 AI Learning Buddy

An AI-powered web app that helps students learn any topic instantly. Type in a subject, choose what you want — a simple explanation, a real-life example, a quiz, or a free-form answer — and Google's Gemini AI generates it live in the browser.

## What It Does

AI Learning Buddy takes any topic a student enters and, based on the selected activity, generates:

- **Explain Concept** — a beginner-friendly explanation of the topic
- **Real-Life Example** — a simple real-world example to build intuition
- **Generate Quiz** — 5 multiple-choice questions with answers for self-testing
- **Ask Anything** — an open-ended Q&A mode for any question

## Tech Stack

| Tool | Role |
|---|---|
| **Streamlit** | Turns the Python script into an interactive web UI (text input, dropdown, button) with no HTML/JS |
| **Google Gemini API** (`gemini-2.5-flash`) | Generates the explanations, examples, and quizzes |
| **Google Colab** | Cloud environment used to write and run the app — no local installation required |
| **ngrok** | Creates a public URL to expose the app running inside Colab so it can be opened in any browser |

## How It Works

1. The user enters a topic and selects an activity from a dropdown.
2. On clicking **Generate**, the app builds a tailored prompt based on the selected activity.
3. The prompt is sent to Gemini via `model.generate_content(prompt)`.
4. Gemini's response is displayed directly on the page.

## Running It Yourself

1. Open the notebook in Google Colab.
2. Install dependencies:
```python
   !pip install -q streamlit pyngrok google-generativeai
```
3. Add your own Gemini API key (get one free at [aistudio.google.com/app/apikey](https://aistudio.google.com/app/apikey)) — for security, store it using Colab Secrets rather than hardcoding it:
```python
   from google.colab import userdata
   api_key = userdata.get('GEMINI_API_KEY')
   genai.configure(api_key=api_key)
```
4. Run the app in the background:
```python
   !nohup streamlit run app.py --server.port 8501 &
```
5. Expose it publicly with ngrok (requires a free [ngrok](https://ngrok.com) account and auth token):
```python
   from pyngrok import ngrok
   ngrok.set_auth_token("YOUR_NGROK_AUTH_TOKEN")
   public_url = ngrok.connect(8501)
   print(public_url)
```
6. Open the printed link to use the app.

## Notes

- The free Gemini API tier has a rate limit (a few requests per minute) — if you hit a `429 ResourceExhausted` error, just wait ~30–60 seconds and retry.
- Colab + ngrok sessions are temporary — the public link changes each time `ngrok.connect()` is rerun, and the app stops once the Colab runtime disconnects.
- Never commit real API keys to version control — use environment variables or Colab Secrets instead.

## What This Project Demonstrates

- Integrating a live LLM API (Google Gemini) into a functional application
- Rapid prototyping and deployment using Streamlit
- Debugging real-world deployment issues (indentation errors, API rate limits, tunneling)
- End-to-end thinking from local script to publicly accessible web app
