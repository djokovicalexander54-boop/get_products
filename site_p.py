from google import genai
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
    #pdf_file_A = gemini_ai.files.upload(file=MM)
    while True:
        try:
            key = os.getenv("key_gemini")
            gemini_ai = genai.Client(api_key=key)
            #pdf_file_A = gemini_ai.files.upload(file=MM)
            responce = gemini_ai.models.generate_content( 
                model = f"gemini-3.5-flash", 
                contents=["HELLO"]
            )
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
