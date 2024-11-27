import time
from concurrent.futures import ThreadPoolExecutor
import fitz  # PyMuPDF
from gtts import gTTS
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


def split_text_into_chunks(text, chunk_size=20000):
    """Uzun metni büyük parçalara böler."""
    words = text.split()
    num_chunks = len(words) // chunk_size + (1 if len(words) % chunk_size != 0 else 0)
    for i in tqdm(range(num_chunks), desc="Metin parçalara ayrılıyor", unit="parça"):
        yield " ".join(words[i * chunk_size:(i + 1) * chunk_size])


def generate_audio(text_chunk, output_path, lang="en"):
    """Bir metin parçasını MP3 dosyasına dönüştürür."""
    tts = gTTS(text=text_chunk, lang=lang)
    tts.save(output_path)
    # 1 saniye bekleme ekleyin
    time.sleep(1)


def process_chunks_in_parallel(chunks, output_dir, lang="en"):
    """Parçaları paralel olarak işler ve her istek arasında bekleme süresi ekler."""
    with ThreadPoolExecutor() as executor:
        futures = []
        for idx, chunk in enumerate(tqdm(chunks, desc="Ses dosyaları oluşturuluyor", unit="parça")):
            output_path = output_dir / f"part_{idx + 1}.mp3"
            futures.append(executor.submit(generate_audio, chunk, output_path, lang))
            # Her 3 parçadan sonra 3 saniye bekle
            if (idx + 1) % 3 == 0:
                time.sleep(3)  # Bu bekleme süresi API isteği limitini aşmamayı sağlar
        for future in futures:
            future.result()


def process_pdf_to_audio(pdf_path):
    """PDF'den metin çıkarır ve her 20.000 kelime için bir ses dosyası oluşturur."""
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
    text_chunks = list(split_text_into_chunks(full_text, chunk_size=20000))  # 20.000 kelimeye göre parçala

    # Parçaları paralel işleyerek ses dosyalarını oluştur
    print("\nSes dosyaları oluşturuluyor...")
    process_chunks_in_parallel(text_chunks, output_dir, lang="en")

    print(f"Tüm ses dosyaları '{output_dir}' dizinine kaydedildi.")


if __name__ == "__main__":
    pdf_path = input("PDF dosyasının yolunu girin: ").strip()

    if not os.path.exists(pdf_path):
        print("Belirtilen PDF dosyası mevcut değil. Çıkılıyor.")
    else:
        process_pdf_to_audio(pdf_path)
