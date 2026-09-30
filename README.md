# EduGenie — Google Gemini Powered Learning Assistant

EduGenie is a lightweight AI educational assistant based on the supplied project
documentation. It provides:

- Question answering
- Beginner-friendly concept explanations
- Three-question MCQ quiz generation
- Educational passage summarization
- Personalized learning paths

The original documentation specifies FastAPI, HTML/CSS, Gemini, and an optional
local LaMini-Flan-T5 explanation model. This implementation keeps those concepts
but uses Google's current `google-genai` Python SDK for Gemini access.

## 1. Requirements

- Python 3.10+
- VS Code
- A Google AI Studio Gemini API key

## 2. Create the environment

### Windows PowerShell

```powershell
cd EduGenie
py -3.10 -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
```

If PowerShell blocks activation, use Command Prompt:

```cmd
.venv\Scripts\activate.bat
```

### macOS/Linux

```bash
cd EduGenie
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
```

The default installation uses Gemini only. The optional local LaMini model has
separate dependencies so you do not need to install PyTorch just to run the app.

If you want local LaMini explanations:

```bash
pip install -r requirements-local.txt
```

## 3. Configure Gemini

Copy `.env.example` to `.env`.

Windows PowerShell:

```powershell
Copy-Item .env.example .env
```

macOS/Linux:

```bash
cp .env.example .env
```

Open `.env` and set:

```env
GEMINI_API_KEY=your_real_key
```

Do not commit `.env` to Git.

## 4. Run

```bash
uvicorn main:app --reload
```

Open:

http://127.0.0.1:8000

API documentation:

http://127.0.0.1:8000/docs

Health check:

http://127.0.0.1:8000/health

## 5. Test

Run the automated tests:

```bash
pytest
```

The tests cover the application page, health endpoint, validation, API route
behavior, and quiz response shape without consuming Gemini API calls.

## 6. API examples

### Q&A

```bash
curl -X POST http://127.0.0.1:8000/qa ^
  -H "Content-Type: application/json" ^
  -d "{\"text\":\"What is photosynthesis?\"}"
```

On macOS/Linux, use `\` instead of `^` for line continuation.

### Quiz

```bash
curl -X POST http://127.0.0.1:8000/quiz \
  -H "Content-Type: application/json" \
  -d '{"text":"The Pythagoras theorem relates the sides of a right triangle."}'
```

## 7. Optional local LaMini explanation model

The supplied documentation describes LaMini-Flan-T5-783M for concept
explanations. This project includes that capability as an optional path.

First install `requirements-local.txt`, then set:

```env
LOCAL_EXPLANATION_ENABLED=true
```

The first request may download the model from Hugging Face and requires more
RAM/disk than the normal Gemini-only configuration. If the local model cannot
load, the application automatically falls back to Gemini.

For the easiest first run, keep it:

```env
LOCAL_EXPLANATION_ENABLED=false
```

## 8. Project structure

```text
EduGenie/
├── main.py
├── config.py
├── models.py
├── gemini_client.py
├── utils.py
├── explanation_module.py
├── qna.py
├── quiz_module.py
├── summary_module.py
├── learning_path.py
├── requirements.txt
├── .env.example
├── .gitignore
├── pytest.ini
├── README.md
├── templates/
│   └── index.html
├── static/
│   ├── style.css
│   └── app.js
└── tests/
    ├── test_app.py
    └── test_utils.py
```

## 9. VS Code setup

1. Open the `EduGenie` folder in VS Code.
2. Install the Microsoft Python extension.
3. Open Terminal → New Terminal.
4. Create and activate `.venv`.
5. Run `pip install -r requirements.txt`.
6. Create `.env` from `.env.example`.
7. Add your Gemini API key.
8. Select `.venv` through `Python: Select Interpreter`.
9. Run `uvicorn main:app --reload`.
10. Open `http://127.0.0.1:8000`.

## 10. Troubleshooting

### "GEMINI_API_KEY is not configured"

Make sure `.env` exists in the project root and contains:

```env
GEMINI_API_KEY=...
```

Restart Uvicorn after changing `.env`.

### Gemini request errors

Check the API key, account/API access, model availability, network connection,
and the model name in `.env`.

### PowerShell activation error

Use Command Prompt and run:

```cmd
.venv\Scripts\activate.bat
```

or configure your PowerShell execution policy according to your organization's
security policy.

### Local model is slow

Set:

```env
LOCAL_EXPLANATION_ENABLED=false
```

The default Gemini path is considerably simpler to install.

## 11. Security notes

- Never put the Gemini API key in `static/app.js` or HTML.
- Never commit `.env`.
- Keep API keys server-side.
- For production, add authentication, rate limiting, logging/monitoring, HTTPS,
  and stronger request controls before exposing the service publicly.

## 12. Functional mapping to the supplied documentation

| Documentation feature | Implementation |
|---|---|
| Q&A | `/qa` → `qna.py` |
| Explanation | `/explain` → `explanation_module.py` |
| Quiz | `/quiz` → `quiz_module.py` |
| Summary | `/summarize` → `summary_module.py` |
| Learning path | `/learn/recommendations` → `learning_path.py` |
| HTML frontend | `templates/index.html` |
| CSS | `static/style.css` |
| FastAPI | `main.py` |
| Gemini | `gemini_client.py` |
| JSON cleanup | `utils.py` |
