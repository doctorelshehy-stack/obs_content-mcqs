#!/usr/bin/env python3
"""
Process 7 Week 3 Malpresentation files by injecting MCQs.
Reads from extracted/, writes to enhanced-assets/.
"""
import sys, os, json, re, shutil

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from inject_mcqs import process_file

BASE = "extracted/assets/second task/obstetric/Week3"
ENH = "enhanced-assets/second task/obstetric/Week3"
SUBDIR = "Malpresentations_OP_face_breech_cord"

SRC = os.path.join(BASE, SUBDIR)
DST = os.path.join(ENH, SUBDIR)

# Ensure destination exists
os.makedirs(DST, exist_ok=True)

##############################################################
# MCQ DATA for each file
# Format: {section_id: [{'q': '...', 'options': [...], 'correct': N, 'explain': '...'}, ...]}
##############################################################

MCQ_DATA = {}

# ---- File 22: Occipitoposterior Position ----
MCQ_DATA["22_Occipitoposterior_Position.html"] = {
    "s2": [
        {
            "q": "What is the most common fetal malposition?",
            "options": ["Face presentation", "Brow presentation", "Occipitoposterior position", "Breech presentation"],
            "correct": 2,
            "explain": "Occipitoposterior (OP) position is the most common fetal malposition. It is a vertex presentation in which the fetal back is directed posteriorly."
        },
        {
            "q": "In occipitoposterior position, the fetal back is directed:",
            "options": ["Anteriorly", "Posteriorly", "Laterally", "Superiorly"],
            "correct": 1,
            "explain": "In OP position, the fetal back is directed posteriorly (baby's back toward the mother's back), also called 'sunny-side up'."
        },
    ],
    "s3": [
        {
            "q": "Which of the following is a fetal cause of occipitoposterior position?",
            "options": ["Android pelvis", "Pendulous abdomen", "Prematurity", "Placenta previa"],
            "correct": 2,
            "explain": "Prematurity is a fetal cause of OP position. Android pelvis, pendulous abdomen, and placenta previa are maternal causes."
        },
        {
            "q": "Which pelvic shapes predispose to occipitoposterior position?",
            "options": ["Gynecoid and platypelloid", "Android and anthropoid", "Android and gynecoid", "Anthropoid and platypelloid"],
            "correct": 1,
            "explain": "Android and anthropoid pelvis shapes predispose to OP position due to their narrowed anterior pelvic architecture."
        },
    ],
    "s4": [
        {
            "q": "In Right Occipitoposterior (ROP) position, the occiput is placed over the:",
            "options": ["Left sacroiliac joint", "Right sacroiliac joint", "Sacrum", "Symphysis pubis"],
            "correct": 1,
            "explain": "In Right O.P., the occiput is placed over the right sacroiliac joint. ROP is more common than left OP."
        },
        {
            "q": "Which of the following is NOT one of the four named positions of OP?",
            "options": ["Left O.P.", "Right O.P.", "Direct O.P.", "Oblique O.P."],
            "correct": 3,
            "explain": "The four named positions are: Left O.P., Right O.P., Direct O.P., and Occipito transverse. Oblique O.P. is not a named position."
        },
    ],
    "s5": [
        {
            "q": "What is the incidence of OP position at the onset of labor?",
            "options": ["About 5%", "About 10%", "About 15%", "About 20%"],
            "correct": 1,
            "explain": "At the onset of labor, the incidence of OP position is about 10%."
        },
        {
            "q": "Right OP is more common than left OP due to:",
            "options": ["Sinistrorotation of the uterus", "Dextrorotation of the uterus and presence of sigmoid colon on the left", "Asymmetry of the pelvic inlet", "Fetal cardiac position"],
            "correct": 1,
            "explain": "Right OP is more common due to dextrorotation (rightward rotation) of the uterus and the presence of the sigmoid colon on the left side, which deflects the fetal occiput to the right."
        },
    ],
    "s6": [
        {
            "q": "On abdominal examination of a patient with OP position, the abdomen typically appears:",
            "options": ["Distended above the umbilicus", "Flat below the level of the umbilicus", "Globular and tense", "Irregular contour"],
            "correct": 1,
            "explain": "In OP position, the abdomen appears flat below the level of the umbilicus on inspection because the fetal back is posterior."
        },
        {
            "q": "Where are fetal heart sounds best heard in OP position?",
            "options": ["In the midline", "Near the flanks", "Above the umbilicus", "Deep in the suprapubic region"],
            "correct": 1,
            "explain": "In OP position, FHS are heard near the flanks (the fetal back is posterior and away from the maternal abdominal wall)."
        },
    ],
    "s7": [
        {
            "q": "What is the most common outcome of the mechanism of labor in OP position?",
            "options": ["Persistent OP (3%)", "Deep transverse arrest (1%)", "Long anterior rotation (90%)", "Direct OP face-to-pubis (6%)"],
            "correct": 2,
            "explain": "Long anterior rotation (90%) is the most common outcome. The head rotates 3/8 of a circle (135°) anteriorly to become direct occipito-anterior."
        },
        {
            "q": "Which mechanism of labor in OP position leads to obstructed labor when no rotation occurs?",
            "options": ["Long anterior rotation", "Direct OP face-to-pubis", "Persistent OP", "Deep transverse arrest"],
            "correct": 2,
            "explain": "Persistent OP (3%) occurs when no rotation occurs, leading to obstructed labor. Deep transverse arrest (1%) also leads to obstructed labor."
        },
    ],
    "s8": [
        {
            "q": "During the first stage of labor in OP position, which of the following is recommended?",
            "options": ["Frequent P.V. examinations", "Avoid uterine inertia", "Rupture membranes early", "Apply vacuum extraction"],
            "correct": 1,
            "explain": "Recommendations during first stage include: avoid unnecessary P.V. examinations, avoid uterine inertia, evacuate the bladder and rectum, avoid PROM, and maintain close maternal and fetal observation."
        },
        {
            "q": "In direct occipitoposterior position delivering face-to-pubis, what is recommended to avoid perineal laceration?",
            "options": ["Vacuum extraction", "Forceps rotation", "Episiotomy", "Fundal pressure"],
            "correct": 2,
            "explain": "Episiotomy is done in direct OP to avoid perineal laceration when the head delivers face-to-pubis, as the wider occipito-frontal diameter stretches the perineum."
        },
    ],
    "s9": [
        {
            "q": "Which of the following is a maternal complication of OP position?",
            "options": ["Fetal hypoxia", "Skull fracture", "Rupture uterus", "Cord around the neck"],
            "correct": 2,
            "explain": "Maternal complications of OP position include: early PROM, cord prolapse, prolonged labor, obstructed labor, vaginal tears, cervical tears, and rupture uterus."
        },
        {
            "q": "A fetal skull fracture in OP position can occur due to impingement of which fetal bone against the ischial spine?",
            "options": ["Occipital bone", "Right parietal bone", "Left parietal bone", "Frontal bone"],
            "correct": 2,
            "explain": "In OP position, the fetal left parietal bone can be pressed against the maternal ischial spine during descent, leading to iatrogenic neonatal skull fracture."
        },
    ],
}

