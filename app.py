from flask import Flask, render_template, request
import pickle
import re

app = Flask(__name__)

# Load model and vectorizer
with open("model/fake_news_model.pkl", "rb") as f:
    model, vectorizer = pickle.load(f)

# Text cleaner
def clean_text(text):
    return re.sub(r'[^a-zA-Z\s]', '', text.lower())

@app.route("/", methods=["GET", "POST"])
def index():
    prediction = ""
    if request.method == "POST":
        input_text = request.form["news"]
        cleaned = clean_text(input_text)
        vect_text = vectorizer.transform([cleaned])
        result = model.predict(vect_text)[0]
        prediction = "🟢 Real News" if result == 1 else "🔴 Fake News"
    return render_template("index.html", prediction=prediction)

if __name__ == "__main__":
    app.run(debug=True)
