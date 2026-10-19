<<<<<<< HEAD
# Email / SMS Spam Classifier

A Streamlit web application that classifies messages as Spam or Legitimate (Ham)
using a Multinomial Naive Bayes model trained on TF-IDF features.

---

## Project Structure

```
spam_detector/
├── app.py                   Main Streamlit application
├── model.pkl                Pre-trained MultinomialNB classifier
├── vectorizer.pkl           Pre-fitted TF-IDF vectorizer
├── requirements.txt         Python dependencies
├── .gitignore
├── README.md
└── assets/
    ├── style.css            Custom theme stylesheet
    └── favicon.png          Browser tab icon
```

---

## How to Run in VS Code (localhost)

### Step 1 — Open the project folder in VS Code

```
File → Open Folder → select the spam_detector folder
```

### Step 2 — Open the integrated terminal

```
View → Terminal   (or press  Ctrl + ` )
```

### Step 3 — Create a virtual environment

Windows (PowerShell):
```powershell
python -m venv venv
venv\Scripts\Activate.ps1
```

macOS / Linux:
```bash
python3 -m venv venv
source venv/bin/activate
```

You should see (venv) at the start of your terminal prompt.

### Step 4 — Install dependencies

```bash
pip install -r requirements.txt
```

IMPORTANT: requirements.txt pins scikit-learn==1.3.0 because the .pkl model
files were saved with that version. Using a different version may cause errors.

### Step 5 — Run the application

```bash
streamlit run app.py
```

Streamlit will print a URL in the terminal:

  Local URL:  http://localhost:8501

Open that address in your browser.

---

## Deploying to Streamlit Cloud (free public URL)

1. Push the project to a GitHub repository (public or private).
2. Go to https://share.streamlit.io and sign in with GitHub.
3. Click "New app" and select your repository and branch.
4. Set the main file path to: app.py
5. Click "Deploy". Your app will be live at a public URL in a few minutes.

---

## Troubleshooting

| Error | Solution |
|---|---|
| ModuleNotFoundError: streamlit | Activate the venv and run pip install -r requirements.txt |
| FileNotFoundError: vectorizer.pkl | Ensure model.pkl and vectorizer.pkl are in the same folder as app.py |
| NLTK LookupError | The app downloads punkt and stopwords automatically on first run |
| scikit-learn version warning | Pin with: pip install scikit-learn==1.3.0 |
| PowerShell execution policy error | Run: Set-ExecutionPolicy -Scope CurrentUser RemoteSigned |

---

Developed by Sarat Banik — https://www.linkedin.com/in/saratbanik
=======
# Email-or-SMS-Spam-Detection
An NLP-powered web app that classifies email and SMS messages as spam or legitimate using a Multinomial Naive Bayes classifier trained on TF-IDF features.