# ---- File 23: Face Presentation ----
MCQ_DATA["23_Face_Presentation.html"] = {
    "sec2": [
        {
            "q": "In face presentation, what is the presenting part?",
            "options": ["The occiput", "The vertex", "The chin (mentum)", "The brow"],
            "correct": 2,
            "explain": "In face presentation, the head is hyperextended so that the occiput touches the fetal back and the chin (mentum) becomes the presenting part."
        },
        {
            "q": "What is the denominator in face presentation?",
            "options": ["Occiput", "Sacrum", "Mentum (chin)", "Frontal bone"],
            "correct": 2,
            "explain": "The denominator in face presentation is the mentum (chin), not the occiput."
        },
    ],
    "sec3": [
        {
            "q": "Which of the following is a cause specific to face presentation (not shared with OP position)?",
            "options": ["Prematurity", "Android pelvis", "Neck tumors", "Polyhydramnios"],
            "correct": 2,
            "explain": "Neck tumors, cystic hygroma, and large fetal thyroid gland are specific causes of face presentation as they physically prevent head flexion by occupying space in the fetal neck."
        },
    ],
    "sec4": [
        {
            "q": "In mentoposterior position, the mentum is oriented toward the:",
            "options": ["Symphysis pubis", "Sacrum", "Left iliac fossa", "Right iliac fossa"],
            "correct": 1,
            "explain": "In mentoposterior (MP) position, the mentum is oriented toward the posterior pelvis (sacrum). This is generally unfavorable and often requires cesarean section."
        },
        {
            "q": "How many named positions does face presentation have?",
            "options": ["2 groups with 8 total variants", "3 groups with 8 total variants", "3 groups with 7 total variants", "4 groups with 8 total variants"],
            "correct": 1,
            "explain": "Face presentation has 3 groups (Mentoanterior, Mentoposterior, Mentotransverse) with a total of 8 named positions (Direct MA, RMA, LMA, Direct MP, RMP, LMP, RMT, LMT)."
        },
    ],
    "sec5": [
        {
            "q": "Primary face presentation is present:",
            "options": ["Only during the second stage", "During pregnancy", "During labor only", "After membrane rupture"],
            "correct": 1,
            "explain": "Primary face presentation is present during pregnancy, usually due to fetal causes. Secondary face presentation occurs during labor, commonly due to contracted pelvis or pendulous abdomen."
        },
    ],
    "sec6": [
        {
            "q": "On vaginal examination in face presentation, which structures are felt?",
            "options": ["Occiput and sagittal suture", "Mouth, nose, orbital bones and chin", "Frontal bone and anterior fontanelle", "Sacrum and coccyx"],
            "correct": 1,
            "explain": "On PV examination in face presentation, the mouth, nose, orbital bones and chin are felt. The mouth and anus can be confused — the mouth and malar eminences form a triangle, while the ischial tuberosities and anus are in a straight line."
        },
    ],
    "sec7": [
        {
            "q": "What is the engaging diameter in face presentation (mentoanterior)?",
            "options": ["Occipito-frontal diameter (11.5 cm)", "Submento-bregmatic diameter (9.5 cm)", "Mento-vertical diameter (13.75 cm)", "Biparietal diameter (9.5 cm)"],
            "correct": 1,
            "explain": "In mentoanterior position, the head engages by the submento-bregmatic diameter (9.5 cm). This is the favorable diameter that allows vaginal delivery."
        },
        {
            "q": "In the absence of long anterior rotation in mentoposterior position, labor becomes:",
            "options": ["Accelerated", "Obstructed", "Precipitous", "Unchanged"],
            "correct": 1,
            "explain": "In the absence of long anterior rotation, labor becomes obstructed and usually cesarean section is the only safe option."
        },
    ],
    "sec8": [
        {
            "q": "Which of the following is contraindicated in face presentation?",
            "options": ["Large episiotomy", "Forceps extraction for mentoanterior", "Vacuum extractor", "Epidural analgesia"],
            "correct": 2,
            "explain": "Vacuum extractor is contraindicated in face presentation because the vacuum cup cannot be applied to a face (no scalp, no firm engagement surface)."
        },
        {
            "q": "What should NOT be attempted in face presentation?",
            "options": ["Wait for spontaneous rotation", "Convert face to vertex presentation", "Epidural analgesia", "Forceps in mentoanterior"],
            "correct": 1,
            "explain": "Do not try to convert face to vertex presentation. Internal version/manual conversion is contraindicated as it can cause uterine rupture, cord prolapse, and fetal trauma."
        },
    ],
}

