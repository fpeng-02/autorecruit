import pyautogui as pyag
import time
import keyboard
import json

tag_dict = {
    6: [("top operator",
         [["top operator"]])
    ],
    5: [
        ("senior operator",
         [["senior operator"]]),
        ("summon",
         [["summon"]]),
        ("debuff",
         [["specialist"], ["fast-redeploy"], ["aoe"], ["melee"], ["supporter"]]),
        ("support",
         [["dp-recovery"], ["vanguard"], ["survival"], ["supporter"]]),
        ("crowd-control",
         [["fast-redeploy"], ["specialist"],["supporter"],["vanguard"],["melee"],["dp-recovery"],["slow"]]),
        ("nuker",
         [["ranged"], ["sniper"],["aoe"],["caster"]]),
        ("shift",
         [["slow"],["dps"],["defense"],["defender"]]),
        ("specialist",
         [["slow"],["survival"]]),
        ("defense",
         [["guard"],["ranged"],["caster"],["aoe"]]),
        ("dps",
         [["defense"],["defender"],["supporter"],["aoe"]]),
        ("survival",
         [["defense"],["defender"],["supporter"]]),
        ("healing",
         [["dps"],["caster"]]),
        ("slow",
         [["dps", "caster"]]) #lol
    ],
    4: [
        ("fast-redeploy",
         [["fast-redeploy"]]),
        ("crowd-control",
         [["crowd-control"]]),
        ("debuff",
         [["debuff"]]),
        ("support",
         [["support"]]),
        ("nuker",
         [["nuker"]]),
        ("shift",
         [["shift"]]),
        ("specialist",
         [["specialist"]]),
        ("survival",
         [["ranged"],["sniper"]]),
        ("healing",
         [["dp-recovery"],["vanguard"],["supporter"]]),
        ("slow",
         [["healing"],["dps"],["caster"],["aoe"],["sniper"],["melee"],["guard"]])
    ]
}

arknights_title = "Arknights"
img_path = './img/screenie.png'
'''
screenWidth, screenHeight = pyag.size()
currentMouseX, currentMouseY = pyag.position()

pyag.moveTo(508,300)
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


arknights_window = pyag.getWindowsWithTitle(arknights_title)[0]
arknights_window.activate()



time.sleep(0.1)

im = pyag.screenshot()
width,height = im.size
top = height/7
bottom = 6*height/7
left = width/4
right = 6*width/7
im1 = im.crop((left, top, right, bottom))
im1.save(img_path)



arknights_window = pyag.getWindowsWithTitle(arknights_title)[0]
arknights_window.activate()
print(arknights_window.size)
'''#638.0, 669.0
#pyag.moveTo(656,460)

'''
def print_ding():
    print("ding")
    exit()

hotkey = 'alt+t'
keyboard.add_hotkey(hotkey, print_ding)
print(f"Waiting for hotkey: {hotkey}")
keyboard.wait()
'''

with open('tag_combos.json', 'w') as fp:
    json.dump(tag_dict, fp)