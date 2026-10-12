import json
import os
from google import genai
from google.genai import errors

DOSYA_ADI = "urunler.json"
# Senin API anahtarın:
API_ANAHTARI = "AQ.Ab8RN6Ih1WPddwaIE2NKpJWf7AkeKVrQIEih7t-bnXMuHooeaQ"

def verileri_yukle():
    if not os.path.exists(DOSYA_ADI):
        return []
    try:
        with open(DOSYA_ADI, 'r', encoding='utf-8') as dosya:
            return json.load(dosya)
    except (json.JSONDecodeError, IOError):
        print("[HATA] JSON dosyası okunamadı. Temiz bir liste ile başlanıyor.")
        return []

def verileri_kaydet(urunler):
    with open(DOSYA_ADI, 'w', encoding='utf-8') as dosya:
        json.dump(urunler, dosya, ensure_ascii=False, indent=4)

def e_ticaret_api_simulasyonu(urun_talebi):
    os.system('cls' if os.name == 'nt' else 'clear')
    print("=" * 70)
    print(" B2C E-TİCARET SİSTEMİ: API ENTEGRASYONU ".center(70, " "))
    print("=" * 70)

    client = genai.Client(api_key=API_ANAHTARI)
    sistem_mesaji = """
    Sen kurumsal bir e-ticaret sisteminin arka planında çalışan bir veri yapılandırma asistanısın.
    Kullanıcının girdiği ham ürün bilgilerini analiz edip, veritabanına kaydedilebilmesi için SADECE JSON formatında yanıt vermelisin.
    JSON nesnesi kesinlikle şu anahtarları içermelidir:
    {
        "urun_adi": "Kısa ve optimize edilmiş ürün adı",
        "kategori": "Uygun e-ticaret kategorisi",
        "seo_etiketleri": "3 adet virgülle ayrılmış SEO etiketi",
        "satis_aciklamasi": "Müşteriyi ikna edecek profesyonel 2 cümle"
    }
    JSON dışında hiçbir açıklama yazma.
    """

    print(f"\n[AŞAMA 1] KULLANICI TALEBİ ALINDI: '{urun_talebi}'")
    print("[AŞAMA 2] GEMINI SUNUCULARINA API İSTEĞİ GÖNDERİLİYOR...")

    try:
        # Yeni nesil kütüphane formatına uyarlandı
        response = client.models.generate_content(
            model="gemini-1.5-flash",
            contents=f"{sistem_mesaji}\nKullanıcının ürün talebi:\n{urun_talebi}"
        )
        print("[AŞAMA 3] SUNUCUDAN YANIT ALINDI. VERİ ÇÖZÜMLENİYOR...\n")
        
        yapilandirilmis_veri = response.text
        
        # SADECE DİCT DÖNDÜR (Ödev kuralı)
        temiz_yanit = yapilandirilmis_veri.replace("```json", "").replace("```", "").strip()
        return json.loads(temiz_yanit)

    except Exception as e:
        print(f"\n[API HATASI] Bağlantı kurulamadı: {e}")
        print("[BİLGİ] Ödevin çalışmaya devam etmesi için otomatik simülasyon verisi üretiliyor...\n")
        return {
            "urun_adi": urun_talebi.title(),
            "kategori": "Genel Kategoriler",
            "seo_etiketleri": "test, otomatik, ürün",
            "satis_aciklamasi": "API bağlantısı kurulamadığı için bu ürün açıklaması otomatik oluşturuldu."
        }

def stok_uyarisi_yazdir(stok):
    if stok == 0:
        print("[UYARI] STOKTA YOK")
    elif 1 <= stok <= 4:
        print(f"[UYARI] KRİTİK STOK! Yalnızca {stok} adet kaldı.")

