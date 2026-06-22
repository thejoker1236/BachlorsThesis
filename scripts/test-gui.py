#!/usr/bin/env python3
"""
Test GUI direkt
"""

import sys
sys.path.insert(0, r'c:\development\PrivProjects\BachlorsThesis\scripts')

from auto_fix_citations import AutoCorrectionReviewGUI

# Test-Daten
test_corrections = [
    {
        'citation': {
            'file': '01_einleitung.tex',
            'bib_key': 'Srnicek2017',
            'page_info': 'S. 1',
            'page_num': 1,
            'context': 'Test Kontext für die Zitation. Dies ist ein längerer Text um zu sehen wie es im GUI aussieht.',
            'position': 100,
            'full_match': r'\footcite[S. 1]{Srnicek2017}'
        },
        'old_page': 1,
        'new_page': 4,
        'confidence': 0.75,
        'pdf_name': 'Srnicek - Platform Capitalism.pdf',
        'status': 'auto_correct'
    },
    {
        'citation': {
            'file': '02_grundlagen.tex',
            'bib_key': 'Zuboff2019',
            'page_info': 'S. 10',
            'page_num': 10,
            'context': 'Zweite Test-Zitation mit anderem Kontext.',
            'position': 200,
            'full_match': r'\footcite[S. 10]{Zuboff2019}'
        },
        'old_page': 10,
        'new_page': 15,
        'confidence': 0.55,
        'pdf_name': 'Zuboff - The Age of Surveillance Capitalism.pdf',
        'status': 'auto_correct'
    }
]

print("Starte Test-GUI mit 2 Korrekturen...")
app = AutoCorrectionReviewGUI(test_corrections)
app.run()
print("GUI geschlossen")
