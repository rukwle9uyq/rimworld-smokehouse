#!/usr/bin/env python3
"""Generate the mod's pixel-art textures (logical pixel grid, nearest-neighbour upscale)."""
from PIL import Image, ImageDraw
import os

OUT = "/Coze/Drive/扣子/mods/rimworld-smokehouse/Smokehouse/Textures"
SCALE = 8

OUTLINE = (36, 26, 18, 255)
WOOD = (107, 74, 48, 255)
WOOD_D = (78, 53, 34, 255)
WOOD_L = (140, 100, 66, 255)
ROOF = (91, 65, 48, 255)
ROOF_D = (58, 41, 30, 255)
STONE = (110, 108, 104, 255)
STONE_L = (146, 143, 138, 255)
DOOR = (47, 33, 24, 255)
EMBER = (224, 139, 47, 255)
EMBER_L = (247, 194, 96, 255)
SMOKE = (176, 176, 172, 190)
SMOKE_L = (208, 208, 204, 150)
MEAT = (122, 58, 42, 255)
MEAT_L = (163, 84, 58, 255)
MEAT_D = (84, 38, 28, 255)
TWINE = (201, 168, 106, 255)
SACK = (168, 146, 114, 255)
SACK_L = (196, 176, 142, 255)
SACK_D = (122, 104, 78, 255)
CARROT = (217, 139, 63, 255)
CABBAGE = (138, 154, 74, 255)


def canvas(w, h):
    img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    return img, ImageDraw.Draw(img)


def smokehouse():
    img, d = canvas(32, 16)

    # smoke above the chimney
    d.rectangle([25, 0, 26, 1], fill=SMOKE_L)
    d.rectangle([27, 1, 28, 2], fill=SMOKE)
    d.rectangle([24, 1, 25, 2], fill=SMOKE)
    d.rectangle([26, 3, 27, 3], fill=SMOKE_L)

    # chimney
    d.rectangle([22, 2, 26, 7], fill=STONE, outline=OUTLINE)
    d.rectangle([23, 2, 23, 6], fill=STONE_L)
    d.rectangle([22, 2, 26, 2], fill=STONE_L)

    # roof (hip shape), overhanging the walls
    d.polygon([(0, 8), (4, 4), (27, 4), (31, 8)], fill=ROOF, outline=OUTLINE)
    for x in range(5, 27, 4):
        d.line([(x, 5), (x - 1, 7)], fill=ROOF_D)
    d.line([(0, 8), (31, 8)], fill=ROOF_D)

    # walls
    d.rectangle([1, 8, 30, 14], fill=WOOD, outline=OUTLINE)
    for y in (10, 12, 14):
        d.line([(1, y), (30, y)], fill=WOOD_D)
    for x in (7, 15, 23):
        d.line([(x, 9), (x, 13)], fill=WOOD_D)

    # door with frame and handle
    d.rectangle([4, 9, 9, 14], fill=DOOR, outline=OUTLINE)
    d.rectangle([4, 9, 9, 9], fill=WOOD_L)
    d.rectangle([8, 11, 8, 11], fill=TWINE)

    # smoke vent with embers glowing inside
    d.rectangle([20, 9, 25, 12], fill=DOOR, outline=OUTLINE)
    d.rectangle([21, 10, 24, 11], fill=EMBER)
    d.rectangle([22, 11, 23, 11], fill=EMBER_L)

    # plank shadow along the base
    d.rectangle([1, 14, 30, 14], fill=WOOD_D)

    return img


def smoked_meat():
    img, d = canvas(16, 16)
    strips = [(2, 5, 12, 8), (3, 8, 11, 10), (2, 10, 12, 13)]
    for (x0, y0, x1, y1) in strips:
        d.rectangle([x0, y0, x1, y1], fill=MEAT, outline=OUTLINE)
        d.line([(x0 + 1, y0 + 1), (x1 - 1, y0 + 1)], fill=MEAT_L)
        d.line([(x0 + 1, y1 - 1), (x1 - 1, y1 - 1)], fill=MEAT_D)
    # twine binding
    d.line([(6, 4), (6, 13)], fill=TWINE)
    d.line([(7, 4), (7, 13)], fill=TWINE)
    d.rectangle([5, 6, 8, 7], fill=TWINE, outline=OUTLINE)
    return img


def dried_veg():
    img, d = canvas(16, 16)
    # cloth sack
    d.polygon([(4, 5), (12, 5), (13, 13), (3, 13)], fill=SACK, outline=OUTLINE)
    d.polygon([(4, 5), (7, 5), (7, 13), (3, 13)], fill=SACK_L)
    d.line([(4, 11), (12, 11)], fill=SACK_D)
    d.rectangle([5, 3, 11, 5], fill=SACK_D, outline=OUTLINE)
    d.line([(5, 4), (11, 4)], fill=TWINE)
    # dried flakes spilling over the rim
    d.rectangle([6, 2, 7, 2], fill=CARROT)
    d.rectangle([9, 2, 10, 2], fill=CABBAGE)
    d.rectangle([7, 1, 8, 1], fill=CARROT)
    d.rectangle([10, 3, 11, 3], fill=CABBAGE)
    return img


def save(img, path, target_w, target_h):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    big = img.resize((target_w, target_h), Image.NEAREST)
    big.save(path)
    print("wrote", path, big.size)


save(smokehouse(), f"{OUT}/Things/Building/Production/Smokehouse.png", 32 * SCALE, 16 * SCALE)
save(smoked_meat(), f"{OUT}/Things/Item/Meal/SmokedMeat.png", 16 * SCALE, 16 * SCALE)
save(dried_veg(), f"{OUT}/Things/Item/Meal/DriedVegetables.png", 16 * SCALE, 16 * SCALE)

# preview: 512x512 mod-list thumbnail built from the same sprites
preview = Image.new("RGBA", (512, 512), (58, 52, 46, 255))
bg = ImageDraw.Draw(preview)
for i in range(0, 512, 64):
    bg.line([(i, 0), (i, 512)], fill=(66, 60, 53, 255))
    bg.line([(0, i), (512, i)], fill=(66, 60, 53, 255))
house = smokehouse().resize((32 * SCALE * 2, 16 * SCALE * 2), Image.NEAREST)
preview.alpha_composite(house, (0, 96))
meat = smoked_meat().resize((128, 128), Image.NEAREST)
veg = dried_veg().resize((128, 128), Image.NEAREST)
preview.alpha_composite(meat, (96, 336))
preview.alpha_composite(veg, (288, 336))
preview.convert("RGB").save(
    "/Coze/Drive/扣子/mods/rimworld-smokehouse/Smokehouse/About/preview.png"
)
print("wrote preview")
