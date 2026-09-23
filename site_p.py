from google import genai
import time
from flask import Flask
import os
import threading
app = Flask(__name__)
@app.route("/")
def home():
    return "run"
def bb():
    m=1
    key_gemini = "AQ.Ab8RN6LE1xYxM_ocOW91pnCs-7ZTrYwsQw1cK2WVQKn3SpsXdA"
    gemini_ai = genai.Client(api_key=key_gemini)
    #pdf_file_A = gemini_ai.files.upload(file=MM)
    while True:
        try:
            responce = gemini_ai.models.generate_content( 
                model = f"gemini-2.5-flash", 
                contents=["HELLO"]
            )
            print(responce.text, flush=True)
            break
        except:
            time.sleep(2)
            print(f"NO {m}")
            m+=1
if __name__ == '__main__':
    threading.Thread(target=bb, daemon=True).start()
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
