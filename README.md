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
