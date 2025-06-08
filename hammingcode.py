import tkinter as tk
from tkinter import messagebox
import math

hammingcode = []
kontrol_biti_sayisi = 0
toplam_bit_sayisi = 0
hatali_bit = 0

# XOR hesaplama
def xor_hesaplama(i, j):
    return str(int(i) ^ int(j))
# Binaryden decimale çevirme
def binary_to_decimal(veri):
    return int("".join(veri), 2)

# Hamming kodunu hesapla
def hesapla_hamming():
    global hammingcode, kontrol_biti_sayisi, toplam_bit_sayisi
    canvas.delete("all")
    veri = veri_giris.get().strip()

    if len(veri) not in [8, 16, 32] or not all(c in "01" for c in veri):
        messagebox.showerror("Hata", "Lütfen yalnızca 8, 16 veya 32 bitlik 0 ve 1'lerden oluşan veri girin.")
        return

    veri_uzunluk = len(veri)
    kontrol_biti_sayisi = 0
    while (2**kontrol_biti_sayisi < veri_uzunluk + kontrol_biti_sayisi + 1):
        kontrol_biti_sayisi += 1

    toplam_bit_sayisi = veri_uzunluk + kontrol_biti_sayisi
    #İlk indexi boşluk olarak alıyorum çünkü parity bitit hesaplamalarında index kontrolü kolaylaşmış oluyor.
    hammingcode = [' '] + ['0'] * toplam_bit_sayisi


    j = 0
    for i in range(1, toplam_bit_sayisi + 1):
        if math.log2(i).is_integer():
            continue
        hammingcode[i] = veri[j]
        j += 1

    for i in range(kontrol_biti_sayisi):
        parity_pos = 2 ** i
        xor_sum = 0
        for j in range(1, toplam_bit_sayisi + 1):
            if j & parity_pos:
                xor_sum ^= int(hammingcode[j])
        hammingcode[parity_pos] = str(xor_sum)

    ciz_kod()

# Hamming kodunu canvas'a çiziyoruz.
def ciz_kod(bozulmus=False, hatali_pozisyon=0):
    canvas.delete("all")
    start_x = 20
    y = 30

    for i in range(1, toplam_bit_sayisi + 1):
        x = start_x + (i - 1) * 40
        color = "red" if i == hatali_pozisyon else "lightgray"
        canvas.create_rectangle(x, y, x + 30, y + 30, fill=color)
        canvas.create_text(x + 15, y + 15, text=hammingcode[i], font=("Arial", 12, "bold"))
        canvas.create_text(x + 15, y + 45, text=str(i), font=("Arial", 10))

        if i == hatali_pozisyon:
            # ok ve açıklama
            canvas.create_text(x + 15, y - 10, text="▲", font=("Arial", 14), fill="red")
            canvas.create_text(x + 15, y - 25, text="Hatalı Bit", font=("Arial", 10), fill="red")

# Bit bozma ve sendrom çözme işlemi
def boz_bit():
    global hatali_bit
    try:
        pozisyon = int(bozma_giris.get())
    except ValueError:
        messagebox.showerror("Hata", "Lütfen geçerli bir sayı girin.")
        return

    if pozisyon < 1 or pozisyon > toplam_bit_sayisi:
        messagebox.showerror("Hata", f"Pozisyon 1 ile {toplam_bit_sayisi} arasında olmalı.")
        return

    hammingcode[pozisyon] = '1' if hammingcode[pozisyon] == '0' else '0'

    sendrom_kelimesi = []
    for i in range(kontrol_biti_sayisi):
        parity_pos = 2 ** i
        xor_sum = 0
        for j in range(1, toplam_bit_sayisi + 1):
            if j & parity_pos:
                xor_sum ^= int(hammingcode[j])
        sendrom_kelimesi.insert(0, str(xor_sum))

    hatali_bit = binary_to_decimal(sendrom_kelimesi)
    if hatali_bit == 0:
        sonuc_label.config(text="✅ Hata tespit edilmedi.")
    else:
        sonuc_label.config(text=f"❌ Hatalı bit pozisyonu: {hatali_bit}")

    ciz_kod(bozulmus=True, hatali_pozisyon=hatali_bit)

# Arayüz tasarımı
pencere = tk.Tk()
pencere.title("Hamming SEC-DED Görsel Simülatör")
pencere.geometry("750x400")

tk.Label(pencere, text="Veri (8 / 16 / 32 bit, sadece 0 ve 1):").pack()
veri_giris = tk.Entry(pencere, width=50)
veri_giris.pack()

tk.Button(pencere, text="Hamming Kodu Hesapla", command=hesapla_hamming).pack(pady=5)

tk.Label(pencere, text="Bozulacak bit pozisyonu (1'den başlayarak):").pack()
bozma_giris = tk.Entry(pencere, width=10)
bozma_giris.pack()

tk.Button(pencere, text="Bit Boz ve Hata Tespit Et", command=boz_bit).pack(pady=5)

sonuc_label = tk.Label(pencere, text="Sonuç: ")
sonuc_label.pack(pady=5)

canvas = tk.Canvas(pencere, width=1000, height=200, bg="white")
canvas.pack(pady=10)

pencere.mainloop()
