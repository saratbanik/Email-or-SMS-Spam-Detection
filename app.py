import streamlit as st
import pickle
import nltk
import string
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Email / SMS Spam Classifier",
    page_icon="SC",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# ── Inline CSS (no external files needed) ────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&family=Source+Serif+4:wght@600&display=swap');

:root {
    --navy:       #0D2B4E;
    --navy-mid:   #163D6B;
    --navy-light: #1F5290;
    --gold:       #C89A3A;
    --gold-light: #F0C060;
    --white:      #FFFFFF;
    --off-white:  #F5F6F8;
    --border:     #D6DBE4;
    --text-main:  #0D1B2E;
    --text-muted: #4A5568;
    --spam-red:   #B91C1C;
    --spam-bg:    #FEF2F2;
    --ham-green:  #166534;
    --ham-bg:     #F0FDF4;
    --warn-amber: #92400E;
    --warn-bg:    #FFFBEB;
    --radius:     6px;
}

html, body, [data-testid="stAppViewContainer"] {
    background-color: var(--off-white) !important;
    font-family: 'Inter', sans-serif;
    color: var(--text-main);
}
[data-testid="stMain"] { background-color: var(--off-white) !important; }
#MainMenu, footer, header { visibility: hidden; }
[data-testid="stToolbar"]    { display: none; }
[data-testid="stDecoration"] { display: none; }
[data-testid="stMainBlockContainer"] {
    max-width: 780px !important;
    padding: 0 1.5rem 3rem !important;
    margin: 0 auto !important;
}

