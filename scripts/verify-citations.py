#!/usr/bin/env python3
"""
Zitations-Validierungs-Script
Prüft ob Zitationen im LaTeX-Text mit den PDF-Quellen übereinstimmen
"""

import re
import os
from pathlib import Path
from typing import List, Dict, Tuple
import PyPDF2

# Pfade
PAPER_DIR = Path(r"c:\development\PrivProjects\BachlorsThesis\Paper")
SOURCES_DIR = Path(r"c:\development\PrivProjects\BachlorsThesis\sources")
CHAPTERS_DIR = PAPER_DIR / "chapters"
BIB_FILE = PAPER_DIR / "references.bib"
OUTPUT_DIR = Path(r"c:\development\PrivProjects\BachlorsThesis\.kiro\specs\quellenprufung")


def extract_citations_from_latex(latex_content: str, filename: str) -> List[Dict]:
    """
    Extrahiert alle Zitationen aus LaTeX-Text
    Format: \footcite[S. 123]{Author2020}
    """
    citations = []
    
    # Pattern für verschiedene Zitationstypen mit optionalen Seitenangaben
    patterns = [
        r'\\footcite\[([^\]]+)\]\{([^}]+)\}',  # \footcite[S. 123]{Key}
        r'\\vglfootcite\[([^\]]+)\]\{([^}]+)\}',  # \vglfootcite[S. 123]{Key}
        r'\\cite\[([^\]]+)\]\{([^}]+)\}',  # \cite[S. 123]{Key}
        r'\\parencite\[([^\]]+)\]\{([^}]+)\}',  # \parencite[S. 123]{Key}
    ]
    
    for pattern in patterns:
        matches = re.finditer(pattern, latex_content)
        for match in matches:
            page_info = match.group(1)
            bib_key = match.group(2)
            
            # Kontext extrahieren (100 Zeichen vor und nach der Zitation)
            start_pos = max(0, match.start() - 100)
            end_pos = min(len(latex_content), match.end() + 100)
            context = latex_content[start_pos:end_pos]
            
            # Seitenzahl extrahieren - verschiedene Formate
            # Format 1: "S. 123" oder "S.~123"
            page_match = re.search(r'S\.[\s~]*(\d+)', page_info)
            if not page_match:
                # Format 2: nur Zahl "123"
                page_match = re.search(r'^(\d+)$', page_info.strip())
            if not page_match:
                # Format 3: "1\,ff." (erste Zahl nehmen)
                page_match = re.search(r'(\d+)', page_info)
            
            page_num = int(page_match.group(1)) if page_match else None
            
            citations.append({
                'file': filename,
                'bib_key': bib_key,
                'page_info': page_info,
                'page_num': page_num,
                'context': context.strip(),
                'position': match.start()
            })
    
    return citations


