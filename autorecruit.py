import time

time1 = time.perf_counter()
from paddleocr import PaddleOCR,draw_ocr
from PIL import Image
import pyautogui as pyag
time2 = time.perf_counter()
print(time2-time1)


arknights_title = "Arknights"
img_path = './img/screenie.png'

tag_list = ["guard",
    "sniper",
    "defender",
    "medic",
    "supporter",
    "caster",
    "specialist",
    "vanguard",
    "melee",
    "ranged",
    "starter",
    "senior operator",
    "top operator",
    "crowd control",
    "nuker",
    "healing",
    "support",
    "dp-recovery",
    "dps",
    "survival",
    "aoe",
    "defense",
    "slow",
    "debuff",
    "fast-redeploy",
    "shift",
    "summon",
    "robot"]

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
         ["dp-recovery", "vanguard", "survival", "supporter"]),
        ("crowd control",
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
        ("crowd control",
         [["crowd control"]]),
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

def get_img_words(img_path):
    time1 = time.perf_counter()
    ocr = PaddleOCR(lang='en', enable_mkldnn = True) # need to run only once to download and load model into memory
    result = ocr.ocr(img_path, cls=False)
    time2 = time.perf_counter()
    print(time2-time1)
    return result

def get_relevant_words(result):
    curr_tags = []
    curr_ui_elems = []
    for idx in range(len(result)):
        res = result[idx]
        for line in res:
            formatted_line = line[1][0].strip().lower()
            print(formatted_line)
            #Get relevant UI features
            if formatted_line[:2] == "01":
                curr_ui_elems.append((line[0],formatted_line[:2]))
            #Get all recruitment tags
            if formatted_line in tag_list:
                curr_tags.append((line[0], formatted_line))
    if len(curr_tags) != 5:
        print("tag count inaccurate")
    return (curr_tags,curr_ui_elems)
    


def tags_to_combos(loc_tags):
    tags = [x[1] for x in loc_tags]
    rare_tag_list = []
    for rarity in tag_dict:
        for tag in tag_dict[rarity]:
            if tag[0] in tags:
                for x in tag[1]:
                    for y in x:
                        if y in tags:
                            rare_tag_list.append((rarity, x + [tag[0]]))
            else:
                continue
    return sorted(rare_tag_list, reverse=True, key=lambda x : x[0])


def draw_result(result,img_path):
    # draw result
    
    result = result[0]
    image = Image.open(img_path).convert('RGB')
    boxes = [line[0] for line in result]
    txts = [line[1][0] for line in result]
    scores = [line[1][1] for line in result]
    im_show = draw_ocr(image, boxes, txts, scores, font_path='./fonts/simfang.ttf')
    im_show = Image.fromarray(im_show)
    im_show.save('result.jpg')

def combo_testing():
    return

def get_coords(all_pos,rare_tags, ui_pos):

    if not rare_tags:
        return []
    unique_tags = set(rare_tags[0][1])
    
    coords = []
    for y in all_pos:

        if y[1] in unique_tags:
            coords.append(y[0][0])
    return coords

def get_ui_coords(relevant_ui,screen_scale):
    coords = []
    print(relevant_ui)
    for x in relevant_ui:
        if x[1] == "01":
            coords.append([x[0][0][0],x[0][0][1]+150])
    return coords
    


def recruit_page_inputs(coords):
    print(coords)
    for x in coords:
        pyag.moveTo(x[0],x[1])
        pyag.mouseDown()
        pyag.mouseUp()

    #TODO: get rid of magic #s
    try:
        hour_loc = pyag.locateOnScreen("img/hour_adjust.png",confidence=0.9)
        pyag.moveTo(hour_loc[0]+50,hour_loc[1]+250)
        pyag.mouseDown()
        pyag.mouseUp()
    except pyag.ImageNotFoundException:
        print("Hour not located")

    confirm_loc = pyag.locateOnScreen("img/confirm_button.png",confidence=0.8)
    pyag.moveTo(confirm_loc[0]+50,confirm_loc[1]+50)

    #pyag.mouseDown()
    #pyag.mouseUp()

def take_sceenshot():
    arknights_window = pyag.getWindowsWithTitle(arknights_title)[0]
    arknights_window.activate()
    time.sleep(0.1)

    im = pyag.screenshot()
    im.save(img_path)
    return im

if __name__ == "__main__":

    #Try a different method to bring window to forefront
    im = take_sceenshot()
    

    words = get_img_words(img_path)

    #draw_result(words,img_path)

    relevant_tags,relevant_ui = get_relevant_words(words)
    print(relevant_ui)

    print(relevant_tags)
    rare_tags = tags_to_combos(relevant_tags)
    print(rare_tags)


    if (rare_tags and rare_tags[0][0] >= 5):
        print("Very Rare Tag Discovered! Stopping Execution")
        exit()
    else:
        coords = get_coords(relevant_tags,rare_tags,relevant_ui)
        ui_coords = get_ui_coords(relevant_ui,None)
        total_coords = coords+ui_coords
        print(total_coords)
        recruit_page_inputs(total_coords)
    



#Look into doing the operations 
    