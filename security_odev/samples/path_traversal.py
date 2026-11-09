import os

def dosya_oku(dosya_adi):
    base_dir = "/var/www/html/images/"
    # Girdi denetlenmeden doğrudan dosya yoluna ekleniyor (Path Traversal)
    tam_yol = base_dir + dosya_adi
    with open(tam_yol, 'r') as f:
        return f.read()