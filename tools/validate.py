#!/usr/bin/env python3
"""Sanity-check the mod: XML well-formedness, internal def references, texture paths."""
import os
import sys
import xml.etree.ElementTree as ET

ROOT = "/Coze/Drive/扣子/mods/rimworld-smokehouse/Smokehouse"
errors = []
warnings = []

defs = {}  # defName -> (type, file)


def walk():
    for base, _, files in os.walk(ROOT):
        for f in files:
            if f.endswith(".xml"):
                yield os.path.join(base, f)


for path in sorted(walk()):
    try:
        tree = ET.parse(path)
    except ET.ParseError as e:
        errors.append(f"XML parse error in {path}: {e}")
        continue
    rel = os.path.relpath(path, ROOT)
    for node in tree.getroot():
        name = node.findtext("defName")
        if name:
            defs[name] = (node.tag, rel)

print(f"parsed defs: {len(defs)}")
for n, (t, f) in sorted(defs.items()):
    print(f"  {t:22} {n:24} {f}")

# --- reference checks -------------------------------------------------------
refs = {
    "Smokehouse.recipes": ["Make_SmokedMeat", "Make_DriedVegetables"],
    "products": ["SmokedMeat", "DriedVegetables"],
    "research": ["SmokePreserving"],
    "thought": ["AteSmokedMeal"],
}
for group, names in refs.items():
    for n in names:
        if n not in defs:
            errors.append(f"{group}: referenced def {n} is not defined")

# building recipe list -> defined recipes
bpath = os.path.join(ROOT, "Defs/ThingDefs/Buildings_Smokehouse.xml")
btree = ET.parse(bpath)
for r in btree.getroot().find("ThingDef").find("recipes"):
    if r.text not in defs:
        errors.append(f"building recipes: {r.text} not defined")

# recipes: product + research + thought references
for rpath in [
    os.path.join(ROOT, "Defs/RecipeDefs/Recipes_Smokehouse.xml"),
]:
    rtree = ET.parse(rpath)
    for rec in rtree.getroot():
        for prod in rec.find("products"):
            if prod.tag not in defs:
                errors.append(f"{rec.findtext('defName')}: product {prod.tag} not defined")
        rp = rec.findtext("researchPrerequisite")
        if rp and rp not in defs:
            errors.append(f"{rec.findtext('defName')}: research {rp} not defined")

# research prerequisites -> defined or known vanilla
for name in ["SmokePreserving"]:
    node = None
    for path in walk():
        t = ET.parse(path)
        for n in t.getroot():
            if n.findtext("defName") == name:
                node = n
    for pre in node.find("prerequisites"):
        if pre.text not in defs:
            warnings.append(f"{name}: prerequisite {pre.text} is a vanilla def (expected)")

# food defs: tasteThought reference
for path in walk():
    t = ET.parse(path)
    for n in t.getroot():
        tt = n.findtext("ingestible/tasteThought")
        if tt and tt not in defs:
            errors.append(f"{n.findtext('defName')}: tasteThought {tt} not defined")
        gd = n.find("graphicData")
        if gd is not None:
            tex = gd.findtext("texPath")
            if tex:
                png = os.path.join(ROOT, "Textures", tex + ".png")
                if not os.path.exists(png):
                    errors.append(f"{n.findtext('defName')}: missing texture {png}")

# --- texture size checks ----------------------------------------------------
from PIL import Image
for path in walk():
    t = ET.parse(path)
    for n in t.getroot():
        gd = n.find("graphicData")
        if gd is None:
            continue
        tex, size, cls = gd.findtext("texPath"), gd.findtext("drawSize"), gd.findtext("graphicClass")
        if not tex:
            continue
        img = Image.open(os.path.join(ROOT, "Textures", tex + ".png"))
        if cls == "Graphic_Single" and size:
            w, h = [float(v) for v in size.strip("()").split(",")]
            want = (round(w * 128), round(h * 128))
            if img.size != want:
                errors.append(f"{n.findtext('defName')}: texture {img.size} != expected {want}")
            print(f"  graphic ok: {n.findtext('defName')} {img.size} drawSize {size}")
        else:
            if img.size != (128, 128):
                warnings.append(f"{n.findtext('defName')}: item texture is {img.size}, vanilla uses 128x128")

# --- localisation key coverage ---------------------------------------------
keys = set()
for base, _, files in os.walk(os.path.join(ROOT, "Languages")):
    for f in files:
        if f.endswith(".xml"):
            t = ET.parse(os.path.join(base, f))
            for n in t.getroot():
                keys.add(n.tag)
print(f"\nlocalisation keys: {len(keys)}")

print("\n--- ERRORS ---")
print("\n".join(errors) if errors else "none")
print("--- WARNINGS ---")
print("\n".join(warnings) if warnings else "none")
sys.exit(1 if errors else 0)
