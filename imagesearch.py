import time
import numpy as np
from numpy.random import randint as r
import pyautogui
import cv2
import win32gui
import win32ui
import win32api
import win32con
from ctypes import windll
from PIL import Image
from pynput import keyboard
from pynput.keyboard import Key

windowName = 'NoxPlayer'
menuUnstuck = 30

hRes = 1280
vRes = 720
hMargin = 2
vMargin = 32


def setWindowMargins():
    hwnd = win32gui.FindWindow(None, windowName)
    left, top, right, bot = win32gui.GetWindowRect(hwnd)
    w = right - left
    h = bot - top

    global hMargin
    hMargin = int((w - hRes) / 2)
    global vMargin
    vMargin = int((h - vRes - 2 * hMargin) + hMargin)


def screenshot(rleft=-1, rtop=-1, rright=-1, rbot=-1):
    hwnd = win32gui.FindWindow(None, windowName)

    left, top, right, bot = win32gui.GetWindowRect(hwnd)
    w = right - left
    h = bot - top

    if left < 0 and bot < 0 and right < 0 and top < 0:
        return None

    hwndDC = win32gui.GetWindowDC(hwnd)
    mfcDC = win32ui.CreateDCFromHandle(hwndDC)
    saveDC = mfcDC.CreateCompatibleDC()

    saveBitMap = win32ui.CreateBitmap()
    saveBitMap.CreateCompatibleBitmap(mfcDC, w, h)

    saveDC.SelectObject(saveBitMap)

    result = windll.user32.PrintWindow(hwnd, saveDC.GetSafeHdc(), 0)

    bmpinfo = saveBitMap.GetInfo()
    bmpstr = saveBitMap.GetBitmapBits(True)

    im = Image.frombuffer(
        'RGB',
        (bmpinfo['bmWidth'], bmpinfo['bmHeight']),
        bmpstr, 'raw', 'BGRX', 0, 1)

    win32gui.DeleteObject(saveBitMap.GetHandle())
    saveDC.DeleteDC()
    mfcDC.DeleteDC()
    win32gui.ReleaseDC(hwnd, hwndDC)

    if rleft is not -1:
        return im.crop((rleft + hMargin, rtop + vMargin, rright + hMargin, rbot + vMargin))
    return im


def imagesearcharea(image, x1, y1, x2, y2, precision=0.8, im=None):
    if im is None:
        im = screenshot(x1, y1, x2, y2)

    if not im:
        print("Failed to find window, probably minimized.")
        return [-1, -1]

    img_rgb = np.array(im)
    img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
    template = cv2.imread(image, 0)

    res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
    if max_val < precision:
        return [-1, -1]
    return [max_loc[0] + x1, max_loc[1] + y1]


def imagesearch(image, precision=0.8):
    im = screenshot()
    if not im:
        print("Failed to find window, probably minimized.")
        return [-1, -1]

    img_rgb = np.array(im)
    img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
    template = cv2.imread(image, 0)
    if template.shape:
        template.shape[::-1]
    else:
        return -1

    res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
    if max_val < precision:
        return [-1, -1]
    return max_loc


def imagesearch_loop(image, timesample=1, precision=0.8, timer=np.infty):
    pos = imagesearch(image, precision)
    while pos[0] == -1 and time.perf_counter() - timer < menuUnstuck:
        time.sleep(timesample)
        pos = imagesearch(image, precision)
    return pos


def click_random(pos, timestamp=0.5, action="left", offset=5):
    hWnd = win32gui.FindWindow(None, windowName)
    if offset > 0:
        lParam = win32api.MAKELONG(pos[0] + hMargin + r(-offset, offset),
                                   pos[1] + vMargin + r(-offset, offset))
    else:
        lParam = win32api.MAKELONG(pos[0] + hMargin, pos[1] + vMargin)

    win32gui.PostMessage(hWnd, win32con.WM_LBUTTONDOWN,
                         win32con.MK_LBUTTON, lParam)
    win32gui.PostMessage(hWnd, win32con.WM_LBUTTONUP,
                         0, lParam)
    time.sleep(timestamp)


def click_image(image, pos, timestamp=0.5, action="left", offset=5):
    img = cv2.imread(image)
    width = pos[0]
    height = pos[1]
    if img.shape:
        height, width, channels = img.shape
    newPos = [int(pos[0] + width / 2 - hMargin),
              int(pos[1] + height / 2 - vMargin)]
    click_random(newPos, timestamp, action, height / 10)


def click_exact(pos, timestamp=0.5, action="left"):
    click_random(pos, timestamp, action, 0)


def searchForImage(imageDir, clickPos=False, precision=0.8):
    pos = imagesearch(imageDir, precision)
    if clickPos and pos[0] != -1:
        click_image(imageDir, pos)
    return pos[0] != -1


def searchForImageInArea(imageDir, x1, y1, x2, y2,
                         clickPos=False, precision=0.8):
    im = screenshot(x1, y1, x2, y2)
    pos = imagesearcharea(imageDir, x1, y1, x2, y2, precision, im)
    if clickPos and pos[0] != -1:
        click_image(imageDir, pos)
    return pos[0] != -1


def searchForImageLoop(imageDir, clickPos=False, timer=np.infty):
    pos = imagesearch_loop(imageDir, 1, 0.8, timer)
    if clickPos and pos[0] != -1:
        click_image(imageDir, pos)
    return pos[0] != -1
