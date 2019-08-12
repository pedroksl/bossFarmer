import time
import numpy as np
import cv2
import win32gui
import win32api
import win32con
import win32ui
from ctypes import windll
from numpy.random import randint as r
from PIL import Image

class ImageSearcher:
    def __init__(self, ConCon):
        self.cc = ConCon
        self.windowName = self.cc.configs.windowName
        self.menuUnstuck = self.cc.configs.menuUnstuck
        self.hWnd = win32gui.FindWindow(None, self.windowName)

        self.hRes = 1280
        self.vRes = 720
        self.hMargin = 2
        self.vMargin = 32

    def setWindowMargins(self):
        self.hWnd = win32gui.FindWindow(None, self.windowName)
        left, top, right, bot = win32gui.GetWindowRect(self.hWnd)
        w = right - left
        h = bot - top

        im = self.screenshot()
        im.save("teste.png")

        if self.windowName is "LDPlayer":
            self.hMargin = 1
        else:
            self.hMargin = int((w - self.hRes) / 2)
        self.vMargin = int((h - self.vRes - 2 * self.hMargin) + self.hMargin)
        print(self.hMargin, self.vMargin)

    def getPixel(self, x, y, ignoreMargins=False, image=None):
        if image is None:
            image = self.screenshot()

        xPos = x
        yPos = y
        if not ignoreMargins:
            xPos += self.hMargin
            yPos += self.vMargin
        return image.getpixel((xPos, yPos))

    def screenshot(self, rleft=-1, rtop=-1, rright=-1, rbot=-1, windowName=""):
        if windowName is "":
            windowName = self.windowName
        self.hWnd = win32gui.FindWindow(None, windowName)

        left, top, right, bot = win32gui.GetWindowRect(self.hWnd)
        w = right - left
        h = bot - top

        if left < 0 and bot < 0 and right < 0 and top < 0:
            return None

        hwndDC = win32gui.GetWindowDC(self.hWnd)
        mfcDC = win32ui.CreateDCFromHandle(hwndDC)
        saveDC = mfcDC.CreateCompatibleDC()

        saveBitMap = win32ui.CreateBitmap()
        saveBitMap.CreateCompatibleBitmap(mfcDC, w, h)

        saveDC.SelectObject(saveBitMap)

        result = windll.user32.PrintWindow(self.hWnd, saveDC.GetSafeHdc(), 0)

        bmpinfo = saveBitMap.GetInfo()
        bmpstr = saveBitMap.GetBitmapBits(True)

        im = Image.frombuffer(
            'RGB',
            (bmpinfo['bmWidth'], bmpinfo['bmHeight']),
            bmpstr, 'raw', 'BGRX', 0, 1)

        win32gui.DeleteObject(saveBitMap.GetHandle())
        saveDC.DeleteDC()
        mfcDC.DeleteDC()
        win32gui.ReleaseDC(self.hWnd, hwndDC)

        if rleft is not -1:
            return im.crop((rleft + self.hMargin, rtop + self.vMargin, rright + self.hMargin, rbot + self.vMargin))
        return im


    def imagesearcharea(self, image, x1, y1, x2, y2, precision=0.8, im=None):
        if im is None:
            im = self.screenshot(x1, y1, x2, y2)

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


    def imagesearch(self, image, precision=0.8):
        im = self.screenshot()
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


    def imagesearch_loop(self, image, timesample=1, precision=0.8, timer=np.infty):
        pos = self.imagesearch(image, precision)
        while pos[0] == -1 and time.perf_counter() - timer < self.menuUnstuck:
            time.sleep(timesample)
            pos = self.imagesearch(image, precision)
        return pos


    def click_random(self, pos, timestamp=0.5, action="left", offset=5, windowName=""):
        if windowName is "":
            windowName = self.windowName

        hWnd = win32gui.FindWindow(None, windowName)
        if windowName is "LDPlayer":
            win32gui.EnumChildWindows(hWnd, self.findCorrectChild, "TheRender")
            clickX = pos[0]
            clickY = pos[1]
        else:
            self.hWnd = hWnd
            clickX = pos[0] + self.hMargin
            clickY = pos[1] + self.vMargin
        if offset > 0:
            lParam = win32api.MAKELONG(clickX + r(-offset, offset), clickY + r(-offset, offset))
        else:
            lParam = win32api.MAKELONG(clickX, clickY)

        win32gui.SendMessage(self.hWnd, win32con.WM_LBUTTONDOWN,
                             win32con.MK_LBUTTON, lParam)
        win32gui.SendMessage(self.hWnd, win32con.WM_LBUTTONUP,
                             0, lParam)
        time.sleep(timestamp)


    def click_image(self, image, pos, timestamp=0.5, action="left", offset=5):
        img = cv2.imread(image)
        width = pos[0]
        height = pos[1]
        if img.shape:
            height, width, channels = img.shape
        newPos = [int(pos[0] + width / 2 - self.hMargin),
                  int(pos[1] + height / 2 - self.vMargin)]
        self.click_random(newPos, timestamp, action, height / 10)


    def click_exact(self, pos, timestamp=0.5, action="left"):
        self.click_random(pos, timestamp, action, 0)


    def searchForImage(self, imageDir, clickPos=False, precision=0.8):
        pos = self.imagesearch(imageDir, precision)
        if clickPos and pos[0] != -1:
            self.click_image(imageDir, pos)
        return pos[0] != -1

    def click_scroll(self, pos, dir="up", distance=100, windowName=""):
        if windowName is "":
            windowName = self.windowName
        self.hWnd = win32gui.FindWindow(None, windowName)
        lParam1 = win32api.MAKELONG(pos[0] + self.hMargin, pos[1] + self.vMargin)
        if dir is "up":
            lParam2 = win32api.MAKELONG(pos[0] + self.hMargin, pos[1] - distance + self.vMargin)
        elif dir is "down":
            lParam2 = win32api.MAKELONG(pos[0] + self.hMargin, pos[1] + distance + self.vMargin)
        elif dir is "left":
            lParam2 = win32api.MAKELONG(pos[0] - distance + self.hMargin, pos[1] + self.vMargin)
        elif dir is "right":
            lParam2 = win32api.MAKELONG(pos[0] + distance + self.hMargin, pos[1] + self.vMargin)

        win32gui.SendMessage(self.hWnd, win32con.WM_MOUSEWHEEL, -5000, lParam1)
        time.sleep(0.5)

    def searchForImageInArea(self, imageDir, x1, y1, x2, y2,
                             clickPos=False, precision=0.8):
        im = self.screenshot(x1, y1, x2, y2)
        pos = self.imagesearcharea(imageDir, x1, y1, x2, y2, precision, im)
        if clickPos and pos[0] != -1:
            self.click_image(imageDir, pos)
        return pos[0] != -1


    def searchForImageLoop(self, imageDir, clickPos=False, timer=np.infty):
        pos = self.imagesearch_loop(imageDir, 1, 0.8, timer)
        if clickPos and pos[0] != -1:
            self.click_image(imageDir, pos)
        return pos[0] != -1

    def findCorrectChild(self, hWnd, lParam):
        text = win32gui.GetWindowText(hWnd)
        if text == lParam:
            self.hWnd = hWnd
