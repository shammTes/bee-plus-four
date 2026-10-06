"""geography 9-12 (+agri11): remove 'Section x.y' / 'Table x.y' / textbook attributions left by the study-notes generator."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from subs import apply, apply_re

GEN = [
 (r" under Section \d[\w./]*\w", ""),
 (r"Review Section [\d.]+'s regional debate", "Review the debate about regions"),
 (r"Check Section 7\.1 details", "Recall the ethnic groups and where they live"),
 (r"The text explicitly notes: ", ""),
 (r"According to Section [\w./]+, plateaus", "Plateaus"),
 (r"Section \d[\w.]*\w (?:states|notes) that (\w)", lambda m: m.group(1).upper()),
 (r"Section 2\.2 lists five different factors", "There are five different factors"),
 (r"Section 1\.2\.3\.i lists three distinctive characteristics", "There are three distinctive characteristics"),
 (r"Section 1\.2\.4 describes the natural vegetation", "Think about the natural vegetation"),
 (r"Section 2\.5 describes how water carries materials down\.", "Water carries materials downward in different ways."),
 (r"Section 2\.5 describes the different layers\.", "A soil profile has different layers (horizons)."),
 (r"Section 2\.5 defines this vertical cross-section\.", "A vertical cross-section through the soil from the surface to the bedrock is called a soil profile."),
 (r"Section 2\.6 divides water erosion into (five types|progressive stages)\.", r"Water erosion is divided into \1: splash, sheet, rill, gully and stream-bank erosion."),
 (r"Section 2\.7 outlines erosion control strategies\.", "Erosion is controlled by terracing, contour ploughing, afforestation, check dams and strip cropping."),
 (r"Section 3\.3 contains global density metrics\.", "Population density = total population ÷ land area."),
 (r"Section 3\.3\.1 outlines how rugged configurations affect settlement\.", "Rugged relief (steep mountains) discourages settlement, while plains attract people."),
 (r"Section 3\.3\.1\.v outlines how energy and mineral resources affect distribution\.", "Energy and mineral resources attract mining and industry, and so attract people."),
 (r"Section 3\.2 outlines that world population reached a major turning point\.", "World population growth reached a major turning point."),
 (r"\*\*Step 2: Compare with textbook details\.\*\*", "**Step 2: Recall the key facts.**"),
 (r"\*\*Step 2: Retrieve surface temperature from the textbook\.\*\*", "**Step 2: Recall the surface temperature.**"),
 (r" in the text\.\*\*", ".**"),
 (r"The textbook outlines several measures of development\.", "Development is measured by economic indicators (per capita income, energy use, employment structure) and social ones (literacy, nutrition, health)."),
 (r"The textbook lists nutrition indicators of development\.", "Nutrition (daily calorie intake per person) is one indicator of development."),
 (r"The textbook states: \"It is inclined to the plane of the earth's orbit at an angle of 66\.5 degrees\.\"", "The earth's axis is inclined to the plane of its orbit at an angle of 66.5 degrees (23.5° from the vertical)."),
 (r"The textbook states that the word \*climate\* comes", "The word *climate* comes"),
 (r"The textbook states that all soils", "All soils"),
 (r"The textbook mentions that the universe", "The universe"),
 (r"According to the standard soil volume composition documented in Figure 2\.4, an ideal", "By volume, an ideal"),
 (r" \(see Table 1\.1 below\)", ""),
]
n = 0
for bk in ['geography_9', 'geography_10', 'geography_11', 'geography_12', 'agriculture_11']:
    n += apply_re(bk, GEN)

n += apply('geography_10', [
 ("Table 3.4 lists the ten most populated countries in 2009.", "In 2009 the ten most populated countries were China, India, USA, Indonesia, Brazil, Pakistan, Bangladesh, Nigeria, Russia and Japan."),
 ("but per capita income is the one the textbook calls 'widely used'.", "but per capita income is the most widely used measure."),
 ("[Contour map, see Fig. 1 (image).] The contour interval in the map is  A) 100 meters.  B) 200 meters.  C) 300 meters.  D) 400 meters.  E) 500 meters.",
  "On a map, neighbouring contours are labelled 1200 m, 1400 m, 1600 m and 1800 m. The contour interval is  A) 100 m  B) 200 m  C) 300 m  D) 400 m  E) 500 m"),
], strict=False)
n += apply('geography_12', [
 ("**Step 1: Retrieve river discharge values from Table 2.1**", "**Step 1: Recall the annual discharge of the main rivers**"),
 ("**Step 1: Reference Table 3.3 data**", "**Step 1: Use the annual rainfall and evaporation data**"),
 ("**Step 1: Check total vegetative sum in Table 4.1**", "**Step 1: Add up the vegetation cover figures**"),
 ("Table 4.1 shows that the sum", "the sum"),
 ("According to Table 7.2, what was the estimated population of Eritrea in 1945?", "According to historical estimates, what was the population of Eritrea in 1945?"),
 ("**Step 1: Locate 1945 value in Table 7.2**", "**Step 1: Recall the population estimates**"),
 ("constitutes the largest percentage of Eritrea's population according to Table 7.3?", "constitutes the largest percentage of Eritrea's population?"),
 ("**Step 1: Check Table 7.3 values**", "**Step 1: Recall the age structure (% of population)**"),
 ("**Fixes in the book:**", "**Fixes:**"),
 ("Give two advantages of storing rain in dams, as the textbook asks.", "Give two advantages of storing rain in dams."),
 ("Alternatives in the book:", "Alternatives:"),
 ("– one of the textbook's soil conservation measures.", "– one of the main soil conservation measures."),
 ("The textbook lists the major water problems of the Eritrean Highlands:", "The major water problems of the Eritrean Highlands are:"),
 ("The textbook calls the Semitic families (from the Arabian Peninsula) the latest migrants;", "The Semitic families (from the Arabian Peninsula) were the latest migrants;"),
 ("The textbook's table of ethnic groups: 'Rashaida <1.0 % – Northern Red Sea.'", "The Rashaida make up less than 1 % of the population and live in the Northern Red Sea region."),
 ("The textbook's table of ethnic groups gives the Nara (1.5 %)", "The Nara (about 1.5 % of the population) live"),
 ("The textbook places the Rashaida,", "The Rashaida,"),
 ("The textbook's ethnic composition gives Tigrinya about 50%", "Of Eritrea's ethnic groups, Tigrinya make up about 50%"),
 ("The textbook notes that in this area", "In this area"),
], strict=False)
n += apply('geography_11', [
 ("The textbook groups silt and clay together as suspended load, so C is also accepted.", "Silt and clay are both carried as suspended load, so C is also accepted."),
 ("The textbook lists the processes of wave erosion:", "The processes of wave erosion are:"),
 ("The textbook table of administrative zones gives the areas:", "The areas of the administrative zones are:"),
 ("The textbook's table of administrative regions gives Maekel", "Maekel"),
 ("Administration in the textbook is the regional structure", "The administrative regions (zobas) are the structure"),
], strict=False)
print('geo subs', n)
