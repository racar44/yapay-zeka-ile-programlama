import pickle

def veriyi_yukle(guvenilmeyen_bayt_dizisi):
    # Dışarıdan gelen bayt dizisi doğrudan pickle ile açılıyor (Insecure Deserialization)
    return pickle.loads(guvenilmeyen_bayt_dizisi)