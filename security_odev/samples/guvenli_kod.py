import json
import os

def guvenli_veri_isle(dosya_adi):
    base_dir = "/app/data"
    # Dizin geçişi önlemi: sadece en sondaki dosya adını al
    guvenli_isim = os.path.basename(dosya_adi)
    tam_yol = os.path.join(base_dir, guvenli_isim)
    
    # Pickle yerine güvenli JSON formatı kullanımı
    with open(tam_yol, 'r') as f:
        return json.load(f)