#!/usr/bin/env python3
"""Parse and display all section IDs and headings from Week5 files."""
import re, os

BASE = "extracted/assets/second task/obstetric/Week5"
files = [
    "Complications_of_3rd_stage_of_labour/36_Third_Stage_Complications.html",
    "Complications_of_3rd_stage_of_labour/37_Amniotic_Fluid_Embolism.html",
    "Complications_of_3rd_stage_of_labour/38_Normal_and_Abnormal_Puerperium.html",
    "Complications_of_3rd_stage_of_labour/39_Puerperal_Sepsis.html",
    "Contracted_pelvis_and_obstructed_labour/34_Obstructed_Labor.html",
    "Contracted_pelvis_and_obstructed_labour/35_Contracted_Pelvis.html",
    "Revision_and_common_obstetric_complaints/44_Fetal_Birth_Injuries.html",
]

for fname in files:
    path = os.path.join(BASE, fname)
    print(f"=== {fname.split('/')[-1]} ===")
    with open(path, encoding='utf-8') as f:
        html = f.read()
    # Find section elements with id
    pattern = re.compile(
        r'<(section|div)(?:\s+class="[^"]*")?\s+id="([^"]*)"(?:\s+class="[^"]*")?>\s*'
        r'<h[234][^>]*>(.*?)</h[234]>', re.DOTALL
    )
    for m in pattern.finditer(html):
        tag = m.group(1)
        sid = m.group(2)
        heading = re.sub(r'<[^>]+>', '', m.group(3)).strip()
        print(f"  [{tag}] id={sid!r}: {heading}")
    print()
