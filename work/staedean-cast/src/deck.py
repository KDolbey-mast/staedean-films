import glob, os, copy
from pptx import Presentation
from pptx.util import Emu
from lxml import etree
from timing import T
NOTES = {
 "S1_01": "Our PM at his desk, clean-shaven, working.", "S1_02": "An idea pops up.", "S1_03": "He sketches it. No, not good.",
 "S1_04": "Over the shoulder, into the bin. Healthy.", "S1_05": "Back to work, happy.", "S1_06": "Another idea.",
 "S1_07": "He weighs it. This one might be worth showing a customer.", "S1_08": "This one. He takes it.",
 "S1_09": "He turns to the window.",
 "S2_01": "Push in on the window.", "S2_02": "MOUNT STAEDEAN. 20,000 m. Every checkpoint, gate and bench on the way up.",
 "S2_03": "He only wanted to test one small idea.", "S2_04": "Off he goes, towards the customer.",
 "S3_01": "First checkpoint. Still hopeful.", "S3_02": "He explains. At length.", "S3_03": "She smiles and points at the ticket machine.",
 "S3_04": "Ticket 087. A very long ticket.", "S3_05": "Please take a seat. Now serving 086.", "S3_06": "Calendar pages fly. He slumps.",
 "S3_07": "Still 086. Cobwebs. Stubble.", "S3_08": "087! A flash of hope.", "S3_09": "Onwards, with paperwork. He has barely moved.",
 "S4_01": "Up the mountain.", "S4_02": "Customer Success: explain it again. One moment, please.", "S4_03": "Please take a seat.",
 "S4_04": "Bench.", "S4_05": "Product Owner: write-up v7. Please take a seat.", "S4_06": "Bench.",
 "S4_07": "Planning. He does not even explain this time.", "S4_08": "Bench, in the snow.",
 "S4_09": "How far has he got? Here.",
 "S5_01": "The fork.", "S5_02": "The ERP road: here be dragons.", "S5_03": "The AI road: a sea monster.",
 "S5_04": "...either way.",
 "S6_01": "Thin air. The bulb is nearly out.", "S6_02": "...", "S6_03": "Oxygen.", "S6_04": "On his belly, the summit in sight.",
 "S7_01": "The summit. The customer.", "S7_02": "He offers the idea.", "S7_03": "\"Who are you?\"",
 "S7_04": "Silence.", "S7_05": "The bulb goes out.",
}
prs = Presentation()
prs.slide_width, prs.slide_height = Emu(12192000), Emu(6858000)
blank = prs.slide_layouts[6]
P = "http://schemas.openxmlformats.org/presentationml/2006/main"
for fp in sorted(glob.glob("cjpg/*.jpg")):
    key = os.path.basename(fp)[:5]
    s = prs.slides.add_slide(blank)
    s.shapes.add_picture(fp, 0, 0, prs.slide_width, prs.slide_height)
    s.notes_slide.notes_text_frame.text = f"{key.replace('_', ' ')}  ({T[key]} s)\n{NOTES[key]}"
    tr = etree.SubElement(s._element, f"{{{P}}}transition")
    tr.set("advTm", str(int(T[key] * 1000)))
    # transition must come right after clrMapOvr
    clr = s._element.find(f"{{{P}}}clrMapOvr")
    if clr is not None:
        clr.addnext(tr)
prs.save("vid/MOUNT_STAEDEAN_storyboard.pptx")
print("slides", len(prs.slides))
