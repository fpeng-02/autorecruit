import time

time1 = time.perf_counter()
from paddleocr import PaddleOCR,draw_ocr
from PIL import Image
import pyautogui as pyag
time2 = time.perf_counter()
print(f"import runtime: {time2-time1}")


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
    "crowd-control",
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

def get_img_words(img_path):
    time1 = time.perf_counter()
    ocr = PaddleOCR(lang='en', enable_mkldnn = True) # need to run only once to download and load model into memory
    result = ocr.ocr(img_path, cls=False)
    time2 = time.perf_counter()
    print(f"ocr runtime: {time2-time1}")
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
            #"tap" is from "tap to refresh" and is used to indicate a refresh is availilbe and to anchor the confirm buttom
            #"con" is from "contacting hr" and is used to indicate a refresh is not availilbe and to anchor the confirm buttom
            #"01" is from the timer and is used to anchor the time increase button
            if formatted_line[:2] == "01":
                curr_ui_elems.append((line[0],formatted_line[:2]))
            if formatted_line[:3] == "tap" or formatted_line[:3] == "con":
                curr_ui_elems.append((line[0],formatted_line[:3]))
            
            #Get all recruitment tags
            if formatted_line in tag_list:
                curr_tags.append((line[0], formatted_line))
    if len(curr_tags) != 5:
        print("Tag count is inaccurate! (not 5)")
    return (curr_tags,curr_ui_elems)
    


def tags_to_combos(loc_tags):
    tags = [x[1] for x in loc_tags]
    rare_tag_list = []
    for rarity in tag_dict:
        for tag in tag_dict[rarity]:
            if tag[0] in tags:
                for x in tag[1]:
                    if all([(y in tags) for y in x]):
                        rare_tag_list.append((rarity, x + [tag[0]]))         
            else:
                continue
    return sorted(rare_tag_list, reverse=True, key=lambda x : x[0])


def draw_result(result,img_path):    
    result = result[0]
    image = Image.open(img_path).convert('RGB')
    boxes = [line[0] for line in result]
    txts = [line[1][0] for line in result]
    scores = [line[1][1] for line in result]
    im_show = draw_ocr(image, boxes, txts, scores, font_path='./fonts/simfang.ttf')
    im_show = Image.fromarray(im_show)
    im_show.save('result.jpg')

def get_coords(all_pos,rare_tags):
    if not rare_tags:
        return []
    unique_tags = set(rare_tags[0][1])
    
    coords = []
    for y in all_pos:

        if y[1] in unique_tags:
            coords.append(y[0][0])
    return coords

def get_confirm_coords(relevant_ui,screen_scale):
    width = screen_scale.width
    height = screen_scale.height
    time_ui_height_multiplier = 0.15
    confirm_ui_height_multiplier = 0.15

    coords = []
    print(relevant_ui)
    confirm = None
    for x in relevant_ui:
        if x[1] == "01":
            coords.append([x[0][0][0], x[0][0][1] + (time_ui_height_multiplier * height)])
        if x[1] == "tap" or x[1] == "con":
            confirm = x 
    #Ensure the confirm is the last thing to be added to the list
    coords.append([confirm[0][0][0], confirm[0][0][1] + (confirm_ui_height_multiplier * height)])
    return coords
    
def get_refresh_coords(relevant_ui, screen_scale):
    width = screen_scale.width
    height = screen_scale.height
    refresh_ui_height_multiplier = -0.05
    refresh_ui_width_multiplier = 0.05
    confirm_refresh_height_multiplier = 0.03

    coords = []
    for x in relevant_ui:
        if x[1] == "tap":
            #tapping
            coords.append([x[0][0][0]+ (refresh_ui_width_multiplier * width), x[0][0][1] + (refresh_ui_height_multiplier * height)])
            coords.append([x[0][0][0], x[0][0][1] + (confirm_refresh_height_multiplier * height)])
            return coords
    raise Exception(f"tap not located on screen in a refresh scenario, coords: {relevant_ui}")

def recruit_page_inputs(coords):
    print(coords)
    for x in coords:
        pyag.moveTo(x[0],x[1])
        pyag.mouseDown()
        pyag.mouseUp()

def activate_window():
    arknights_window = pyag.getWindowsWithTitle(arknights_title)[0]
    arknights_window.activate()
    window_size = arknights_window.size
    return window_size

def take_sceenshot():
    im = pyag.screenshot()
    im.save(img_path)
    return im

def refresh_availible(relevant_ui):
    for x in relevant_ui:
        if x[1] == "tap":
            return True
        if x[1] == "con":
            return False
    raise Exception(f"tap/con not located on screen, ui coords: {relevant_ui}")

def run_recruit():
    #Bring Arknights window to the forefront
    window_size = activate_window()
    time.sleep(0.1)
    #Take the screenshot and save it as img/screenie.png
    im = take_sceenshot()
    
    #Run OCR to get the text from the image
    words = get_img_words(img_path)
    #draw_result(words,img_path)

    #Process the results of the OCR to get relevant text.
    #This includes the recruitment tags and certain other text that will be used as anchors for other UI elements
    relevant_tags,relevant_ui = get_relevant_words(words)
    print(f"relevant ui: {relevant_ui}")
    print(f"relevant tags: {relevant_tags}")
    #From the tags, we extract any rare tag combos (robot, 4 star)
    rare_tags = tags_to_combos(relevant_tags)
    print(f"rare tags: {rare_tags}")

    #Check if no rare tags are present, and if a refresh is availible, if so we refresh and run recruitment again.
    if (not rare_tags and refresh_availible(relevant_ui)):
        refresh_coords = get_refresh_coords(relevant_ui, window_size)
        recruit_page_inputs(refresh_coords)
        print("Refreshing!")
        run_recruit()
    #If we have a 5 star or above, we stop recruitment since 5 stars should be up to the user to select.
    elif (rare_tags and rare_tags[0][0] >= 5):
        print("Very Rare Tag Discovered! Stopping Execution")
        exit()
    #Otherwise we run through and do the recruitment as normal. If 3 star no tags are selected (for now).
    else:
        coords = get_coords(relevant_tags,rare_tags)
        ui_coords = get_confirm_coords(relevant_ui,window_size)
        total_coords = coords+ui_coords
        print(f"total coords: {total_coords}")
        recruit_page_inputs(total_coords)

if __name__ == "__main__":
    run_recruit()

    
    



#Look into doing the operations 
    