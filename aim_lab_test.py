import waktu

import pyautogui
import cv2
import keyboard
import win32api, win32con
dari PIL import Image, ImageGrab

y_adjust = 64
pyautogui.MINIMUM_SLEEP = 0
pyautogui.MINIMUM_DURATION = 0
def ambil_screenshot():
    myScreenshot = ImageGrab.grab()
    return myScreenshot

def tindakan_mouse(x,y):
    pyautogui.moveTo(0, 0)
    x_offset, y_offset = pyautogui.position()
    y_offset -= y_adjust # saya memiliki monitor yang tidak seimbang
    win32api.mouse_event(win32con.MOUSEEVENTF_MOVE, x - x_offset - round(((x - x_offset) * 0.4)),
                         y - y_offset - round(((y - y_offset) * 0.4)), 0, 0)

    waktu.sleep(0.005)

    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, x - x_offset - round(((x - x_offset) * 0.4)),
                         y - y_offset - round(((y - y_offset) * 0.4)), 0, 0)

    waktu.sleep(0.0005)

    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, x - x_offset - round(((x - x_offset) * 0.4)),
                         y - y_offset - round(((y - y_offset) * 0.4)), 0, 0)

def deteksi_warna(rgb):
    bot = True
    while bot:
        if keyboard.is_pressed('capslock'):
            print("Bot warna berhenti!")
            exit()
        img = ambil_screenshot()
        #img = Image.open(filename)
        lebar, tinggi = img.size
        img = img.convert('RGBA')
        data = img.getdata()
        #image = cv2.imread(filename)
        i = 0
        untuk item dalam data:
            #print(item)
            jika item[0] > rgb[0] - 10 dan item[1] > rgb[1] - 50 dan item[2] > rgb[2] - 10:
                jika item[0] < rgb[0] + 10 dan item[1] < rgb[1] + 54 dan item[2] < rgb[2] + 50:
                    #print(True)
                    #print("index:", [i])
                    #print("tinggi gambar:", tinggi, "| lebar gambar:", lebar)
                    #print("baris:", i/lebar, "kolom:", (i/lebar % 1)*lebar)
                    y = round(i/lebar)
                    x = round((i/lebar % 1)*lebar)
                    tindakan_mouse(x, y)
                    #image = cv2.rectangle(image, pt1=(x - 2, y - 2), pt2=(x + 2, y + 2), warna=(0, 0, 0), tebal=1)
                    #cv2.imwrite("textshot.png", image)

                    break
            i += 1


# Tekan tombol hijau di gutter untuk menjalankan skrip.
jika __name__ == '__main__':
    waktu.sleep(5)
    deteksi_warna((22, 201, 208)) # bola biru aim lab