# ---- File 24: Brow Presentation ----
MCQ_DATA["24_Brow_Presentation.html"] = {
    "definition": [
        {
            "q": "Brow presentation is a cephalic presentation in which the fetal head is:",
            "options": ["Fully flexed", "Fully extended", "Midway between flexion and extension", "Laterally rotated"],
            "correct": 2,
            "explain": "Brow presentation is a cephalic presentation in which the fetal head is midway between flexion and extension."
        },
    ],
    "causes": [
        {
            "q": "The causes of brow presentation are similar to those of:",
            "options": ["Face presentation", "Breech presentation", "Occipitoposterior position", "Compound presentation"],
            "correct": 2,
            "explain": "The causes of brow presentation are the same as those of occipitoposterior position."
        },
    ],
    "denominator": [
        {
            "q": "What is the denominator in brow presentation?",
            "options": ["Occiput", "Mentum", "Sacrum", "Frontal bone"],
            "correct": 3,
            "explain": "In brow presentation, the frontal bone is the denominator (reference point for describing position)."
        },
    ],
    "positions": [
        {
            "q": "How many named positions are recognized in brow presentation?",
            "options": ["2 (frontoanterior and frontoposterior) with 4 variants", "3 (as in face presentation)", "4 (as in OP position)", "1 (direct brow)"],
            "correct": 0,
            "explain": "Brow presentation has two main position groups: Frontoanterior and Frontoposterior, each with right and left variants (4 named positions total)."
        },
    ],
    "diagnosis": [
        {
            "q": "On vaginal examination in brow presentation, which of the following is felt?",
            "options": ["Chin and mouth", "Occiput and sagittal suture", "Frontal bone, supraorbital ridge, and root of the nose", "Sacrum and coccyx"],
            "correct": 2,
            "explain": "On PV examination in brow presentation, the frontal bone, supraorbital ridge, and root of the nose are felt. The chin is NOT felt — this distinguishes brow from face presentation."
        },
        {
            "q": "The key feature distinguishing brow from face presentation on vaginal examination is:",
            "options": ["The occiput is palpable", "The chin is not felt", "The mouth is felt", "The fontanelles are palpable"],
            "correct": 1,
            "explain": "The chin is NOT felt in brow presentation — that is the single most useful clinical sign separating it from face presentation, where the mentum (chin) is the leading point."
        },
    ],
    "mechanism": [
        {
            "q": "Why is brow presentation essentially incompatible with vaginal delivery?",
            "options": ["The biparietal diameter is too large", "The engaging mento-vertical diameter (13.75 cm) exceeds all pelvic inlet diameters", "The head is too flexed", "The head is too extended"],
            "correct": 1,
            "explain": "The engaged diameter is the mento-vertical diameter (13.75 cm), which is longer than any diameter of the female pelvic inlet, making labor obstructed from the start."
        },
        {
            "q": "What is the mento-vertical diameter in brow presentation?",
            "options": ["9.5 cm", "11.0 cm", "13.75 cm", "12.5 cm"],
            "correct": 2,
            "explain": "The mento-vertical diameter is 13.75 cm, measured from the chin (mentum) to the most distant point on the vertex (crown)."
        },
    ],
    "management": [
        {
            "q": "What is the standard management for brow presentation?",
            "options": ["Vacuum extraction", "Forceps delivery", "Cesarean section", "Manual rotation to vertex"],
            "correct": 2,
            "explain": "Cesarean section is the only safe option for brow presentation because the mento-vertical diameter (13.75 cm) cannot pass through the pelvic inlet."
        },
    ],
    "complications": [
        {
            "q": "Which complication is a constant risk in brow presentation?",
            "options": ["Uterine atony", "Shoulder dystocia", "Cord prolapse", "Postpartum hemorrhage"],
            "correct": 2,
            "explain": "Cord prolapse is a constant risk in brow presentation because the presenting part does not fit the pelvic inlet, leaving space for the cord to descend."
        },
    ],
}

