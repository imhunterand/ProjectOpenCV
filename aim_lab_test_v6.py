import matematika
import threading
import waktu

import numpy as np
import cv2
import keyboard
import seri
import win32api, win32con.SM_CXSCREEN)
dari PIL import Image, ImageGrab
import skapy

import PyArduinoBot_v2
dari PyArduinoBot_v2 import arduino_mouse

# Mendapatkan resolusi layar.
scalex = win32api.GetSystemMetrics(win32con.SM_CXSCREEN)
scaley = win32api.GetSystemMetrics(win32con.SM_CYSCREEN)

PyArduinoBot_v2.FOV = 1.2 #1.04 57.2% > 1.05
PyArduinoBot_v2.FPS = benar
#print("skala monitor:", scalex,scaley)

def ambil_screenshot(nama='screenshot.jpg'):
    im = ImageGrab.grab()  # kiri , atas , kanan, bawah
    im.save(nama)
    im.tutup()


def atur_ke_fov():
    jika keyboard.is_pressed(','):
        PyArduinoBot_v2.FOV += 0.01
        print(PyArduinoBot_v2.FOV, "Meningkatkan penyesuaian FOV!!!")
    jika keyboard.is_pressed('.'):
        PyArduinoBot_v2.FOV -= 0.01
        print(PyArduinoBot_v2.FOV, "Menurunkan penyesuaian FOV!!!")

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


def tindakan_mouse(x,y, tombol):
    global fov, arduino
    #print("tindakan mouse:", x,y)
    #print("tindakan yang disesuaikan:", adj_x, adj_y)
    #print(tombol)
    arduino_mouse(x, y, ard=arduino, tombol=tombol, winType='FPS')
    #waktu.sleep(0.05)

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
        ret, thresh = cv2.threshold(mask, 40, 255, 0)
        kontur, hierarki = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        kontur = kontur
        cv2.drawContours(gambar, kontur, -1, (255, 0, 0), 2, cv2.LINE_AA)
        #kontur, hierarki = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        untuk c dalam kontur:
            jika cv2.cv2.contourArea(c) > ukuran:

                # print(cv2.pointPolygonTest(c, pt, True))
                # close_poly.append(cv2.pointPolygonTest(c, pt, True))
                x1, y1, w1, h1 = cv2.boundingRect(c)
                # print((x1 + (w1 / 2)), (y1 + (h1 / 2)))
                titik_terdekat.append((round(x1 + (w1 / 2)), round(y1 + (h1 / 2))))

        # print("titik terdekat:", min(titik_terdekat))
        jika len(kontur) != 0:
            pt = (960, 540) # posisi senter layar dan posisi tengah cross-hair #win32api.GetCursorPos()
            #print("pt x dan y:", pt)

            titik_terdekat = titik_terdekat[skapy.spatial.KDTree(titik_terdekat).query(pt)[1]]

            #print(titik_terdekat)
            cv2.circle(gambar, (titik_terdekat[0], titik_terdekat[1]), radius=3, warna=(0, 0, 255), ketebalan=-1)
            cv2.line(gambar, pt, (titik_terdekat[0], titik_terdekat[1]), (0, 255, 0), 2)
            #cv2.imwrite('res_marked.png', gambar)
            print("tujuan:",titik_terdekat[0], titik_terdekat[1])
            tindakan_mouse(titik_terdekat[0], titik_terdekat[1], tombol='kiri')
        #cv2.imshow("gambar", gambar)
        #cv2.waitKey(10)

            #bot = Salah
            # tindakan_mouse(titik_terdekat[0], titik_terdekat[1], tombol=None)
            # jika abs(pt[0]) <= abs(titik_terdekat[0]+15) dan abs(pt[0]) >= abs(titik_terdekat[0]-15):
            #     #print(pt, titik_terdekat)
            #     jika abs(pt[1]) <= abs(titik_terdekat[1]+15) dan abs(pt[1]) >= abs(titik_terdekat[1]-15):
            #         print('tindakan tengah tombol mouse')
            #         tindakan_mouse(titik_terdekat[0], titik_terdekat[1], tombol='kiri')


# Menjalankan skrip.
jika __name__ == '__main__':
    global arduino
    port = 'COM5'
    baudrate = 115200
    arduino = seri.Serial(port=port, baudrate=baudrate, timeout=.1)
    print("Memulai aimbot!!!")
    waktu.sleep(5)
    threading.Thread(target=tutup_skrip).start()
    print("Aimbot On!!!")
    deteksi_warna() # bola biru aim lab
    print("selesai!!")
