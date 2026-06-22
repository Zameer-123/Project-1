from flask import Flask, render_template, request
import traceback
from groq import Groq

app = Flask(__name__)

# Initialize Groq client (replace with your actual API key)
client = Groq(api_key="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")

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/analyze", methods=["POST"])
def analyze():
    code = request.form["code"]
    try:
        exec(code)
        error = None
        explanation = "No errors found."
    except Exception:
        error = traceback.format_exc()

        # Send error + code to Groq AI model
        prompt = f"Explain the bug in this Python code:\n\n{code}\n\nError:\n{error}"
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",  # Groq model
            messages=[{"role": "user", "content": prompt}]
        )
        explanation = response.choices[0].message.content

    return render_template("index.html", error=error, explanation=explanation)

if __name__ == "__main__":
    app.run(debug=True)