# ---- File 25: Compound Presentation ----
MCQ_DATA["25_Compound_Presentation.html"] = {
    "s2": [
        {
            "q": "What is the definition of compound presentation?",
            "options": ["Breech with extended legs", "Cephalic presentation with a prolapsed limb beside the presenting part", "Transverse lie with prolapsed cord", "Face presentation with extended neck"],
            "correct": 1,
            "explain": "Compound presentation is a cephalic presentation in which a limb (usually upper limb, less commonly lower limb) prolapses beside the presenting part."
        },
    ],
    "s3": [
        {
            "q": "Which of the following is a cause of compound presentation?",
            "options": ["Fetal macrosomia", "Prematurity", "Oligohydramnios", "Vertex presentation"],
            "correct": 1,
            "explain": "Prematurity is a cause of compound presentation. Other causes include PROM, polyhydramnios, multiparity, contracted pelvis, pelvic tumors, and twins."
        },
        {
            "q": "How many etiologic factors for compound presentation does the source list?",
            "options": ["5", "6", "7", "8"],
            "correct": 2,
            "explain": "The source lists 7 etiologic factors: prematurity, PROM, polyhydramnios, multiparity, contracted pelvis, pelvic tumors, and twins — all create extra room at the pelvic inlet."
        },
    ],
    "s4": [
        {
            "q": "How is compound presentation definitively diagnosed?",
            "options": ["Abdominal ultrasound only", "Vaginal examination showing prolapsed limb beside the presenting part", "X-ray pelvimetry", "Leopold's maneuvers alone"],
            "correct": 1,
            "explain": "Compound presentation is definitively diagnosed on PV examination when the prolapsed limb is felt beside the presenting part."
        },
    ],
    "s5": [
        {
            "q": "What is the conservative management for compound presentation?",
            "options": ["Immediate cesarean section", "Forceps delivery", "Gently reduce the prolapsed limb and push the head down", "Vacuum extraction"],
            "correct": 2,
            "explain": "The conservative step is to gently try to reduce the prolapsed limb upward above the pelvic brim and hold it till contraction, then push the head down into the pelvis."
        },
        {
            "q": "Which of the following is an indication for cesarean section in compound presentation?",
            "options": ["Presence of any limb prolapse", "Maternal request", "Abnormal FHR pattern", "Primigravida"],
            "correct": 2,
            "explain": "CS is indicated in compound presentation if any of the following develops: abnormal FHR pattern, cord prolapse, or poor progress of labor."
        },
    ],
}

