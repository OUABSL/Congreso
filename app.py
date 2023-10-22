import os
import PyPDF2
import openai
from flask import Flask, redirect, render_template, request, url_for

app = Flask(__name__)

# Set your API key directly
os.environ["OPENAI_API_KEY"] = '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'
openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        # Leer el contenido del PDF cargado
        pdf_file = request.files["pdf_file"]
        title = request.form["title"]

        pdf_content = ""
        if pdf_file:
            pdf_reader = PyPDF2.PdfReader(pdf_file)
            for page_num in range(len(pdf_reader.pages)):
                page = pdf_reader.pages[page_num]
                pdf_content += page.extract_text()

        # Enviar el contenido del PDF a GPT-4 para resumirlo
        response = openai.ChatCompletion.create(
            model="gpt-4", 
            messages=[
                {"role": "system", "content": "un tutor de universidad 'Dpto. de Ciencias de la Computación e Inteligencia Artificial' ."},
                {"role": "user", "content": generate_prompt(pdf_content, title)},
            ]
        )

        # Obtener la respuesta completa de OpenAI
        result = response.choices[0].message["content"]

        return render_template("index.html", result=result)

    return render_template("index.html")

def generate_prompt(pdf_content, title):
    return f"""Resume el trabajo académico sobre {title}. 
     Deja claro todo lo importante. Quiero un resumen que mantiene el 50% del trabajo:\n\n{pdf_content}"""

if __name__ == "__main__":
    app.run(debug=True)
