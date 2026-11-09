import os

def sunucu_kontrol(hedef_ip):
    # Kullanıcıdan gelen değer doğrudan kabuk (shell) komutunda kullanılıyor
    os.system("ping -c 1 " + hedef_ip)