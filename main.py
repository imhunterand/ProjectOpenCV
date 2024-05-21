import pyautogui
import numpy as np
import cv2
import random
dari PIL import Image

def deteksi_warna(warna, nama_file):
    gambar = Image.buka(nama_file)
    lebar, tinggi = gambar.size
    gambar = gambar.konversi('RGBA')
    data = gambar.getdata()
    gambar_cv = cv2.imread(nama_file)

    i = 0
    untuk item dalam data:
        print(item)
        jika item[0] == warna[0] dan item[1] == warna[1] dan item[2] == warna[2]:
            print(True)
            print("index:", [i])
            print("tinggi gambar:", tinggi, "| lebar gambar:", lebar)
            print("baris:", i/lebar, "kolom:", (i/lebar % 1)*lebar)
            p2 = round(i/lebar)
            p1 = round((i/lebar % 1)*lebar)
            gambar_cv = cv2.rectangle(gambar_cv, pt1=(p1 - 2, p2 - 2), pt2=(p1 + 2, p2 + 2), warna=(0, 0, 0), tebal=1)
            cv2.imwrite("textshot.png", gambar_cv)
            return True
        i += 1
    print(False)
    return False


jika __name__ == '__main__':
    deteksi_warna((255, 0, 0), 'test.png') # merah
    #deteksi_warna((0, 255, 0), 'test.png') # hijau
    #deteksi_warna((0, 0, 255), 'test.png') # biru
