import threading
import waktu

import numpy as np
import cv2
import keyboard
import win32api, win3import Image
import ImageGrab
import skimage

# Mengambil resolusi layar
scalex = win32api.GetSystemMetrics(win32con.SM_CXSCREEN)
scaley = win32api.GetSystemMetrics(win32con.SM_CYSCREEN)

y_adjust = 0 #50
x_adjust = 0 #80

def ambil_screenshot(nama='screenshot.jpg'):
    im = ImageGrab.grab()  # kiri , atas , kanan, bawah
    im.save(nama)
    #im.tutup()

def tindakan_mouse(x,y):
    x_offset, y_offset = win32api.GetCursorPos()
    win32api.mouse_event(win32con.MOUSEEVENTF_MOVE, x - x_offset - round(((x - x_offset) * 0.35)),
                         y - y_offset - round(((y - y_offset) * 0.35)), 0, 0)

    waktu.sleep(0.00001)

    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, x - x_offset - round(((x - x_offset) * 0.35)),
                         y - y_offset - round(((y - y_offset) * 0.35)), 0, 0)

    waktu.sleep(0.0191)

    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, x - x_offset - round(((x - x_offset) * 0.35)),
                         y - y_offset - round(((y - y_offset) * 0.35)), 0, 0)

def tutup_skrip():
    global bot
    bot = Benar
    while bot:
        jika keyboard.is_pressed('capslock'):
            bot = Salah
            print("Bot warna berhenti!")
            exit()
        waktu.sleep(1)
def deteksi_warna(ukuran=1):
    global bot
    bot = Benar
    while bot:
        ambil_screenshot()
        gambar = cv2.imread('screenshot.jpg')

        # definisikan daftar batasan
        # B, G, R
        titik_terdekat = []
        # melakukan perulangan over batasan
        #lower = merah[0]
        #upper = merah[1]
        # membuat array NumPy dari batasan
        lower = np.array([160, 140, 0], dtype="uint8")
        upper = np.array([255, 255, 45], dtype="uint8")
        # mencari warna dalam batasan yang ditentukan dan menerapkan mask
        mask = cv2.inRange(gambar, lower, upper)
        #output = cv2.bitwise_and(gambar, gambar, mask=mask)
        #cv2.imwrite("res1.png", np.hstack([gambar, output]))
        # mencari titik koordinat dengan mask
        kontur, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        if len(kontur) > 0:
            M = cv2.moments(kontur[0])
            cX = int(M["m10"] / M["m00"])
            cY = int(M["m01"] / M["m00"])
            # menaruh titik terdekat ke dalam array
            titik_terdekat.append((cX, cY))
            # membuat kelipatan (n, m) dan mengeksplor ulang ukuran warna yang cocok
            x = cX - (ukuran * 5)
            y = cY - (ukuran * 5)
            w = cX+ (ukuran * 5)
            h = cY + (ukuran * 5)
            mask2 = cv2.inRange(gambar, lower, upper)
            mask2 = cv2.erode(mask2, None, iterations=1)
            mask2 = cv2.dilate(mask2, None, iterations=1)
            # mencari titik koordinat dengan mask
            kontur2, _ = cv2.findContours(mask2, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
            if len(kontur2) > 0:
                M2 = cv2.moments(kontur2[0])
                cX2 = int(M2["m10"] / M2["m00"])
                cY2 = int(M2["m01"] / M2["m00"])
                # menaruh titik terdekat ke dalam array
                titik_terdekat.append((cX2, cY2))
            # menggambar kotak pada titik yang terdekat
            cv2.rectangle(gambar, (x, y), (w, h), (0, 255, 0), 2)
            # mencari titik terdekat dari titik koordinat mouse
            jarak_terdekat = skimage.distance.euclidean(win32api.GetCursorPos(), titik_terdekat)
            idx_titik_terdekat = np.argmin(jarak_terdekat)
            # mengklik titik terdekat
            tindakan_mouse(titik_terdekat[idx_titik_terdekat][0], titik_terdekat[idx_titik_terdekat][1])
        # menampilkan gambar
        cv2.imshow('gambar', gambar)
        cv2.waitKey(1)

        # hapus gambar lama jika sudah ada
        if os.path.exists('screenshot.jpg'):
            os.remove('screenshot.jpg')
        jika keyboard.is_pressed('capslock'):
            bot = Salah
            print("Bot warna berhenti!")
            cv2.destroyAllWindows()
            exit()
        waktu.sleep(0.1)

tutup_skrip()
deteksi_warna()


# Cara menggunakan bot:
# 1. Pastikan warna yang ingin dicari telah didefinisikan dengan baik (batasan RGB).
# 2. Bot akan mengambil screenshot dan mendeteksi warna yang sesuai.
# 3. Bot akan mengklik titik terdekat dengan kelipatan ukuran yang ditentukan.
# 4. Untuk mengatur ukuran kelipatan, ubah variabel 'ukuran' menjadi angka yang diinginkan.
# 5. Untuk menonaktifkan bot, tekan tombol 'capslock'. Bot akan berhenti dan menutup semua jendela yang dibuka.
# 6. Bot mungkin akan memerlukan waktu untuk memulai pencarian warna, jadi beri waktu untuk memulai.
