import os
from PyPDF2 import PdfReader
import pyttsx3
from gtts import gTTS

# Çıktı dosyalarının kaydedileceği klasör
OUTPUT_FOLDER = 'static/downloads'
if not os.path.exists(OUTPUT_FOLDER):
    os.makedirs(OUTPUT_FOLDER)


def extract_text_from_pdf(pdf_path):
    """PDF dosyasındaki metni çıkarır."""
    reader = PdfReader(pdf_path)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text


def list_voice_options():
    """pyttsx3 için mevcut sesleri listeler."""
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    return [(index, voice.name) for index, voice in enumerate(voices)]


def text_to_speech_pyttsx3(text, voice_id=0, output_file="audiobook_pyttsx3.mp3"):
    """pyttsx3 ile TTS işlemi yapar."""
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[int(voice_id)].id)
    engine.setProperty('rate', 150)
    output_path = os.path.join(OUTPUT_FOLDER, output_file)
    engine.save_to_file(text, output_path)
    engine.runAndWait()
    return output_path


def text_to_speech_gtts(text, lang="en", output_file="audiobook_gtts.mp3"):
    """gTTS ile TTS işlemi yapar."""
    tts = gTTS(text=text, lang=lang)
    output_path = os.path.join(OUTPUT_FOLDER, output_file)
    tts.save(output_path)
    return output_path


def main():
    print("PDF to Audiobook Converter")
    pdf_path = input("PDF dosyasının yolunu girin: ")

    if not os.path.exists(pdf_path):
        print("Geçersiz dosya yolu. Lütfen doğru bir PDF dosyası yolu girin.")
        return

    text = extract_text_from_pdf(pdf_path)
    if not text:
        print("PDF'den metin çıkarılamadı. Geçersiz veya boş PDF dosyası.")
        return

    print("\nSeslendirme motoru seçin:")
    print("1. pyttsx3 (Çevrimdışı)")
    print("2. gTTS (Çevrimiçi)")
    engine_choice = input("Seçiminiz (1 veya 2): ")

    output_file = ""

    if engine_choice == "1":
        # pyttsx3 motoru için ses seçimi
        voices = list_voice_options()
        print("\nMevcut sesler:")
        for idx, voice_name in voices:
            print(f"{idx}: {voice_name}")

        voice_id = input("Ses ID'sini seçin: ")
        if not voice_id.isdigit() or int(voice_id) >= len(voices):
            print("Geçersiz ses ID'si seçildi.")
            return

        output_file = text_to_speech_pyttsx3(text, voice_id=int(voice_id))

    elif engine_choice == "2":
        # gTTS motoru için dil seçimi
        lang = input("Dil kodunu girin (örneğin, 'en' İngilizce, 'tr' Türkçe): ")
        output_file = text_to_speech_gtts(text, lang=lang)

    else:
        print("Geçersiz seslendirme motoru seçimi.")
        return

    print(f"Sesli kitap oluşturuldu: {output_file}")


if __name__ == "__main__":
    main()