def get_pdf_for_bibkey(bib_key: str) -> Path:
    """
    Findet die PDF-Datei für einen BibTeX-Key
    """
    # Mapping aus Phase 2
    mappings = {
        "Zuboff2019": "Zuboff - The Age of Surveillance Capitalism.pdf",
        "Pasquale2015": "Pasquale - Black Box Society.pdf",
        "ONeil2016": "ONeil - Weapons of Math Destruction.pdf",
        "Srnicek2017": "Srnicek - Platform Capitalism.pdf",
        "VanDijck2018": "van Dijck - Datafiction, Dataism, Dataveillance.pdf",
        "VanDijck2014": "van Dijck - Datafiction, Dataism, Dataveillance.pdf",
        "Gillespie2014": "Gillespie - The Relevance of Algorithms.pdf",
        "Goodfellow2016": "Goodfellow, Bengio, Courville - Deep Learning.pdf",
        "Pariser2011": "Pariser - The Filter Bubble.pdf",
        "Cinelli2021": "Cinelli - The Echo Chamber Effect on Social Media.pdf",
        "SuttonBarto2018": "Sutton, Barto - Reinforcement Learning An Introduction.pdf",
        "Laudon2016": "Laudon - Management Information Systems.pdf",
        "Lyon2012": "Lyon - Surveillance Studies.pdf",
        "Narayanan2023": "Narayanan - Understanding Social Media Recommendation Algorithms.pdf",
        "MetzlerGarcia2023": "Metzler, Garcia - Social Drivers and Algorithmic Mechanisms.pdf",
        "Tiwana2014": "Tiwana - The Rise of Platform Ecosystems.pdf",
        "Parker2016": "Parker, Van Alstyne, Choudary - Platform Revolution.pdf",
        "OECD2013": "OECD - Exploring the Economics of Personal Data.pdf",
        "Acquisti2016": "Acquisti, Taylor, Wagman - The Economics of Privacy.pdf",
        "Kitchin2014": "Kitchin - The Data Revolution.pdf",
        "Adomavicius2005": "Adomavicius, Tuzhilin - Toward the Next Generation of Recommender Systems.pdf",
        "Burke2002": "Burke - Hybrid Recommender Systems.pdf",
        "Fogg2009": "Fogg - A Behavior Model for Persuasive Design.pdf",
        "Kramer2014": "Kramer - Experimental Evidence of Emotional Contagion.pdf",
        "Isaak2018": "Isaak - User Data Privacy and Privacy Protection.pdf",
        "Creemers2018": "Creemers - Chinas Social Credit System.pdf",
        "Qiang2019": "Qiang - Road to Digital Unfreedom.pdf",
        "SFRC2020": "Senate - The New Big Brother.pdf",
        "AIHLEG2019": "EU - Ethics Guidelines for Trustworthy AI.pdf",
        "Susser2019": "Susser, Roessler, Nissenbaum - Online Manipulation Hidden Influences in a Digital World.pdf",
        "Kaptein2015": "Kaptein et al. - Personalizing Persuasive Technologies.pdf",
        "Yeung2017": "Yeung - Hypernudge Big Data as a Mode of Regulation by Design.pdf",
        "OrbenPrzybylski2019": "Orben, Przybylski - Adolescent Well-being and Digital Technology.pdf",
        "Areeb2023": "Areeb et al. - Filter Bubbles in Recommender Systems A Systematic Review.pdf",
        "Kelm2023": "Kelm et al. - How Algorithmically Curated Online Environments Influence Political Polarization.pdf",
        "Davenport2006": "Davenport - Competing on Analytics.pdf",
        "EvansSchmalensee2016": "Evans, Gawer - The Business of Platforms.pdf",
        "BradshawHoward2018": "Bradshaw, Howard - Challenging Truth and Trust A Global Inventory of Organized Social Media Manipulation.pdf",
        "Feldstein2019": "Feldstein - The Global Expansion of AI Surveillance.pdf",
        "WoolleyHoward2017": "Woolley, Howard - Computational Propaganda Worldwide Executive Summary.pdf",
        "GDPR2016": "EU - General Data Protection Regulation (GDPR).pdf",
        "NIST2023": "NIST - AI Risk Management Framework.pdf",
        "AIAct2024": "EU - Artificial Intelligence Act.pdf",
        "DSA2022": "EU - Digital Services Act (DSA).pdf",
        "VomBrocke2009": "vom Brocke - Reconstructing the Giant.pdf",
        "Mitchell1997": "Mitchell - Machine Learning.pdf",
        "JordanMitchell2015": "Jordan, Mitchell - Machine Learning Trends, Perspectives, Prospects.pdf",
        "Chandola2009": "Chandola, Banerjee, Kumar - Anomaly Detection A Survey.pdf",
        "RussellNorvig2010": "Russell, Norvig - Artificial Intelligence A Modern Approach.pdf",
    }
    
    if bib_key in mappings:
        pdf_name = mappings[bib_key]
        # Suche in allen Unterverzeichnissen
        for subdir in ["", "new", "Webquellen"]:
            pdf_path = SOURCES_DIR / subdir / pdf_name
            if pdf_path.exists():
                return pdf_path
    
    return None


