import threading
import waktu

import numpy as np
import cv2
import keyboard
import win32api, win32con
dari PIL import Image, ImageGrab
import skapy

# Mendapatkan resolusi layar.
scalex = win32api.GetSystemMetrics(win32con.SM_CXSCREEN)
scaley = win32api.GetSystemMetrics(win32con.SM_CYSCREEN)

fov = 0.65 # Ubah berdasarkan Sudut Persepsi (Field of View)

def ambil_screenshot(nama='screenshot.jpg'):
    im = ImageGrab.grab()  # kiri , atas , kanan, bawah
    im.save(nama)
    #im.tutup()

def tindakan_mouse(x,y):
    global fov
    #print("x dan y:", x, y)
    pos_x, pos_y = win32api.GetCursorPos() # butuh mendapatkan posisi mouse relatif dan menyesuaikan untuk layar FPS
    #print("Pos x dan y:", pos_x,pos_y)
    dx = int(x - pos_x)
    dy = int(y - pos_y)
    #print("dx dan dy:", dx, dy)

    adj_x = round((dx * fov))
    adj_y = round((dy * fov))
    #print("disesuaikan dengan skala resolusi:", adj_x, adj_y)
    win32api.mouse_event(win32con.MOUSEEVENTF_MOVE, adj_x,
                         adj_y, 0, 0)

    waktu.sleep(0.00001)

    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, adj_x,
                         adj_y, 0, 0)

    waktu.sleep(0.0191)

    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, adj_x,
                         adj_y, 0, 0)

def atur_ke_fov():
    global fov
    jika keyboard.is_pressed(','):
        fov += 0.05
        print(fov, "Meningkatkan penyesuaian FOV!!!")
    jika keyboard.is_pressed('.'):
        fov -= 0.05
        print(fov, "Menurunkan penyesuaian FOV!!!")
def tutup_skrip():
    global bot
    bot = Benar
    while bot:
        atur_ke_fov()
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
        #cv2.imshow('gambar', output)
        # mencari titik koordinat dengan mask
        _, output = cv2.threshold(mask, 1, 255, cv2.THRESH_BINARY)
        kontur, _ = cv2.findContours(output, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        if len(kontur) > 0:
            M = cv2.moments(kontur[0])
            cX = int(M["m10"] / M["m00"])
            cY = int(M["m01"] / M["m00"])
            # menaruh titik terdekat ke dalam array
            titik_terdekat.append((cX, cY))
            # membuat kelipatan (n, m) dan mengeksplor ulang ukuran warna yang cocok
            x = cX - (ukuran * 5)
            y = cY - (ukuran * 5)
            w = cX + (ukuran * 5)
            h = cY + (ukuran * 5)
            mask2 = cv2.inRange(gambar, lower, upper)
            mask2 = cv2.erode(mask2, None, iterations=1)
            mask2 = cv2.dilate(mask2, None, iterations=1)
            _, output2 = cv2.threshold(mask2, 1, 255, cv2.THRESH_BINARY)
            # cv2.imshow('output2', output2)
            for (cX2, cY2) in titik_terdekat:
                if 0 <= cX2 - ukuran <= 255 and 0 <= cY2 - ukuran <= 255:
                    mask2 = cv2.circle(mask2, (cX2, cY2), ukuran, 0, -1)
                    output2 = cv2.circle(output2, (cX2, cY2), ukuran, 0, -1)
                    cv2.imshow('output2', output2)
            cv2.waitKey(1)
            #menggambar kotak pada titik yang terdekat
            tindakan_mouse(x, y)
            # menggambar kelipatan
            cv2.rectangle(gambar, (x, y), (w, h), (0, 255, 0), 2)
        # menampilkan gambar
        cv2.imshow('gambar', gambar)
        cv2.waitKey(1)

        # hapus gambar lama jika sudah ada
        if os.path.exists('screenshot.jpg'):
            os.remove('screenshot.jpg')
        if keyboard.is_pressed('capslock'):
            bot = Salah
            print("Bot warna berhenti!")
            cv2.destroyAllWindows()
            exit()
        waktu.sleep(0.1)

tutup_skrip()
deteksi_warna()


#Cara menggunakan bot:
# 1. Pastikan warna yang ingin dicari telah didefinisikan dengan baik (batasan RGB).
# 2. Bot akan mengambil screenshot dan mendeteksi warna yang sesuai.
# 3. Bot akan mengklik titik terdekat dengan kelipatan ukuran yang ditentukan.
# 4. Untuk mengatur ukuran kelipatan, ubah variabel 'ukuran' menjadi angka yang diinginkan.
# 5. Untuk menonaktifkan bot, tekan tombol 'capslock'. Bot akan berhenti dan menutup semua jendela yang dibuka.
# 6. Bot mungkin akan memerlukan waktu untuk memulai pencarian warna, jadi beri waktu untuk mem
