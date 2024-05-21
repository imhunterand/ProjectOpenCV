# Dalam detik. Durasi yang kurang dari ini dibulatkan menjadi 0.0 untuk langsung memindahkan mouse.
import ctypes
import math
import random
import time
import ctypes.wintypes
import serial

jumlah_langkah = 10
FOV = 1.0
FPS = False
# MENGATASI LAMBAI WAKTU.SLEEP DI WINDOWS OS
timeBeginPeriod = ctypes.windll.winmm.timeBeginPeriod #baru
timeBeginPeriod(1) #baru

jika FPS:
    tambahF = (960, 540)
lain:
    cursor = ctypes.wintypes.POINT()
    ctypes.windll.user32.GetCursorPos(ctypes.byref(cursor))
    tambahF = (cursor.x, cursor.y)
daftar_sebelumnya = [tambahF]
terakhir_daftar = 0,0

def linear(n):
    """
    Mengembalikan ``n``, di mana ``n`` adalah argumen float antara ``0.0`` dan ``1.0``. Fungsi ini untuk tween linear default untuk fungsi gerakan mouse.

    Fungsi ini disalin dari modul PyTweening, sehingga dapat dipanggil meskipun PyTweening tidak terinstal.
    """

    # Kami menggunakan fungsi ini daripada pytweening.linear untuk fungsi tween default hanya dalam kasus pytweening tidak dapat diimport.
    if not 0.0 <= n <= 1.0:
        raise print("Argument harus antara 0.0 dan 1.0.")
    return n

def _position():
    """Mengembalikan koordinat xy saat ini dari kursor mouse sebagai dua integer
    tuple dengan memanggil fungsi GetCursorPos() win32.

    Mengembalikan:
      (x, y) tuple dari koordinat xy saat ini dari kursor mouse.
    """

    cursor = ctypes.wintypes.POINT()
    ctypes.windll.user32.GetCursorPos(ctypes.byref(cursor))
    return (cursor.x, cursor.y)

def getPointOnLine(x1, y1, x2, y2, n):
    global FOV, jumlah_langkah
    """
    Mengembalikan (x, y) tuple dari titik yang telah melanjutkan sebagian besar ``n`` di garis yang ditentukan oleh dua
    koordinat ``x1``, ``y1`` dan ``x2``, ``y2``.

    Fungsi ini disalin dari modul pytweening, sehingga dapat dipanggil meskipun PyTweening tidak terinstal.
    """
    print(n)
    x = (((x2 - x1) * (1 / (jumlah_langkah)))) * FOV
    y = (((y2 - y1) * (1 / (jumlah_langkah)))) * FOV
    return (str(math.ceil(x)) + ":" + str(math.ceil(y)))

def getPoint(x1, y1, x2, y2, n):
    global FOV, jumlah_langkah
    """
    Mengembalikan (x, y) tuple dari titik yang telah melanjutkan sebagian besar ``n`` di garis yang ditentukan oleh dua
    koordinat ``x1``, ``y1`` dan ``x2``, ``y2``.

    Fungsi ini disalin dari modul pytweening, sehingga dapat dipanggil meskipun PyTweening tidak terinstal.
    """print(n)
    x = (((x2 - x1) * (1 / (jumlah_langkah)))) * FOV
    y = (((y2 - y1) * (1 / (jumlah_langkah)))) * FOV
    return (math.ceil(x), math.ceil(y))

def _mouseMoveDrag(x, y, tween=linear, ard=None, winType=None):
    global daftar_sebelumnya, terakhir_daftar, jumlah_langkah
    jika winType == 'FPS':
        startx, starty = (960, 540)
    lain:
        startx, starty = _position()

    arduino = ard
    #x = int(x) jika x tidak None jika tidak x = startx
    #y = int(y) jika y tidak None jika tidak y = starty

    # Jika durasi cukup kecil, langsung geser kursor ke situ.
    langkah = [(x, y)]
    jika FPS:
        jumlah_langkah = 10
    lain:
        jumlah_langkah = 30
    #print('jumlah_langkah:', jumlah_langkah)
    #print("start:", startx, starty)
    langkah = [getPointOnLine(startx, starty, x, y, tween(n / jumlah_langkah)) for n in range(jumlah_langkah + 1)]
    #print("Koordinat final yang dikirim:", langkah)
    # Memastikan posisi terakhir adalah posisi tujuan yang sebenarnya.
    jika tidak FPS:
        langkah.pop()
        langkah.pop(0)


    langkah = str(langkah)
    print("Koordinat final yang dikirim:", langkah)
    arduino.write(bytes(langkah, 'utf-8'))

def getLatestStatus(ard=None):
    status = 'Nothing'
    while ard.inWaiting() > 0:
        status = ard.readline()
    return status

def arduino_mouse(x=100, y=100, ard=None, button=None, winType=None):
    #
    #print("mouse arduino adalah:", button)
    #jika button tidak None:
    _mouseMoveDrag(x, y, tween=linear, ard=ard, winType=winType)
    waktu_mulai = time.time()
    stat = getLatestStatus(ard)
    print(stat)
    print(time.time() - waktu_mulai)
    jika button tidak None:
        time.sleep(0.05)
    lain:
        time.sleep(0.01)
    c = random.uniform(0.02,0.05)
    #time.sleep(0.05)
    #print("mouse arduino yang telah melewati adalah:", button)
    jika button == 'left':
        ard.write(bytes(button, 'utf-8'))
        stat = getLatestStatus(ard)
        print(stat)
        time.sleep(c)
    jika button == 'right':
        ard.write(bytes(button, 'utf-8'))
        stat = getLatestStatus(ard)
        print(stat)
        time.sleep(c)


jika __name__ == '__main__':
    port = 'COM5'
    kecepatan_baud = 115200
    arduino = serial.Serial(port=port, baudrate=kecepatan_baud, timeout=.1)
    time.sleep(5)
    #time.sleep(3.5)
    print('menggunakan mouse arduino untuk memindahkan')
    jika FPS:
        tambahF = (960,540)
    lain:
        cursor = ctypes.wintypes.POINT()
        ctypes.windll.user32.GetCursorPos(ctypes.byref(cursor))
        tambahF = (cursor.x, cursor.y)
    print(tambahF)
    daftar_sebelumnya = [tambahF]
    terakhir_daftar = 0,0
    arduino\_mouse(x=200, y=200, ard=arduino, button='right')
