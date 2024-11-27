import fitz  # PyMuPDF
import pyttsx3
from pathlib import Path
from tqdm import tqdm
import os


def extract_text_from_pdf(pdf_path):
    """PDF dosyasından tüm metni çıkarır."""
    full_text = ""
    try:
        with fitz.open(pdf_path) as pdf:
            total_pages = pdf.page_count
            for page_num in tqdm(range(total_pages), desc="Sayfa çıkarılıyor", unit="sayfa"):
                page = pdf.load_page(page_num)
                text = page.get_text("text")  # Sayfa metnini çıkar
                full_text += text
    except Exception as e:
        print(f"PDF işlenirken bir hata oluştu: {e}")
    return full_text


def split_text_into_chunks(text, chunk_size=1000):
    """Uzun metni küçük parçalara böler."""
    words = text.split()
    num_chunks = len(words) // chunk_size + (1 if len(words) % chunk_size != 0 else 0)
    for i in tqdm(range(num_chunks), desc="Metin parçalara ayrılıyor", unit="parça"):
        yield " ".join(words[i * chunk_size:(i + 1) * chunk_size])


def text_to_speech_pyttsx3(text_chunks, output_file):
    """Metin parçalarını ses dosyasına dönüştürür."""
    engine = pyttsx3.init()
    engine.setProperty("rate", 150)  # Konuşma hızı ayarı

    try:
        for idx, chunk in enumerate(tqdm(text_chunks, desc="Ses dosyaları oluşturuluyor", unit="parça")):
            output_file_part = output_file.parent / f"{output_file.stem}_part_{idx + 1}.mp3"
            print(f"Parça {idx + 1} işleniyor ve kaydediliyor: {output_file_part}")
            engine.save_to_file(chunk, str(output_file_part))
            engine.runAndWait()
    except Exception as e:
        print(f"Ses dosyası oluşturulurken hata oluştu: {e}")


def process_pdf_to_audio(pdf_path):
    """PDF'den metin çıkarır ve her 30-40 sayfa için bir ses dosyası oluşturur."""
    print("PDF'den metin çıkarılıyor...")
    full_text = extract_text_from_pdf(pdf_path)

    if not full_text.strip():
        print("Hiç metin çıkartılamadı. PDF dosyası okunabilir metin içermiyor olabilir.")
        return

    # PDF dosyasının adını al ve klasör oluştur
    pdf_filename = Path(pdf_path).stem  # PDF dosyasının ismini uzantısız al
    output_dir = Path(os.path.expanduser("~/Desktop")) / pdf_filename  # Kitap ismine göre klasör
    output_dir.mkdir(parents=True, exist_ok=True)  # Klasörü oluştur (varsa hata vermez)

    # Metin parçalara ayrılıyor
    print("Metin parçalara ayrılıyor...")
    text_chunks = list(split_text_into_chunks(full_text, chunk_size=9000))  # 9000 kelimeye göre parçala

    # Her parça için ayrı ses dosyası oluştur
    print("Ses dosyaları oluşturuluyor...")
    output_file = output_dir / pdf_filename
    text_to_speech_pyttsx3(text_chunks, output_file)

    print(f"Tüm ses dosyaları '{output_dir}' dizinine kaydedildi.")


if __name__ == "__main__":
    pdf_path = input("PDF dosyasının yolunu girin: ").strip()

    if not os.path.exists(pdf_path):
        print("Belirtilen PDF dosyası mevcut değil. Çıkılıyor.")
    else:
        process_pdf_to_audio(pdf_path)
