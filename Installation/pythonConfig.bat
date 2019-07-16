@echo off
set /p proc=What file to use (1=Generic, 2=AMD) (Recommended=1):

IF %proc% EQU 1 (
pip install pywin32-224-cp37-cp37m-win32.whl
) ELSE (
pip install pywin32-224-cp37-cp37m-win_amd64.whl
)
python pywin32_postinstall.py -install

pip install numpy pynput pyautogui opencv-python pyqt5 pyside2