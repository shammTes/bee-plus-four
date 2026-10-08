from common import set_unit, QSet
set_unit('bio11-u3')
a = QSet('3.1.3 Practice — axial and appendicular skeleton', 's313')
a.M(59, 'The axial skeleton consists of', ['80 bones', '126 bones', '206 bones', '60 bones'], 'A',
    ['Step 1: skull 22 + ossicles 6 + hyoid 1 = 29.', 'Step 2: vertebral column 26 + sternum 1 + ribs 24 = 51.', 'Step 3: 29 + 51 = 80.'], 'Axial 80 + appendicular 126 = 206.', [('How many bones are in the appendicular skeleton?', '126.')])
a.M(62, 'The vertebrae that allow nodding and rotation of the head are the', ['lumbar vertebrae', 'atlas and axis', 'sacrum and coccyx', 'thoracic vertebrae'], 'B',
    ['Step 1: the head sits on the neck (cervical) vertebrae.', 'Step 2: C1 atlas → nodding; C2 axis → rotation.'], 'Atlas holds the world (head) — nods; axis is the pivot — turns.', [('In which region are the atlas and axis found?', 'The cervical (neck) region.')])
a.F(62, 'In humans the four caudal vertebrae fuse to form the ____.', 'coccyx', ['coccyx', 'sacrum', 'sternum', 'atlas'],
    ['Step 1: caudal = tail.', 'Step 2: the human tail is vestigial; its 4 vertebrae fuse → coccyx.'], 'Sacrum = 5 sacral fused; coccyx = 4 caudal fused.', [('How many vertebrae fuse to form the sacrum?', 'Five.')])
a.TF(63, 'The clavicle is part of the axial skeleton.', False,
     ['Step 1: the clavicle belongs to the pectoral girdle.', 'Step 2: girdles are appendicular → false.'], 'Girdles go with limbs.', [('True or false: ribs are axial.', 'True.')])
a.S(63, 'Distinguish between true, false and floating ribs.', 'True ribs (upper 7 pairs) join the sternum directly by their own cartilage. False ribs (next 3 pairs) join it indirectly through the cartilage of the rib above. Floating ribs (last 2 pairs) have no attachment to the sternum.',
    ['Step 1: number each kind (7, 3, 2).', 'Step 2: state the type of attachment to the sternum.'], 'Count down: 7 direct, 3 indirect, 2 none.', [('What allows the rib cage to move during breathing?', 'The flexible cartilage joining ribs to the sternum.')])
a.M(64, 'The bone on the thumb side of the forearm is the', ['ulna', 'radius', 'humerus', 'fibula'], 'B',
    ['Step 1: the forearm has radius and ulna.', 'Step 2: the radius is on the thumb side; the ulna forms the elbow.'], 'Radius → rotates with the thumb.', [('Which bone is on the outer, thinner side of the lower leg?', 'The fibula.')])
a.S(65, 'How many phalanges are there in one hand? Show your working.', 'Thumb 2 + four fingers × 3 = 2 + 12 = 14 phalanges.',
    ['Step 1: the thumb has 2 phalanges.', 'Step 2: each of 4 fingers has 3 → 12.', 'Step 3: 2 + 12 = 14.'], 'Same for the foot: big toe 2, others 3.', [('How many bones are in the wrist?', '8 carpals.')])
a.M(63, 'Which is NOT a function of the pelvic girdle?', ['Socket for the femur', 'Protecting the lower abdominal organs', 'Transmitting weight to the legs', 'Allowing a wide range of arm movement'], 'D',
    ['Step 1: the pelvic girdle supports the legs.', 'Step 2: arm movement depends on the pectoral girdle.'], 'Pectoral = arms; pelvic = legs.', [('Which girdle is loosely attached to the sternum?', 'The pectoral girdle.')])
a.S(65, 'Explain why the opposable thumb is important to humans.', 'The thumb metacarpal joins the wrist by a saddle joint, so the thumb can move across the palm and touch the fingertips. This allows a precise grip, so humans can grasp objects, use tools, write and perform skilful operations.',
    ['Step 1: structure — saddle joint.', 'Step 2: movement — opposes the fingers.', 'Step 3: advantage — grasp, tools, skill.'], 'Structure → movement → advantage.', [('Which bones form the palm?', 'The five metacarpals.')])
a.M(62, 'An adult vertebral column contains 26 bones while a child’s contains 33 because in adults', ['some vertebrae are lost', 'sacral and caudal vertebrae fuse', 'cervical vertebrae fuse', 'discs turn into bone'], 'B',
    ['Step 1: child: 7+12+5+5+4 = 33.', 'Step 2: adult: 5 sacral → 1 sacrum, 4 caudal → 1 coccyx.', 'Step 3: 7+12+5+1+1 = 26.'], 'Fusion, not loss.', [('Which region has the largest vertebrae?', 'The lumbar region.')])
a.TF(60, 'Fontanels are soft spots in a baby’s skull that close by about two years of age.', True,
     ['Step 1: at birth the skull bones are not fully joined.', 'Step 2: the gaps (fontanels) close by about 2 years → true.'], 'Fontanels = baby’s soft spots.', [('What type of joint joins adult skull bones?', 'Immovable joints (sutures).')])
QS = a.items
