import psycopg2

def veritabanina_baglan():
    # Kimlik bilgileri kaynak koda gömülmüş (Hardcoded credentials)
    return psycopg2.connect(
        host="localhost",
        database="eticaret",
        user="admin",
        password="supergizlisifre123"
    )