/* Header */
.site-header {
    background: var(--navy);
    margin: 0 -1.5rem 0 -1.5rem;
    padding: 0 1.5rem;
    border-bottom: 3px solid var(--gold);
}
.header-inner {
    max-width: 780px;
    margin: 0 auto;
    padding: 1rem 0;
    display: flex;
    align-items: center;
    justify-content: space-between;
}
.header-brand { display: flex; align-items: center; gap: 0.75rem; }
.brand-mark {
    width: 42px; height: 42px;
    background: var(--gold); color: var(--navy);
    display: flex; align-items: center; justify-content: center;
    font-size: 14px; font-weight: 700; letter-spacing: 0.5px;
    border-radius: 4px; flex-shrink: 0;
}
.brand-title { font-size: 16px; font-weight: 600; color: var(--white); letter-spacing: 0.3px; }
.brand-sub   { font-size: 11px; color: #93B5D8; margin-top: 1px; letter-spacing: 0.2px; }
.header-badge {
    font-size: 11px; font-weight: 500; color: var(--gold-light);
    border: 1px solid var(--gold); border-radius: 3px;
    padding: 3px 10px; letter-spacing: 0.8px; text-transform: uppercase;
}

/* Hero */
.hero-section { padding: 2.25rem 0 1.5rem; }
.hero-title {
    font-family: 'Source Serif 4', serif;
    font-size: 26px; font-weight: 600;
    color: var(--navy); margin: 0 0 0.75rem 0; line-height: 1.3;
}
.hero-desc { font-size: 14.5px; color: var(--text-muted); line-height: 1.75; margin: 0; max-width: 680px; }

/* Divider */
.divider { height: 1px; background: var(--border); margin: 1.5rem 0; }

/* Input label */
.input-label {
    font-size: 12px; font-weight: 600; letter-spacing: 0.8px;
    text-transform: uppercase; color: var(--navy-light); margin: 0 0 0.5rem 0;
}

/* Textarea */
[data-testid="stTextArea"] textarea {
    background: var(--white) !important;
    border: 1.5px solid var(--border) !important;
    border-radius: var(--radius) !important;
    font-size: 14px !important;
    font-family: 'Inter', sans-serif !important;
    color: var(--text-main) !important;
    line-height: 1.65 !important;
    resize: vertical !important;
    transition: border-color 0.15s ease !important;
}
[data-testid="stTextArea"] textarea:focus {
    border-color: var(--navy-light) !important;
    box-shadow: 0 0 0 3px rgba(31,82,144,0.12) !important;
    outline: none !important;
}

/* Button */
[data-testid="stButton"] button[kind="primary"] {
    background: var(--navy) !important;
    color: var(--white) !important;
    border: none !important;
    border-radius: var(--radius) !important;
    font-size: 13px !important; font-weight: 600 !important;
    letter-spacing: 0.6px !important; text-transform: uppercase !important;
    padding: 0.6rem 2rem !important;
    transition: background 0.15s ease !important;
    font-family: 'Inter', sans-serif !important;
}
[data-testid="stButton"] button[kind="primary"]:hover  { background: var(--navy-light) !important; }
[data-testid="stButton"] button[kind="primary"]:active { background: var(--navy-mid)   !important; }

/* Alert */
.alert { border-radius: var(--radius); font-size: 13.5px; padding: 0.75rem 1rem; margin-top: 1rem; line-height: 1.6; }
.alert-warning { background: var(--warn-bg); border: 1px solid #FDE68A; color: var(--warn-amber); }

/* Result card */
.result-card {
    border-radius: var(--radius); padding: 1.25rem 1.5rem; margin-top: 1.25rem;
    display: flex; align-items: center; justify-content: space-between;
    border-width: 1px; border-style: solid;
}
.result-spam { background: var(--spam-bg); border-color: #FCA5A5; }
.result-ham  { background: var(--ham-bg);  border-color: #86EFAC; }
.result-verdict { font-size: 15px; font-weight: 600; letter-spacing: 0.5px; }
.result-spam .result-verdict { color: var(--spam-red);   }
.result-ham  .result-verdict { color: var(--ham-green);  }
.result-conf { font-size: 13px; font-weight: 500; }
.result-spam .result-conf { color: #991B1B; }
.result-ham  .result-conf { color: #14532D; }

/* Stat cards */
.detail-row { margin-top: 0.75rem; }
.stat-card { background: var(--white); border: 1px solid var(--border); border-radius: var(--radius); padding: 0.9rem 1.1rem; }
.stat-label { font-size: 11px; font-weight: 600; letter-spacing: 0.7px; text-transform: uppercase; color: var(--text-muted); margin-bottom: 4px; }
.stat-value { font-size: 22px; font-weight: 600; color: var(--navy); }

/* Expander */
[data-testid="stExpander"] {
    background: var(--white) !important;
    border: 1px solid var(--border) !important;
    border-radius: var(--radius) !important;
    margin-top: 0.75rem !important;
}
[data-testid="stExpander"] summary { font-size: 13px !important; font-weight: 500 !important; color: var(--navy-light) !important; }
.token-text {
    font-size: 13px; color: var(--text-muted);
    font-family: 'Courier New', monospace;
    background: var(--off-white); border-radius: 4px;
    padding: 0.6rem 0.8rem; word-break: break-all; line-height: 1.6; margin: 0;
}

/* Model strip */
.model-strip {
    display: grid; grid-template-columns: repeat(auto-fit, minmax(170px, 1fr));
    gap: 0; background: var(--white);
    border: 1px solid var(--border); border-radius: var(--radius); overflow: hidden;
}
.model-item { padding: 0.9rem 1rem; border-right: 1px solid var(--border); display: flex; flex-direction: column; gap: 4px; }
.model-item:last-child { border-right: none; }
.model-key { font-size: 10px; font-weight: 700; letter-spacing: 0.9px; text-transform: uppercase; color: var(--gold); }
.model-val { font-size: 12px; color: var(--text-main); font-weight: 500; line-height: 1.4; }

/* Footer */
.site-footer {
    text-align: center; font-size: 13px; color: var(--text-muted);
    padding: 1.5rem 0 0.5rem; border-top: 1px solid var(--border); margin-top: 2rem;
}
.site-footer a {
    color: var(--navy-light); font-weight: 600; text-decoration: none;
    border-bottom: 1px solid var(--gold); padding-bottom: 1px; transition: color 0.15s;
}
.site-footer a:hover { color: var(--gold); }

@media (max-width: 520px) {
    .model-strip { grid-template-columns: 1fr 1fr; }
    .model-item:nth-child(2) { border-right: none; }
    .model-item:nth-child(1), .model-item:nth-child(2) { border-bottom: 1px solid var(--border); }
    .hero-title { font-size: 22px; }
}
</style>
""", unsafe_allow_html=True)

# ── NLTK bootstrap ────────────────────────────────────────────────────────────
@st.cache_resource(show_spinner=False)
def download_nltk():
    for res, kind in [("punkt", "tokenizers"), ("punkt_tab", "tokenizers"), ("stopwords", "corpora")]:
        try:
            nltk.data.find(f"{kind}/{res}")
        except LookupError:
            nltk.download(res, quiet=True)

download_nltk()

ps = PorterStemmer()

def transform_text(text: str) -> str:
    text = text.lower()
    tokens = nltk.word_tokenize(text)
    tokens = [t for t in tokens if t.isalnum()]
    stop_words = set(stopwords.words("english"))
    tokens = [t for t in tokens if t not in stop_words and t not in string.punctuation]
    tokens = [ps.stem(t) for t in tokens]
    return " ".join(tokens)

@st.cache_resource(show_spinner=False)
def load_model():
    tfidf = pickle.load(open("vectorizer.pkl", "rb"))
    model = pickle.load(open("model.pkl",      "rb"))
    return tfidf, model

tfidf, model = load_model()

# ── Header ────────────────────────────────────────────────────────────────────
st.markdown("""
<header class="site-header">
    <div class="header-inner">
        <div class="header-brand">
            <span class="brand-mark">SC</span>
            <div>
                <div class="brand-title">Spam Classifier</div>
                <div class="brand-sub">Natural Language Processing &middot; Machine Learning</div>
            </div>
        </div>
        <div class="header-badge">Academic Project</div>
    </div>
</header>
""", unsafe_allow_html=True)

# ── Hero ──────────────────────────────────────────────────────────────────────
st.markdown("""
<section class="hero-section">
    <h1 class="hero-title">Email / SMS Spam Detection</h1>
    <p class="hero-desc">
        This system applies a Multinomial Naive Bayes classifier trained on TF-IDF features
        to determine whether a given message is spam or legitimate (ham).
        Enter any message in the field below and submit for classification.
    </p>
</section>
""", unsafe_allow_html=True)

st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

# ── Input ─────────────────────────────────────────────────────────────────────
st.markdown('<p class="input-label">Message Input</p>', unsafe_allow_html=True)

input_msg = st.text_area(
    label="",
    placeholder="Paste or type an email or SMS message here...",
    height=160,
    key="message_input",
    label_visibility="collapsed",
)

col1, col2, col3 = st.columns([2, 1, 2])
with col2:
    predict_btn = st.button("Classify", use_container_width=True, type="primary")

# ── Result ────────────────────────────────────────────────────────────────────
if predict_btn:
    if not input_msg.strip():
        st.markdown("""
        <div class="alert alert-warning">
            No message was provided. Please enter a message before submitting.
        </div>""", unsafe_allow_html=True)
    else:
        transformed = transform_text(input_msg)
        vector      = tfidf.transform([transformed])
        result      = model.predict(vector)[0]
        proba       = model.predict_proba(vector)[0]

        spam_pct = round(proba[1] * 100, 1)
        ham_pct  = round(proba[0] * 100, 1)

        if result == 1:
            st.markdown(f"""
            <div class="result-card result-spam">
                <div class="result-verdict">SPAM DETECTED</div>
                <div class="result-conf">Confidence: {spam_pct}%</div>
            </div>""", unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="result-card result-ham">
                <div class="result-verdict">LEGITIMATE MESSAGE</div>
                <div class="result-conf">Confidence: {ham_pct}%</div>
            </div>""", unsafe_allow_html=True)

        col_a, col_b = st.columns(2)
        with col_a:
            st.markdown(f"""
            <div class="stat-card">
                <div class="stat-label">Spam Probability</div>
                <div class="stat-value">{spam_pct}%</div>
            </div>""", unsafe_allow_html=True)
        with col_b:
            st.markdown(f"""
            <div class="stat-card">
                <div class="stat-label">Ham Probability</div>
                <div class="stat-value">{ham_pct}%</div>
            </div>""", unsafe_allow_html=True)

        with st.expander("Preprocessed Tokens"):
            st.markdown(f"""
            <p class="token-text">{transformed if transformed else "(no tokens after preprocessing)"}</p>
            """, unsafe_allow_html=True)

# ── Model info strip ──────────────────────────────────────────────────────────
st.markdown('<div class="divider" style="margin-top:2.5rem;"></div>', unsafe_allow_html=True)
st.markdown("""
<section class="model-strip">
    <div class="model-item"><span class="model-key">Algorithm</span><span class="model-val">Multinomial Naive Bayes</span></div>
    <div class="model-item"><span class="model-key">Vectorizer</span><span class="model-val">TF-IDF (max 3,000 features)</span></div>
    <div class="model-item"><span class="model-key">Dataset</span><span class="model-val">UCI SMS Spam Collection</span></div>
    <div class="model-item"><span class="model-key">Preprocessing</span><span class="model-val">Tokenization &middot; Stopword Removal &middot; Stemming</span></div>
</section>
""", unsafe_allow_html=True)

# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown("""
<footer class="site-footer">
    Developed by <a href="https://www.linkedin.com/in/saratbanik" target="_blank" rel="noopener">Sarat Banik</a>
</footer>
""", unsafe_allow_html=True)