# ---- File 26: Breech Presentation ----
MCQ_DATA["26_Breech_Presentation.html"] = {
    "s2": [
        {
            "q": "What is the incidence of breech presentation at term?",
            "options": ["1-2% of deliveries", "3-4% of all deliveries", "5-6% of deliveries", "10% of deliveries"],
            "correct": 1,
            "explain": "Breech presentation occurs in 3-4% of all deliveries. It is the most common malpresentation at term."
        },
    ],
    "s3": [
        {
            "q": "Which of the following is a predisposing factor for breech presentation?",
            "options": ["Gynecoid pelvis", "Vertex presentation in previous pregnancy", "Prematurity", "Prolonged pregnancy"],
            "correct": 2,
            "explain": "Predisposing factors include: prematurity, uterine malformations/fibroids, polyhydramnios, placenta previa, fetal abnormalities, multiple gestations, cord around the neck, and pelvic tumors."
        },
        {
            "q": "The accommodation theory for breech presentation states that:",
            "options": ["The fetus always prefers breech", "The fetus adapts to the pyriform shape of the uterus with buttocks in fundus and head in lower segment", "Breech is caused by uterine contractions", "The fetal head is always larger than the pelvis"],
            "correct": 1,
            "explain": "The accommodation theory states that the fetus is usually adapted to the pyriform shape of the uterus with the large buttock in the fundus and the smaller head in the lower uterine segment."
        },
    ],
    "s4": [
        {
            "q": "Which type of breech is most common?",
            "options": ["Complete breech", "Frank breech", "Footling breech", "Incomplete breech"],
            "correct": 1,
            "explain": "Frank breech is the most common type of breech presentation."
        },
    ],
    "s5": [
        {
            "q": "What is the denominator in breech presentation?",
            "options": ["Occiput", "Mentum", "Sacrum", "Scapula"],
            "correct": 2,
            "explain": "In breech presentation, the sacrum is the denominator (reference point) for describing the position."
        },
    ],
    "s6": [
        {
            "q": "On abdominal palpation of a breech presentation, the head is felt:",
            "options": ["In the fundus", "At the pelvic inlet", "In the flank", "At the level of the umbilicus"],
            "correct": 0,
            "explain": "In breech presentation, the head is felt in the fundus (the upper part of the uterus), while the buttocks are at the pelvic inlet."
        },
    ],
    "s8": [
        {
            "q": "In the mechanism of labor for breech presentation, which part delivers first?",
            "options": ["The head", "The shoulders", "The breech (buttocks)", "The trunk"],
            "correct": 2,
            "explain": "In breech labor, the breech (buttocks) delivers first, followed by the trunk, shoulders, and finally the head."
        },
    ],
    "s9": [
        {
            "q": "Which maneuver is used to deliver the aftercoming head in breech delivery?",
            "options": ["McRoberts' maneuver", "Mauriceau-Smellie-Veit (MSV) maneuver", "Kristeller maneuver", "Zavanelli maneuver"],
            "correct": 1,
            "explain": "The Mauriceau-Smellie-Veit (MSV) maneuver is a method to deliver the aftercoming head in breech delivery."
        },
    ],
    "s10": [
        {
            "q": "External Cephalic Version (ECV) is best performed at what gestational age?",
            "options": ["32-34 weeks", "36-37 weeks", "38-40 weeks", "After 40 weeks"],
            "correct": 1,
            "explain": "ECV is typically performed at 36-37 weeks gestation to convert a breech to a cephalic presentation."
        },
    ],
    "s11": [
        {
            "q": "Which of the following is a contraindication to vaginal breech delivery?",
            "options": ["Frank breech", "Flexed fetal head on ultrasound", "Footling breech", "Estimated fetal weight of 3000g"],
            "correct": 2,
            "explain": "Footling breech is generally a contraindication to vaginal breech delivery due to risk of cord prolapse and entrapment."
        },
    ],
    "s12": [
        {
            "q": "What is the purpose of the Løvset maneuver in breech delivery?",
            "options": ["To deliver the head", "To deliver the shoulders and arms", "To rotate the trunk", "To flex the fetal head"],
            "correct": 1,
            "explain": "The Løvset maneuver is used for delivery of the shoulders and arms in breech delivery."
        },
    ],
    "s13": [
        {
            "q": "The Løvset maneuver is specifically used for:",
            "options": ["Delivery of the aftercoming head", "Arm delivery in breech", "External rotation", "Version of transverse lie"],
            "correct": 1,
            "explain": "The Løvset maneuver is specifically used for arm delivery (delivery of shoulders and arms) during breech delivery."
        },
    ],
    "s14": [
        {
            "q": "Piper forceps are specifically designed for:",
            "options": ["Rotation of OP position", "Delivery of the aftercoming head in breech", "Mid-cavity rotational delivery", "Outlet forceps in vertex"],
            "correct": 1,
            "explain": "Piper forceps are specifically designed for delivery of the aftercoming head in breech delivery."
        },
    ],
    "s15": [
        {
            "q": "Piper forceps are applied after delivery of which parts?",
            "options": ["After delivery of the head only", "After delivery of the trunk and arms", "After full delivery of the fetus", "Before any part delivers"],
            "correct": 1,
            "explain": "Piper forceps are applied to the aftercoming head after the trunk and arms have been delivered."
        },
    ],
    "s16": [
        {
            "q": "Which of the following is a complication of vaginal breech delivery?",
            "options": ["Face presentation", "Cord prolapse", "Polyhydramnios", "Placenta previa"],
            "correct": 1,
            "explain": "Complications of vaginal breech delivery include cord prolapse, head entrapment, nuchal arm, and birth injuries."
        },
    ],
    "s17": [
        {
            "q": "Total breech extraction involves:",
            "options": ["Allowing spontaneous delivery of the breech", "Pulling on the feet to deliver the entire fetus", "Using forceps to extract the head first", "Performing ECV before delivery"],
            "correct": 1,
            "explain": "Total breech extraction involves the operator pulling on the fetal feet to extract the entire fetus. It is rarely performed today due to high risk of trauma."
        },
    ],
    "s18": [
        {
            "q": "Which of the following is an indication for cesarean section in breech presentation?",
            "options": ["Frank breech in a multiparous woman", "Estimated fetal weight > 3800g", "Flexed fetal head", "Adequate pelvis on pelvimetry"],
            "correct": 1,
            "explain": "Indications for CS in breech include estimated fetal weight > 3800g (macrosomia), hyperextended head, footling breech, and inadequate pelvis."
        },
    ],
    "s19": [
        {
            "q": "Complicated breech delivery includes all EXCEPT:",
            "options": ["Head entrapment", "Nuchal arm", "Frank breech with flexed head", "Cord prolapse"],
            "correct": 2,
            "explain": "Frank breech with a flexed head and adequate pelvis may be suitable for vaginal delivery. Complicated breech includes head entrapment, nuchal arm, and cord prolapse."
        },
    ],
}

