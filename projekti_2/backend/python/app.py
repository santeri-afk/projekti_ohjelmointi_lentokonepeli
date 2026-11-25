import os
from flask import Flask, render_template
import peli

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
app = Flask(
    __name__, template_folder=os.path.join(BASE_DIR, "frontend", "Html")
)


@app.get("/")
def index():
  return render_template("index.html")

@app.get()

if __name__ == "__main__":
  app.run(host="127.0.0.1", port=5000, debug=True)