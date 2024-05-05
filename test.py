import pyautogui as pyag
import time


screenWidth, screenHeight = pyag.size()
currentMouseX, currentMouseY = pyag.position()

pyag.moveTo(100,150)
pyag.getWindowsWithTitle("Arknights")[0].minimize()

pyag.getWindowsWithTitle("Arknights")[0].maximize()
time.sleep(.2)
#pyag locla on screen fcn
im1 = pyag.screenshot("screenie.png")
loc = pyag.locateOnScreen("img/confirm_button.png",confidence=0.8)

pyag.moveTo(loc[0]+50,loc[1]+50)

loc = pyag.locateOnScreen("img/hour_adjust.png",confidence=0.9)
pyag.moveTo(loc[0]+50,loc[1]+250)
pyag.mouseDown()
pyag.mouseUp()