# ---- File 27: Shoulder Presentation ----
MCQ_DATA["27_Shoulder_Presentation.html"] = {
    "s2": [
        {
            "q": "In shoulder presentation (transverse lie), the fetal vertebral column is:",
            "options": ["Parallel to the maternal spine", "Perpendicular to the maternal spine", "At a 45° angle to the maternal spine", "In the same axis as the maternal spine"],
            "correct": 1,
            "explain": "In shoulder presentation, the fetus is in a transverse lie with its vertebral column perpendicular to that of the mother."
        },
    ],
    "s3": [
        {
            "q": "Which is the most common predisposing factor for shoulder presentation?",
            "options": ["Primigravida", "Grand multiparity", "Gynecoid pelvis", "Oligohydramnios"],
            "correct": 1,
            "explain": "Grand multiparity (5 or more deliveries) with lax abdominal musculature is the most common predisposing factor for shoulder presentation."
        },
        {
            "q": "How many predisposing factors for shoulder presentation does the source list?",
            "options": ["6", "7", "8", "9"],
            "correct": 2,
            "explain": "The source lists 8 predisposing factors: grand multiparity, uterine abnormalities, twin pregnancy, uterine overdistension (polyhydramnios), prematurity/small fetus, fetal malformation, placenta previa, and feto-pelvic disproportion."
        },
    ],
    "s5": [
        {
            "q": "What is the denominator in shoulder presentation?",
            "options": ["Acromion", "Scapula (Sc)", "Humerus", "Clavicle"],
            "correct": 1,
            "explain": "In shoulder presentation, the scapula (Sc) is the denominator — analogous to the occiput in cephalic and the sacrum in breech."
        },
        {
            "q": "Which is the most common position in shoulder presentation?",
            "options": ["RScA (Right Scapulo-Anterior)", "LScA (Left Scapulo-Anterior)", "RScP (Right Scapulo-Posterior)", "LScP (Left Scapulo-Posterior)"],
            "correct": 1,
            "explain": "Left scapulo-anterior (LScA) is the commonest position for shoulder presentation."
        },
    ],
    "s6": [
        {
            "q": "On auscultation in shoulder presentation, the fetal heart is best heard:",
            "options": ["In the lower quadrants", "At the umbilical level", "In the flanks", "Deep in the pelvis"],
            "correct": 1,
            "explain": "In shoulder presentation, the fetal heart is heard at the umbilical level."
        },
    ],
    "s7": [
        {
            "q": "What is the initial management for shoulder presentation before labor?",
            "options": ["Immediate CS", "ECV (External Cephalic Version)", "Expectant management", "Induction of labor"],
            "correct": 1,
            "explain": "Before labor or early in labor with intact membranes, ECV may be attempted to convert the transverse lie to a longitudinal lie."
        },
    ],
    "s8": [
        {
            "q": "In singleton pregnancy with transverse lie in labor, the management is:",
            "options": ["ECV", "Vaginal breech delivery", "Cesarean section", "Forceps delivery"],
            "correct": 2,
            "explain": "For singleton pregnancy with transverse lie in labor, cesarean section is the standard management."
        },
    ],
    "s9": [
        {
            "q": "In twin pregnancy, transverse lie of the second twin is managed by:",
            "options": ["Elective CS for both twins", "ECV after delivery of first twin, then vaginal delivery", "Immediate CS of second twin only", "Forceps delivery"],
            "correct": 1,
            "explain": "In twin pregnancy with transverse lie of the second twin, ECV (or internal podalic version) can be performed after delivery of the first twin, followed by vaginal delivery."
        },
    ],
    "s10": [
        {
            "q": "What is the safest mode of delivery for a term singleton with shoulder presentation?",
            "options": ["Vaginal delivery with ECV", "Cesarean section", "Internal podalic version", "Vacuum extraction"],
            "correct": 1,
            "explain": "Cesarean section is the safest mode of delivery for a term singleton with shoulder presentation."
        },
    ],
    "s11": [
        {
            "q": "'Neglected shoulder' refers to:",
            "options": ["Early diagnosis of transverse lie", "A transverse lie that has been allowed to labor for hours after membrane rupture", "A shoulder that delivers spontaneously", "Successful ECV"],
            "correct": 1,
            "explain": "Neglected shoulder is a transverse lie that has been allowed to labor for many hours after rupture of membranes, leading to uterine exhaustion and risk of rupture."
        },
        {
            "q": "What is a key complication of neglected shoulder presentation?",
            "options": ["Cord prolapse", "Uterine rupture", "Polyhydramnios", "Placental abruption"],
            "correct": 1,
            "explain": "Uterine rupture is a key complication of neglected shoulder presentation due to prolonged obstructed labor."
        },
    ],
    "s12": [
        {
            "q": "Internal podalic version is a maneuver to:",
            "options": ["Convert breech to cephalic", "Grasp the fetal feet and convert transverse lie to a breech for extraction", "Rotate the fetal head in OP position", "Deliver the placenta manually"],
            "correct": 1,
            "explain": "Internal podalic version is a maneuver in which the operator's hand enters the uterus, grasps the fetal feet, and converts a transverse lie to a breech for extraction."
        },
    ],
}

