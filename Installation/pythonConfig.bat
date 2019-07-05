@echo off
set /p proc=What is your processor (1=Intel, 2=AMD):

IF %proc% EQU 1 (
pip install pywin32-224-cp37-cp37m-win32.whl
) ELSE (
pip install pywin32-224-cp37-cp37m-win_amd64.whl
)
python ywin32_postinstall.py -install

pip install numpy pynput pyautogui opencv-python