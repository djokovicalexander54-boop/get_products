import google.generativeai as genai
from flask import Flask
import time
import os
import threading
app = Flask(__name__)
@app.route("/")
def home():
    return "run"
def bb():
    m=1
    key_gemini = "AQ.Ab8RN6LE1xYxM_ocOW91pnCs-7ZTrYwsQw1cK2WVQKn3SpsXdA"
    genai.configure(api_key=key_gemini)
    #pdf_file_A = gemini_ai.files.upload(file=MM)
    model = genai.GenerativeModel("gemini-1.5-flash")
    while True:
        try:
            responce = model.generate_content("HELLO")
            print(responce.text, flush=True)
            break
        except Exception as e:
            print(str(e), flush=True)
            time.sleep(2)
            print(f"NO {m}", flush=True)
            m+=1
if __name__ == '__main__':
    threading.Thread(target=bb, daemon=True).start()
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