def yeni_urun_ekle(urunler):
    aciklama = input("Ürün açıklaması: ")
    
    while True:
        try:
            fiyat = float(input("Ürün fiyatı: "))
            stok = int(input("Stok miktarı: "))
            if fiyat < 0 or stok < 0:
                print("[HATA] Fiyat ve stok negatif olamaz.")
                continue
            break
        except ValueError:
            print("[HATA] Lütfen geçerli sayısal değerler girin.")
            
    api_yaniti = e_ticaret_api_simulasyonu(aciklama)
    
    if not api_yaniti:
        print("[HATA] Ürün verisi oluşturulamadı.")
        return

    # URN Kodu Üretimi
    yeni_id = 1
    if urunler:
        son_kod = urunler[-1]["urun_kodu"]
        yeni_id = int(son_kod.split("-")[1]) + 1
    urun_kodu = f"URN-{yeni_id:04d}"

    yeni_urun = {
        "urun_kodu": urun_kodu,
        "urun_adi": api_yaniti.get("urun_adi", "Bilinmeyen Ürün"),
        "kategori": api_yaniti.get("kategori", "Genel"),
        "seo_etiketleri": api_yaniti.get("seo_etiketleri", ""),
        "satis_aciklamasi": api_yaniti.get("satis_aciklamasi", ""),
        "fiyat": fiyat,
        "stok": stok
    }
    
    urunler.append(yeni_urun)
    verileri_kaydet(urunler)
    
    print("\n[BAŞARILI] Ürün kaydedildi.")
    print(f"Ürün Kodu: {urun_kodu}")
    print(f"Ürün Adı: {yeni_urun['urun_adi']}")
    print(f"Kategori: {yeni_urun['kategori']}")
    print(f"Fiyat: {fiyat} TL")
    print(f"Stok: {stok}")
    print(f"SEO: {yeni_urun['seo_etiketleri']}")
    stok_uyarisi_yazdir(stok)

def urunleri_listele(urunler):
    if not urunler:
        print("[BİLGİ] Listelenecek ürün bulunmuyor.")
        return
    
    for u in urunler:
        print("-" * 30)
        print(f"Kod: {u['urun_kodu']} | Ad: {u['urun_adi']}")
        print(f"Kategori: {u['kategori']} | Fiyat: {u['fiyat']} TL | Stok: {u['stok']}")
        stok_uyarisi_yazdir(u['stok'])

def urun_ara(urunler):
    aranan = input("Aranacak ürün (Ad veya Kod): ").lower()
    bulunanlar = [u for u in urunler if aranan in u['urun_adi'].lower() or aranan in u['urun_kodu'].lower()]
    
    print(f"\n[SONUÇ] {len(bulunanlar)} ürün bulundu.")
    for u in bulunanlar:
        print(f"- {u['urun_kodu']}: {u['urun_adi']} (Stok: {u['stok']})")

def stok_guncelle(urunler):
    kod = input("Ürün kodu (Örn: URN-0001): ").upper()
    for u in urunler:
        if u['urun_kodu'] == kod:
            eski_stok = u['stok']
            try:
                yeni_stok = int(input("Yeni stok miktarı: "))
                if yeni_stok < 0:
                    print("[HATA] Stok negatif olamaz.")
                    return
                u['stok'] = yeni_stok
                verileri_kaydet(urunler)
                print(f"[BAŞARILI] Stok {eski_stok} -> {yeni_stok} olarak güncellendi.")
                stok_uyarisi_yazdir(yeni_stok)
            except ValueError:
                print("[HATA] Lütfen geçerli bir tam sayı girin.")
            return
    print("[HATA] Belirtilen kodla eşleşen ürün bulunamadı.")

def ana_menu():
    urunler = verileri_yukle()
    
    while True:
        print("\n=== E-TİCARET YÖNETİM PANELİ ===")
        print("1- Yeni Ürün Ekle")
        print("2- Ürünleri Listele")
        print("3- Ürün Ara")
        print("4- Stok Güncelle")
        print("5- Çıkış")
        
        secim = input("Seçiminiz: ")
        
        if secim == "1":
            yeni_urun_ekle(urunler)
        elif secim == "2":
            urunleri_listele(urunler)
        elif secim == "3":
            urun_ara(urunler)
        elif secim == "4":
            stok_guncelle(urunler)
        elif secim == "5":
            print("Çıkış yapılıyor...")
            break
        else:
            print("[HATA] Geçersiz seçim, lütfen 1-5 arası bir değer girin.")

if __name__ == "__main__":
    ana_menu()