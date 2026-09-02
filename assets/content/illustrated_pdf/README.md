# Illustrated notes PDFs (high school)

Put compressed PDFs here using this naming:

```
assets/content/illustrated_pdf/{GRADE}/{SUBJECT}/u{N}_{short_slug}.pdf
```

Examples:
- G9/CHEMISTRY/u2_atomic_structure.pdf
- G10/BIOLOGY/u1_food_and_digestion.pdf
- G11/PHYSICS/u2_waves_and_sound.pdf

Rules:
- High school only (G9–G12)
- One unit = one PDF
- Prefer compressed PDF (target 0.3–2 MB each)
- After adding files, set `"pdf_asset"` on the matching deck in
  `illustrated_catalog_g9.json` … `g12.json`

Export tip (Mac):
1. Open PPTX → File → Export → PDF
2. Compress with Preview or:
   `gs -sDEVICE=pdfwrite -dCompatibilityLevel=1.4 -dPDFSETTINGS=/ebook -dNOPAUSE -dQUIET -dBATCH -sOutputFile=out.pdf in.pdf`
