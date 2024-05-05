from paddleocr import PaddleOCR,draw_ocr
from PIL import ImageFont
from PIL import Image

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
    ocr = PaddleOCR(use_angle_cls=True, lang='en') # need to run only once to download and load model into memory
    result = ocr.ocr(img_path, cls=True)
    return result

def words_to_tags(result):
    curr_tags = []
    for idx in range(len(result)):
        res = result[idx]
        for line in res:
            print(line)
            formatted_line = line[1][0].strip().lower()
            if formatted_line in tag_list:
                curr_tags.append((line[0], formatted_line))
    if len(curr_tags) != 5:
        print("tag count inaccurate")
    return curr_tags
    


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

if __name__ == "__main__":
    img_path = './img/test9.jpg'

    words = get_img_words(img_path)

    draw_result(words,img_path)

    x = words_to_tags(words)
    print(x)
    valid_tags = tags_to_combos(x)
    print(valid_tags)



    