# ---- File 28: Cord Presentation and Prolapse ----
MCQ_DATA["28_Cord_Presentation_and_Prolapse.html"] = {
    "s2": [
        {
            "q": "What is the difference between cord presentation and cord prolapse?",
            "options": ["Cord presentation occurs in breech, cord prolapse in cephalic", "Cord presentation: cord below presenting part with INTACT membranes. Cord prolapse: after membrane RUPTURE", "Cord presentation is diagnosed by ultrasound only", "There is no difference — they are the same condition"],
            "correct": 1,
            "explain": "Cord presentation = presence of umbilical cord below the presenting part with intact membranes. Cord prolapse = cord below the presenting part after rupture of membranes."
        },
    ],
    "s4": [
        {
            "q": "How many risk factors for cord prolapse does the source enumerate?",
            "options": ["7", "8", "9", "10"],
            "correct": 3,
            "explain": "The source lists 10 risk factors for cord prolapse: prematurity, fetal congenital abnormality, second twin, multiparity, low birth weight (< 2.5 kg), non-cephalic presentations, CPD, low-lying placenta/long cord, polyhydramnios, and macrosomia."
        },
        {
            "q": "Which of the following is a risk factor for cord prolapse?",
            "options": ["Gynecoid pelvis", "Cephalic presentation with engaged head", "Polyhydramnios", "Primigravida"],
            "correct": 2,
            "explain": "Polyhydramnios is a risk factor for cord prolapse because excess amniotic fluid can wash the cord out when membranes rupture."
        },
    ],
    "s5": [
        {
            "q": "What clinical sign indicates fetal viability in cord prolapse?",
            "options": ["Presence of fetal movements", "Pulsating cord", "Amniotic fluid color", "Uterine contractions"],
            "correct": 1,
            "explain": "If the cord is pulsating, the fetus is alive. If the cord is not pulsating, the fetus is likely dead."
        },
    ],
    "s6": [
        {
            "q": "If cord prolapse is diagnosed with the fetus alive and cervix fully dilated, the management is:",
            "options": ["Immediate cesarean section", "Replace the cord and await spontaneous delivery", "Forceps or vacuum delivery (expeditious vaginal delivery)", "Tocolysis and transfer"],
            "correct": 2,
            "explain": "If the cervix is fully dilated and the fetus is alive with cord prolapse, expeditious vaginal delivery (forceps/vacuum) is appropriate."
        },
        {
            "q": "If cord prolapse occurs with a live fetus and an incompletely dilated cervix, the management is:",
            "options": ["Wait for full dilation", "Immediate cesarean section", "Manual replacement of cord", "Pudendal block and trial of forceps"],
            "correct": 1,
            "explain": "When cord prolapse occurs with a live fetus and the cervix is not fully dilated, immediate cesarean section is indicated."
        },
    ],
}

