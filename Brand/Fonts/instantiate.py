"""Instantiate the static card faces from the bundled Google Sans Code variable font.

Run from the repository root: python3 Brand/Fonts/instantiate.py
Requires fontTools. Outputs are committed; rerunning reproduces them.
"""
import pathlib

from fontTools.ttLib import TTFont
from fontTools.varLib import instancer

FONTS = pathlib.Path(__file__).resolve().parent
SOURCE = FONTS / "GoogleSansCode[MONO,wght].ttf"
# MONO=0 selects the proportional design used for card lettering.
FACES = {"GoogleSansCodeProportional-Regular.ttf": 400,
         "GoogleSansCodeProportional-Medium.ttf": 500,
         "GoogleSansCodeProportional-Bold.ttf": 700}

for name, weight in FACES.items():
    font = instancer.instantiateVariableFont(
        TTFont(SOURCE, recalcTimestamp=False), {"MONO": 0, "wght": weight})
    # Keep the source's head timestamps so reruns reproduce identical bytes.
    font.recalcTimestamp = False
    font.save(FONTS / name)
