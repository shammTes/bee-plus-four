# Matric GPA calculator ('Track my GPA')

Off by default (Home > Track my GPA). For Grades 11–12. Rules live in `lib/high/gpa/gpa_config.dart`.

## Verified rules
- Letter grades convert **A = 4, B = 3, C = 2, D = 1, F = 0**; an F means the subject is failed.
- The GPA is the average of **five subjects: Mathematics, English and the three other subjects with the highest results**.
- **2.0** is the minimum GPA for admission to higher education.

Sources: NOKUT, *Refugees Country Briefing: Eritrea* (2017), https://www.nokut.no/contentassets/5751a837c39042b08776c0eacf416e41/country_briefing_eritrea_2017.pdf ;
NOKUT, *Report on recognition of higher education in Eritrea and Ethiopia* (2013), https://www.nokut.no/globalassets/nokut/artikkelbibliotek/kunnskapsbasen/rapporter/ua/2013/gulliksen_anne-kari_audensen_erik_report_on_recognition_of_higher_education_in_eritrea_and_ethiopia_2013-1.pdf

## Not fully verified (editable in gpa_config.dart)
- % bands: A 75–100, B 65–74.99, C 50–64.99, D 40–49.99, F 0–39.99 (Scholaro, https://www.scholaro.com/db/Countries/Eritrea/Grading-System).
  The NCAA guide (http://fs.ncaa.org/Docs/eligibility_center/International_Information/Guide/Countries/Eritrea.pdf) gives A 75, B 65, C 50 and no D band.
  The Ministry may scale real results, so predictions are a guide only.
- Which subjects belong to the Natural Science and Social Science streams.
- Estimate: the newest answer to each of the last 60 matric/model questions per subject; at least 10 answers needed.