##############################################################
# RUN PROCESSING
##############################################################
print("=" * 70)
print("Processing Week 3 Malpresentation files")
print("=" * 70)

# First, copy files from extracted to enhanced
for fname in sorted(os.listdir(SRC)):
    if fname.endswith(".html"):
        src_path = os.path.join(SRC, fname)
        dst_path = os.path.join(DST, fname)
        shutil.copy2(src_path, dst_path)
        print(f"  Copied {fname}")

print("\nInjecting MCQs...\n")

# Process each file
for fname in sorted(os.listdir(DST)):
    if not fname.endswith(".html"):
        continue
    if fname not in MCQ_DATA:
        print(f"  SKIP {fname} (no MCQ data)")
        continue
    
    dst_path = os.path.join(DST, fname)
    mcq_data = MCQ_DATA[fname]
    
    # Load the file
    with open(dst_path, 'r') as f:
        html = f.read()
    
    # Parse sections 
    from inject_mcqs import parse_headings, build_mcq_block, inject_mcq_after_subtopic
    
    sections = parse_headings(html)
    
    # Skip keywords
    skip_keywords = ['ilos', 'study activity', 'reference', 'questions', 'table of contents',
                     'intended learning', 'contents', 'sources']
    
    # Sections to exclude: figure-only sections
    figure_sections = {
        "26_Breech_Presentation.html": ["s7"],  # Figure · Leopold maneuvers
        "27_Shoulder_Presentation.html": ["s4"],  # Figure · Transverse lie
        "28_Cord_Presentation_and_Prolapse.html": ["s3"],  # Figure · Cord prolapse
        "25_Compound_Presentation.html": ["s6"],  # Figure section
    }
    
    excluded = figure_sections.get(fname, [])
    
    # Process MCQs in REVERSE order
    inserted = 0
    for sec in reversed(sections):
        sec_id = sec['id'].lower()
        sec_hdg = sec['heading'].lower()
        
        # Check skip keywords
        skip = False
        for kw in skip_keywords:
            if kw in sec_id or kw in sec_hdg:
                skip = True
                break
        
        # Check if figure-only section
        if sec['id'] in excluded:
            skip = True
        
        if skip:
            continue
        
        if sec['id'] in mcq_data:
            mcqs = mcq_data[sec['id']]
            if mcqs:
                mcq_html = build_mcq_block(mcqs, sec['id'])
                html = inject_mcq_after_subtopic(html, mcq_html, sec['end'] + 300, sec.get('tag', 'section'))
                inserted += 1
    
    # Inject MCQ CSS before </style>
    from inject_mcqs import MCQ_CSS
    style_end = html.find('</style>')
    if style_end != -1:
        html = html[:style_end] + MCQ_CSS + html[style_end:]
    
    # Inject MCQ JS before </body>
    from inject_mcqs import MCQ_JS
    body_end = html.rfind('</body>')
    if body_end != -1:
        html = html[:body_end] + MCQ_JS + html[body_end:]
    
    # Write back
    with open(dst_path, 'w') as f:
        f.write(html)
    
    print(f"  ✓ {fname} → {inserted} subtopics injected (MCQs in {list(mcq_data.keys())})")

print("\n" + "=" * 70)
print("DONE! All 7 Week 3 Malpresentation files processed.")
print("=" * 70)
