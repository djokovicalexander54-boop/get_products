from google import genai
key_gemini = "AQ.Ab8RN6LE1xYxM_ocOW91pnCs-7ZTrYwsQw1cK2WVQKn3SpsXdA"
gemini_ai = genai.Client(api_key=key_gemini)
#pdf_file_A = gemini_ai.files.upload(file=MM)
responce = gemini_ai.models.generate_content( 
    model = f"gemini-3.5-flash", 
    contents=["HELLO"]
)
print(responce.text, flush=True)
