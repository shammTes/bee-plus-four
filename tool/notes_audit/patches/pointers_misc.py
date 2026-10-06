import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from subs import apply

n = 0
n += apply('agriculture_11', [
 ("According to the etymological definition in the textbook, the word", "The word"),
 ("The textbook explicitly states (Employment) that more", "More"),
 ("According to the statistical distribution of farming systems in the textbook (Table 1.1), sedentary", "In Eritrea's distribution of farming systems, sedentary"),
 ("According to physical soil separate sizes (Table 2.4), clay", "In the standard soil separate size classes, clay"),
 ("According to Table 2.6, a saline soil", "In the classification of salt-affected soils, a saline soil"),
 (" (Table 2.7)", ""),
 ("According to the national wildlife status listed in Table 2.11, which", "According to Eritrea's national wildlife status list, which"),
 ("Table 2.11 lists the Nubian", "Eritrea's national wildlife status list classes the Nubian"),
 ("Section 2.4 of the textbook documents that water", "In Eritrea, water"),
 ("As listed in Table 3.5, Urea", "Urea"),
])
n += apply('agriculture_12', [
 ("Historical data provided in the textbook (Table 2.2) shows", "Historical records show"),
 ("Under the textbook classification of water erosion,", "In the standard classification of water erosion,"),
 ("According to textbook section 3.5.5, excellent soils can be waterlogged for just one week, which is sufficient", "Even on excellent soils, just one week of waterlogging is enough"),
 (", as shown in the textbook, is the:", " is the:"),
 ("As specifically documented and Figure 3.15 of the textbook, the *Toker Dam* is", "The *Toker Dam*, near Asmara, is"),
 ("The textbook separates resources", "Farm management separates resources"),
 ("The textbook: 'A balance sheet is a financial statement which reflects the' financial position", "A balance sheet is a financial statement which reflects the financial position"),
 ("The textbook: 'Generally, co-operatives have an economic purpose, are owned and controlled by the members, are run for the benefit of members, and are not charities or state-directed organizations.'",
  "Generally, co-operatives have an economic purpose, are owned and controlled by their members, are run for the benefit of the members, and are not charities or state-directed organisations."),
])
n += apply('business_economics_11', [
 ("(the textbook’s starting model)", "(the starting model of market structures)"),
])
n += apply('business_economics_12', [
 ("Four-sector model in the book: C + I + G + (X − M).", "Four-sector model: C + I + G + (X − M)."),
 ("— the usual textbook answer.", "— the usual answer."),
 ("Theories in the book: countries gain", "Trade theories: countries gain"),
 ("(the textbook's own version of this item reads 'debited only when the fund is first established or subsequently increased in size')", "(strictly, it is debited when the fund is first established or later increased in size)"),
])
n += apply('chemistry_9', [
 ("That is why the book calls this a “chemical age”", "That is why our time is called a “chemical age”"),
 (" (G9 p.29, Activity 1.11)", ""),
 (" (G9 p.43)", ""),
 ("That preview is Unit 2.2 in the book — Grade 10 bonding will thicken it.", "This is only a preview — Grade 10 chemical bonding covers it in depth."),
 ("The textbook table: hydrogen sulphide", "Hydrogen sulphide"),
 ("Textbook: 'A reaction in which one element replaces a less active element in a compound is called a single replacement reaction',", "A reaction in which one element replaces a less active element in a compound is called a single replacement reaction,"),
])
n += apply('chemistry_10', [
 ("For basic soils the textbook recommends ammonium sulphate.", "For basic (alkaline) soils, an acidic fertiliser such as ammonium sulphate is used instead."),
 ("Food, industry feedstock (any one from the book).", "Seasoning and preserving food; also a raw material for making chlorine and sodium hydroxide."),
 ("but the textbook's recommended remedy is calamine lotion.", "but the usual recommended remedy is calamine lotion."),
 (" (textbook G10 p.164 lists producing sugar by photosynthesis as an energy-requiring process)", " (photosynthesis, which makes sugar using energy from sunlight, is an example)"),
 (" (G10 p.158)", ""),
 ("Types the book names:", "Main types:"),
])
n += apply('chemistry_11', [
 ("but the textbook experiment uses ammonia.", "but the classic fountain experiment uses ammonia."),
 (" (textbook Table 4.2)", ""),
 (" (textbook p.126)", ""),
 ("The textbook: 'The carbonate ores are changed into oxides by strongly heating them in a limited air. This process is known as calcining or calcination.'",
  "Carbonate ores are changed into oxides by strongly heating them in a limited supply of air; this process is called calcination."),
 ("The book treats extraction, properties and uses of important metals — plus alloys.", "This unit covers the extraction, properties and uses of important metals, plus alloys."),
])
n += apply('chemistry_12', [
 (" — textbook review item.", " — a common exam item."),
 ("Nuclear power station in the textbook =", "Nuclear power station ="),
])
print('subs', n)
