import os
from flask import Flask, request, render_template, send_file, redirect, url_for
from PyPDF2 import PdfReader
import pyttsx3
from gtts import gTTS

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/downloads'


def extract_text_from_pdf(pdf_path):
    reader = PdfReader(pdf_path)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text


def list_voice_options():
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    return [(index, voice.name) for index, voice in enumerate(voices)]


def text_to_speech_pyttsx3(text, voice_id=0, output_file="static/downloads/audiobook_pyttsx3.mp3"):
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[int(voice_id)].id)
    engine.setProperty('rate', 150)
    engine.save_to_file(text, output_file)
    engine.runAndWait()
    return output_file


def text_to_speech_gtts(text, lang="en", output_file="static/downloads/audiobook_gtts.mp3"):
    tts = gTTS(text=text, lang=lang)
    tts.save(output_file)
    return output_file


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        # Dosya yükleme ve seçenekleri alma
        pdf_file = request.files["pdf_file"]
        engine_choice = request.form["engine_choice"]

        if not pdf_file:
            return "PDF dosyası yüklenmedi", 400

        pdf_path = os.path.join(app.config['UPLOAD_FOLDER'], pdf_file.filename)
        pdf_file.save(pdf_path)

        text = extract_text_from_pdf(pdf_path)

        # Seçilen TTS motoruna göre işleme
        if engine_choice == "pyttsx3":
            voice_id = int(request.form["voice_id"])
            output_file = text_to_speech_pyttsx3(text, voice_id=voice_id)
        elif engine_choice == "gTTS":
            lang = request.form["lang"]
            output_file = text_to_speech_gtts(text, lang=lang)
        else:
            return "Geçersiz seslendirme motoru", 400

        return redirect(url_for("download_file", filename=os.path.basename(output_file)))

    voices = list_voice_options()
    return render_template("index.html", voices=voices)


@app.route("/download/<filename>")
def download_file(filename):
    return send_file(os.path.join(app.config['UPLOAD_FOLDER'], filename), as_attachment=True)


if __name__ == "__main__":
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])
    app.run(debug=True, port=5001)
