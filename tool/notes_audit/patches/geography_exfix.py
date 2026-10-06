"""geography: real whys for 'The textbook states this' items, self-contained versions of questions that relied on a missing contour map, real 6.3 map reduction notes."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from patch import *

def q(B, uid, qid):
    for x in B.unit(uid)['exercise']['questions']:
        if x.get('id') == qid:
            return x
    raise KeyError(qid)

B = Book('geography_11')
q(B, 'geo11-u3', 'geo11-u3-q05')['why'] = ["True. Waves keep eroding headlands and cliffs in some places and depositing sand and shingle in others, so a coastline is never fixed — like the rest of the earth's surface, it changes all the time."]
q(B, 'geo11-u3', 'geo11-u3-q06')['why'] = ["True. Where waves and currents drop more material than they remove, sand, gravel, pebbles and broken shells build up as beaches, spits and bars, so the land advances into the sea."]
q(B, 'geo11-u3', 'geo11-u3-q07')['why'] = ["True. Erosion by hydraulic action, abrasion, attrition and solution cuts cliffs; alternating hard and soft rock gives headlands and bays; attack on lines of weakness makes caves, which grow into blowholes, arches and finally stacks."]
q(B, 'geo11-u3', 'geo11-u3-q08')['why'] = ["True. Depositional features are built of material dropped by waves: beaches (in bays), spits (sand ridges joined to the land at one end), bars (ridges across a bay) and tombolos (ridges joining an island to the mainland)."]
q(B, 'geo11-u5', 'geo11-u5-q08')['why'] = ["True. People depend on their environment and change it: they clear forests for farms and fuel, build roads, dams and settlements, and so alter vegetation, soils, drainage and even climate."]
x = q(B, 'geo11-u8', 'geo11-u8-q08')
x.update(q='On a contour map with a 100 m interval, point E lies inside three closed loops that are themselves inside the 1600 m contour; points C, H and P lie inside only one or two closed loops inside the same contour, and G lies on a saddle between two hills. Which point is highest?',
         why=['Each closed loop inside the 1600 m contour adds one interval (100 m). E is inside three more loops, so it is above 1900 m (1700, 1800, 1900).',
              'C, H and P have fewer loops, so they are lower hills; a saddle (G) is a low point between two hills.', 'Answer: B (E).'],
         similar=[{'q': 'On a contour map, the contours around point D are labelled 300 m, while the contours near points A, B, J and M are labelled 500–800 m. Which point is lowest?  A) Point A  B) Point B  C) Point D  D) Point J  E) Point M',
                   'a': 'C. Point D — it lies at the lowest contour value (about 300 m). Answer: C.'}])
q(B, 'geo11-u8', 'geo11-u8-q07')['similar'] = [{'q': 'Closed contours that get higher towards the centre show  A) a depression  B) a hill or peak  C) a valley  D) a gentle slope  E) a plain', 'a': 'B. a hill or peak — closed loops rising inwards mark a summit.'}]
B.save()

B = Book('geography_12')
q(B, 'geo12-u7', 'geo12-u7-q07')['why'] = ['True. Eritrea has nine recognised ethnic groups — Tigrinya, Tigre, Saho, Kunama, Rashaida, Bilen, Afar, Nara and Hidarb. They are unevenly distributed: Tigrinya mainly in the highlands (Maekel, Debub), Tigre in the north and west lowlands, Afar along the Southern Red Sea coast, Kunama and Nara in Gash-Barka, and so on.']
q(B, 'geo12-u7', 'geo12-u7-q08')['why'] = ["True. The Pygmoid people are regarded as the earliest inhabitants of Eritrea; Nilotic, Hamitic (Kushitic) and later Semitic groups came afterwards and mixed with them, so all the present families share this root."]
B.save()

B = Book('geography_9')
q(B, 'geo9-u6', 'geo9-u6-q01')['similar'] = [{'q': 'A map has a scale of 1:50,000. Its statement scale is  A) One centimetre to ½ of a kilometre  B) One centimetre to 1 kilometre  C) One centimetre to 2 kilometres  D) One centimetre to 5 kilometres  E) One centimetre to 50 kilometres',
    'a': 'A. One centimetre to ½ of a kilometre — 50,000 cm = 500 m = ½ km. Answer: A.', 'exam_question': 'geo-2018-matric-p1-q72'}]
q(B, 'geo9-u6', 'geo9-u6-q03')['similar'] = [{'q': 'On a map of scale 1:50,000, the map distance between points E and M is 14 cm. What is the ground distance?  A) 3 ½ km  B) 7 km  C) 10 ½ km  D) 14 km  E) 21 km',
    'a': 'B. 7 km — 1 cm = 0.5 km, so 14 cm × 0.5 km = 7 km. Answer: B.', 'exam_question': 'geo-2018-matric-p1-q79'}]
B.set('geo9-u6-c05', title='6.3 Map reduction or enlargement', src='notes', body=[
 "Maps often have to be made **smaller (reduced)** or **larger (enlarged)** — for a report, a wall map or to fit a page. When a map is redrawn at a different size, **its scale changes**, so the new scale must be worked out and written on the new map.",
 "**Linear change:** if the length and width are made *k* times as long, the new RF denominator = old denominator ÷ *k*. Example: enlarging a 1:50,000 map **two times** (lengths doubled) gives **1:25,000**; reducing it to **half** the length gives **1:100,000**.",
 "**Area change:** areas change by the square of the linear factor. A map enlarged 2 times in length covers 2² = **4 times** the paper area; reduced to ½ the length it covers ¼ of the area. If a question says the *area* is doubled, the lengths change by √2 ≈ 1.41.",
 "**Methods:** (1) the **square (grid) method** — draw a grid on the original and a grid of larger or smaller squares on the new paper, then copy the detail square by square; (2) the **similar-triangles method**; (3) instruments such as the **pantograph** or a photocopier/computer.",
 "**Remember:** a linear (bar) scale drawn on the map changes size with the map, so it stays correct automatically; an RF or statement scale must be recalculated."], enriched=True)
B.save()
