import time
import pyautogui

print("Waiting 3 seconds... move your mouse over a button or window!")
time.sleep(3)
pos = pyautogui.position()
print(f"Clicking at {pos}")
from pynput.mouse import Controller, Button
mouse = Controller()
mouse.click(Button.left, 1)