def extract_text_from_pdf_page(pdf_path: Path, page_num: int) -> str:
    """
    Extrahiert Text von einer bestimmten PDF-Seite
    """
    try:
        with open(pdf_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            
            # PDF-Seiten sind 0-indiziert, aber Zitationen sind 1-indiziert
            if 0 <= page_num - 1 < len(pdf_reader.pages):
                page = pdf_reader.pages[page_num - 1]
                text = page.extract_text()
                return text
            else:
                return f"[ERROR: Seite {page_num} existiert nicht in PDF]"
    except Exception as e:
        return f"[ERROR: {str(e)}]"


def simple_similarity_check(context: str, pdf_text: str) -> Dict:
    """
    Einfache Ähnlichkeitsprüfung zwischen Kontext und PDF-Text
    """
    # Bereinige Texte
    context_clean = re.sub(r'[^a-zA-Z0-9äöüÄÖÜß\s]', '', context.lower())
    pdf_clean = re.sub(r'[^a-zA-Z0-9äöüÄÖÜß\s]', '', pdf_text.lower())
    
    # Extrahiere Schlüsselwörter (Wörter länger als 4 Zeichen)
    context_words = set([w for w in context_clean.split() if len(w) > 4])
    pdf_words = set([w for w in pdf_clean.split() if len(w) > 4])
    
    if not context_words:
        return {'score': 0, 'match': 'UNKNOWN', 'reason': 'Keine Schlüsselwörter im Kontext'}
    
    # Berechne Überschneidung
    common_words = context_words & pdf_words
    similarity_score = len(common_words) / len(context_words) if context_words else 0
    
    # Bewertung
    if similarity_score > 0.3:
        match = 'OK'
    elif similarity_score > 0.1:
        match = 'SUSPICIOUS'
    else:
        match = 'MISMATCH'
    
    return {
        'score': similarity_score,
        'match': match,
        'common_words': common_words,
        'context_words_count': len(context_words),
        'common_words_count': len(common_words)
    }


def main():
    print("=== Zitations-Validierung ===\n")
    
    # 1. Alle LaTeX-Dateien durchsuchen
    all_citations = []
    
    for tex_file in CHAPTERS_DIR.glob("*.tex"):
        print(f"Analysiere {tex_file.name}...")
        content = tex_file.read_text(encoding='utf-8')
        citations = extract_citations_from_latex(content, tex_file.name)
        all_citations.extend(citations)
    
    print(f"\nOK {len(all_citations)} Zitationen gefunden\n")
    
    # 2. Jede Zitation prüfen
    results = []
    
    for i, citation in enumerate(all_citations, 1):
        print(f"[{i}/{len(all_citations)}] Prüfe {citation['bib_key']}...", end=' ')
        
        # Finde PDF
        pdf_path = get_pdf_for_bibkey(citation['bib_key'])
        
        if not pdf_path:
            print("PDF nicht gefunden")
            results.append({
                **citation,
                'status': 'PDF_NOT_FOUND',
                'similarity': None
            })
            continue
        
        if not citation['page_num']:
            print("Keine Seitenzahl")
            results.append({
                **citation,
                'status': 'NO_PAGE_NUMBER',
                'similarity': None
            })
            continue
        
        # Extrahiere Text von der zitierten Seite
        pdf_text = extract_text_from_pdf_page(pdf_path, citation['page_num'])
        
        if pdf_text.startswith('[ERROR'):
            print(f"ERROR {pdf_text}")
            results.append({
                **citation,
                'status': 'PDF_READ_ERROR',
                'similarity': None,
                'error': pdf_text
            })
            continue
        
        # Prüfe Ähnlichkeit
        similarity = simple_similarity_check(citation['context'], pdf_text)
        
        results.append({
            **citation,
            'status': 'CHECKED',
            'similarity': similarity,
            'pdf_path': str(pdf_path)
        })
        
        if similarity['match'] == 'OK':
            print(f"OK ({similarity['score']:.2%})")
        elif similarity['match'] == 'SUSPICIOUS':
            print(f"SUSPICIOUS ({similarity['score']:.2%})")
        else:
            print(f"MISMATCH ({similarity['score']:.2%})")
    
    # 3. Bericht erstellen
    print("\n=== Erstelle Bericht ===\n")
    
    report_path = OUTPUT_DIR / "zitations-validierung.md"
    
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write("# Zitations-Validierung - Bericht\n\n")
        f.write("**Automatische Prüfung der Zitationen**\n\n")
        f.write("---\n\n")
        
        # Statistiken
        total = len(results)
        ok = len([r for r in results if r.get('similarity') and r['similarity']['match'] == 'OK'])
        suspicious = len([r for r in results if r.get('similarity') and r['similarity']['match'] == 'SUSPICIOUS'])
        mismatch = len([r for r in results if r.get('similarity') and r['similarity']['match'] == 'MISMATCH'])
        errors = len([r for r in results if r['status'] != 'CHECKED'])
        
        f.write("## Zusammenfassung\n\n")
        f.write(f"- **Gesamt:** {total} Zitationen\n")
        f.write(f"- **✓ OK:** {ok} ({ok/total*100:.1f}%)\n")
        f.write(f"- **⚠️ Verdächtig:** {suspicious} ({suspicious/total*100:.1f}%)\n")
        f.write(f"- **❌ Mismatch:** {mismatch} ({mismatch/total*100:.1f}%)\n")
        f.write(f"- **⚠️ Fehler:** {errors}\n\n")
        f.write("---\n\n")
        
        # Problematische Zitationen
        f.write("## ❌ Problematische Zitationen\n\n")
        
        problem_citations = [r for r in results if (
            r['status'] != 'CHECKED' or 
            (r.get('similarity') and r['similarity']['match'] in ['MISMATCH', 'SUSPICIOUS'])
        )]
        
        if problem_citations:
            for result in problem_citations:
                f.write(f"### {result['bib_key']} (Seite {result.get('page_num', 'N/A')})\n\n")
                f.write(f"**Datei:** `{result['file']}`\n\n")
                f.write(f"**Status:** {result['status']}\n\n")
                
                if result.get('similarity'):
                    sim = result['similarity']
                    f.write(f"**Ähnlichkeit:** {sim['score']:.2%} ({sim['match']})\n\n")
                    f.write(f"- Gemeinsame Schlüsselwörter: {sim['common_words_count']}/{sim['context_words_count']}\n\n")
                
                f.write(f"**Kontext:**\n```\n{result['context'][:200]}...\n```\n\n")
                f.write("---\n\n")
        else:
            f.write("✓ Keine problematischen Zitationen gefunden!\n\n")
        
        # Alle Zitationen (Referenz)
        f.write("## 📋 Alle Zitationen (Referenz)\n\n")
        
        for result in results:
            status_icon = "✓" if result.get('similarity') and result['similarity']['match'] == 'OK' else "⚠️"
            f.write(f"{status_icon} **{result['bib_key']}** (S. {result.get('page_num', 'N/A')}) - `{result['file']}`\n")
    
    print(f"OK Bericht gespeichert: {report_path}")
    print("\n=== Fertig ===")


if __name__ == "__main__":
    main()
