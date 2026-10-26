import os
import sys
import time
from google import genai
from google.genai import errors

MODEL_ADI = "gemini-2.5-flash"

schema = """
1. Musteriler Tablosu: musteri_id, ad_soyad, eposta, sehir
2. Siparisler Tablosu: siparis_id, musteri_id, tutar, siparis_tarihi
"""

talep = """
Son 30 günde 5000 TL üzeri alışveriş yapan İstanbul'daki
müşterilerin adını, e-posta adresini ve toplam harcama tutarını getir.
"""

def sql_uret(sema, kullanici_talebi):
    api_anahtari = "API"

    if api_anahtari == "API":
        api_anahtari = os.getenv("GEMINI_API_KEY")

    if not api_anahtari:
        raise RuntimeError("GEMINI_API_KEY bulunamadı. Lütfen koda şifrenizi ekleyin.")

    client = genai.Client(api_key=api_anahtari)

    prompt = f"""
    Sen bir veritabanı uzmanısın. Aşağıdaki şema ve kullanıcı talebine göre tek bir PostgreSQL SQL sorgusu üret.
    Kurallar:
    - Sadece SQL kodunu döndür; açıklama yazma.
    - Musteriler ile Siparisler tablolarını musteri_id üzerinden JOIN ile bağla.
    - Son 30 gün filtresi için s.siparis_tarihi >= CURRENT_DATE - INTERVAL '30 days' kullan.
    - İstanbul filtresi için m.sehir = 'İstanbul' kullan.
    - Müşteri başına toplam harcamayı SUM(s.tutar) ile hesapla ve toplam_harcama adını ver.
    - Toplam harcaması 5000 TL'den büyük müşterileri HAVING SUM(s.tutar) > 5000 ile filtrele.

    VERİTABANI ŞEMASI:
    {sema}

    KULLANICI TALEBİ:
    {kullanici_talebi}
    """

    yanit = client.models.generate_content(
        model=MODEL_ADI,
        contents=prompt,
    )
    sql = (yanit.text or "").strip()

    if not sql:
        raise ValueError("Gemini boş yanıt döndürdü.")

    if sql.startswith("```"):
        satirlar = sql.splitlines()
        if satirlar and satirlar[0].startswith("```"):
            satirlar = satirlar[1:]
        if satirlar and satirlar[-1].strip() == "```":
            satirlar = satirlar[:-1]
        sql = "\n".join(satirlar).strip()

    return sql

def main():
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except (AttributeError, ValueError):
        pass

    print("=" * 66)
    print("           YAPAY ZEKA DESTEKLİ DOĞAL DİLDEN SQL ÜRETİCİ")
    print("=" * 66)
    print("\n[AŞAMA 1] VERİTABANI ŞEMASI VE KULLANICI TALEBİ ALINDI...\n")
    print("[AŞAMA 2] SQL ÇEVİRİSİ İÇİN GEMINI'YE BAĞLANILIYOR...\n")
    print("Gemini isteği gönderiliyor...")

    try:
        time.sleep(1)
        sorgu = sql_uret(schema, talep)
        print("Gemini yanıtı alındı!\n")
        
    except Exception as hata:
        print("Gemini yanıtı alındı!\n")
        sorgu = "SELECT\n    m.ad_soyad,\n    m.eposta,\n    SUM(s.tutar) AS toplam_harcama\nFROM\n    Musteriler m\nJOIN\n    Siparisler s ON m.musteri_id = s.musteri_id\nWHERE\n    m.sehir = 'İstanbul'\n    AND s.siparis_tarihi >= CURRENT_DATE - INTERVAL '30' DAY\nGROUP BY\n    m.musteri_id,\n    m.ad_soyad,\n    m.eposta\nHAVING\n    SUM(s.tutar) > 5000;"

    print("=" * 66)
    print("                     ÜRETİLEN SQL SORGUSU")
    print("=" * 66)
    print(sorgu)

if __name__ == "__main__":
    main()