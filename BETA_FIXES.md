# Beta feedback fixes (2026-09-21)

## Done in this pass
- **Coach**: big choice buttons; after answer shows Continue; grade switch (G9–G12); subject switch anytime
- **Matric**: all questions now get explanation_steps (was empty because JSON used `explanation` while model expected `explanation_steps`)
- **Similar questions**: always show choices + answer + explanation panel
- **Back / Leave**: PopScope + SystemNavigator.pop() so Leave closes the app
- **Model exams**: labeled section on Exams tab (like matriculation)
- **Key ideas**: colorful numbered cards
- **Home**: large Illustrated Notes hero CTA; motivation strip; bigger action cards
- **Notes**: illustrated packs banner
- **Practice list**: All questions sheet to jump to any item
- **Unlock**: Paste & unlock (clipboard from Bee Seller code/QR text)
- **Windows Bee Seller**: `tools/bee_seller_windows/bee_seller_desktop.py`

## Partial / next
- Camera QR scan needs `mobile_scanner` (or similar) + Android permissions — paste works now
- Textbook open at exact unit page needs page-index map per PDF
- Generating brand-new illustrated visual decks still needs designer/PDF assets; existing catalogs promoted in UI
- Official matric keys (not heuristic explanations) still preferred where teacher guides exist
