#!/usr/bin/env python3
"""
Vollautomatisches Zitations-Korrektur-Tool mit Ollama LLM
Läuft OHNE Interaktion - korrigiert automatisch alle Zitationen über Nacht

KEINE GUI - KEINE FRAGEN - NUR AUTOMATISCHE KORREKTUR
"""

import re
import sys
from pathlib import Path
from typing import List, Dict, Tuple, Optional
import PyPDF2
import requests
import json
from datetime import datetime

# Pfade
SCRIPT_DIR = Path(__file__).parent
PAPER_DIR = Path(r"c:\development\PrivProjects\BachlorsThesis\Paper")
SOURCES_DIR = Path(r"c:\development\PrivProjects\BachlorsThesis\sources")
CHAPTERS_DIR = PAPER_DIR / "chapters"
PROGRESS_FILE = SCRIPT_DIR / "korrektur-progress.json"
LOG_FILE = SCRIPT_DIR / "korrektur-protokoll.txt"

# Mapping BibKey -> PDF
PDF_MAPPING = {
    "Srnicek2017": "Srnicek - Platform Capitalism.pdf",
    "Zuboff2019": "Zuboff - The Age of Surveillance Capitalism.pdf",
    "Laudon2016": "Laudon - Management Information Systems.pdf",
    "Pasquale2015": "Pasquale - Black Box Society.pdf",
    "Kitchin2014": "Kitchin - The Data Revolution.pdf",
    "ONeil2016": "ONeil - Weapons of Math Destruction.pdf",
    "RussellNorvig2010": "Russell, Norvig - Artificial Intelligence A Modern Approach.pdf",
    "Goodfellow2016": "Goodfellow, Bengio, Courville - Deep Learning.pdf",
    "SuttonBarto2018": "Sutton, Barto - Reinforcement Learning An Introduction.pdf",
    "Mitchell1997": "Mitchell - Machine Learning.pdf",
    "JordanMitchell2015": "Jordan, Mitchell - Machine Learning Trends, Perspectives, Prospects.pdf",
    "AIHLEG2019": "EU - Ethics Guidelines for Trustworthy AI.pdf",
    "NIST2023": "NIST - AI Risk Management Framework.pdf",
    "Adomavicius2005": "Adomavicius, Tuzhilin - Toward the Next Generation of Recommender Systems.pdf",
    "Burke2002": "Burke - Hybrid Recommender Systems.pdf",
    "Fogg2009": "Fogg - A Behavior Model for Persuasive Design.pdf",
    "Kramer2014": "Kramer - Experimental Evidence of Emotional Contagion.pdf",
    "Gillespie2014": "Gillespie - The Relevance of Algorithms.pdf",
    "VanDijck2014": "van Dijck - Datafiction, Dataism, Dataveillance.pdf",
    "Lyon2012": "Lyon - Surveillance Studies.pdf",
    "Narayanan2023": "Narayanan - Understanding Social Media Recommendation Algorithms.pdf",
    "MetzlerGarcia2023": "Metzler, Garcia - Social Drivers and Algorithmic Mechanisms.pdf",
    "Tiwana2014": "Tiwana - The Rise of Platform Ecosystems.pdf",
    "Parker2016": "Parker, Van Alstyne, Choudary - Platform Revolution.pdf",
    "OECD2013": "OECD - Exploring the Economics of Personal Data.pdf",
    "Acquisti2016": "Acquisti, Taylor, Wagman - The Economics of Privacy.pdf",
    "Isaak2018": "Isaak - User Data Privacy and Privacy Protection.pdf",
    "Creemers2018": "Creemers - Chinas Social Credit System.pdf",
    "Qiang2019": "Qiang - Road to Digital Unfreedom.pdf",
    "SFRC2020": "Senate - The New Big Brother.pdf",
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
    "AIAct2024": "EU - Artificial Intelligence Act.pdf",
    "DSA2022": "EU - Digital Services Act (DSA).pdf",
    "VomBrocke2009": "vom Brocke - Reconstructing the Giant.pdf",
    "Chandola2009": "Chandola, Banerjee, Kumar - Anomaly Detection A Survey.pdf",
    "Pariser2011": "Pariser - The Filter Bubble.pdf",
    "Cinelli2021": "Cinelli - The Echo Chamber Effect on Social Media.pdf",
    "VanDijck2018": "van Dijck - Datafiction, Dataism, Dataveillance.pdf",
}


class Logger:
    """Protokoll-Logger für alle Aktionen"""
    
    def __init__(self, log_file: Path):
        self.log_file = log_file
        self.start_time = datetime.now()
        
        # Neue Session starten
        with open(self.log_file, 'a', encoding='utf-8') as f:
            f.write("\n" + "=" * 80 + "\n")
            f.write(f"AUTOMATISCHE ZITATIONS-KORREKTUR - {self.start_time.strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write("=" * 80 + "\n\n")
    
    def log(self, message: str, also_print: bool = True):
        """Schreibt ins Protokoll und optional auf Konsole"""
        with open(self.log_file, 'a', encoding='utf-8') as f:
            f.write(f"{message}\n")
        if also_print:
            print(message)
    
    def summary(self, corrected: int, skipped: int, errors: int, total: int):
        """Schreibt Zusammenfassung"""
        end_time = datetime.now()
        duration = end_time - self.start_time
        
        # Berechne durchschnittliche Zeit pro Zitation
        avg_per_citation = duration.total_seconds() / total if total > 0 else 0
        
        summary = f"""
{'=' * 80}
ZUSAMMENFASSUNG
{'=' * 80}
Gesamte Zitationen: {total}
✓ Korrigiert:       {corrected} ({corrected/total*100:.1f}%)
⊘ Übersprungen:     {skipped} ({skipped/total*100:.1f}%)
✗ Fehler:           {errors} ({errors/total*100:.1f}%)

Start:              {self.start_time.strftime('%Y-%m-%d %H:%M:%S')}
Ende:               {end_time.strftime('%Y-%m-%d %H:%M:%S')}
Gesamt-Zeit:        {duration}
Ø pro Zitation:     {avg_per_citation:.1f} Sekunden
{'=' * 80}
"""
        self.log(summary)


def check_text_similarity_with_ollama(search_text: str, page_text: str) -> float:
    """
    Verwendet Ollama LLM um semantische Ähnlichkeit zu bewerten
    Gibt Score zwischen 0.0 und 1.0 zurück
    """
    try:
        prompt = f"""Vergleiche diese beiden Texte und bewerte ihre semantische Ähnlichkeit.
Antworte NUR mit einer Zahl zwischen 0 und 100 (0 = völlig unterschiedlich, 100 = sehr ähnlich).

TEXT 1 (Zitat-Kontext):
{search_text[:500]}

TEXT 2 (PDF-Seite):
{page_text[:500]}

Ähnlichkeit (nur Zahl 0-100):"""

        response = requests.post(
            'http://localhost:11434/api/generate',
            json={
                'model': 'llama3.2:3b',
                'prompt': prompt,
                'stream': False,
                'options': {
                    'temperature': 0.1,
                    'num_predict': 10
                }
            },
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()['response'].strip()
            match = re.search(r'(\d+)', result)
            if match:
                score = int(match.group(1))
                return min(score / 100.0, 1.0)
            else:
                return 0.5
        
        return 0.0
        
    except Exception as e:
        return 0.0


def extract_citations(latex_content: str, filename: str) -> List[Dict]:
    """Extrahiert alle Zitationen mit Seitenangaben"""
    citations = []
    patterns = [
        r'\\footcite\[([^\]]+)\]\{([^}]+)\}',
        r'\\vglfootcite\[([^\]]+)\]\{([^}]+)\}',
        r'\\cite\[([^\]]+)\]\{([^}]+)\}',
        r'\\parencite\[([^\]]+)\]\{([^}]+)\}',
    ]
    
    for pattern in patterns:
        for match in re.finditer(pattern, latex_content):
            page_info = match.group(1)
            bib_key = match.group(2)
            
            page_match = re.search(r'S\.[\s~]*(\d+)', page_info)
            if not page_match:
                page_match = re.search(r'^(\d+)$', page_info.strip())
            if not page_match:
                page_match = re.search(r'(\d+)', page_info)
            
            if page_match:
                page_num = int(page_match.group(1))
                
                start = max(0, match.start() - 400)
                end = min(len(latex_content), match.end() + 400)
                context = latex_content[start:end].strip()
                
                citations.append({
                    'file': filename,
                    'bib_key': bib_key,
                    'page_info': page_info,
                    'page_num': page_num,
                    'context': context,
                    'position': match.start(),
                    'full_match': match.group(0)
                })
    
    return citations


def find_pdf(bib_key: str) -> Optional[Path]:
    """Findet PDF-Datei"""
    if bib_key in PDF_MAPPING:
        for subdir in ["", "new", "Webquellen"]:
            pdf_path = SOURCES_DIR / subdir / PDF_MAPPING[bib_key]
            if pdf_path.exists():
                return pdf_path
    return None


def find_best_page_in_pdf(pdf_path: Path, search_text: str, current_page: int, logger: Logger) -> Optional[Tuple[int, float]]:
    """
    Findet die beste Seite im PDF basierend auf semantischer Ähnlichkeit mit Ollama
    """
    try:
        # Bereite Suchtext vor
        clean_search = re.sub(r'\\[a-zA-Z]+(\{[^}]*\}|\[[^\]]*\])?', '', search_text)
        clean_search = re.sub(r'[^a-zA-Z0-9äöüÄÖÜß\s.,;:-]', ' ', clean_search)
        clean_search = re.sub(r'\s+', ' ', clean_search).strip()
        
        words = clean_search.split()
        if len(words) > 200:
            clean_search = ' '.join(words[:200])
        
        with open(pdf_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            total_pages = len(reader.pages)
            
            # Intelligentes Sampling
            pages_to_check = []
            
            # 1. Aktuelle Seite ±10
            for offset in range(-10, 11):
                page = current_page - 1 + offset
                if 0 <= page < total_pages:
                    pages_to_check.append((page, 'high'))
            
            # 2. Erste 15 Seiten
            for page in range(min(15, total_pages)):
                if (page, 'high') not in pages_to_check:
                    pages_to_check.append((page, 'medium'))
            
            # 3. Jede 10. Seite
            for page in range(15, total_pages, 10):
                pages_to_check.append((page, 'low'))
            
            pages_to_check.sort(key=lambda x: (0 if x[1] == 'high' else 1 if x[1] == 'medium' else 2, x[0]))
            
            best_match = None
            best_score = 0.0
            checked_count = 0
            max_checks = 30
            
            for page_num, priority in pages_to_check:
                if checked_count >= max_checks:
                    break
                
                try:
                    page = reader.pages[page_num]
                    page_text = page.extract_text()
                    
                    if not page_text or len(page_text.strip()) < 50:
                        continue
                    
                    clean_page = re.sub(r'\s+', ' ', page_text).strip()
                    page_words = clean_page.split()
                    if len(page_words) > 300:
                        clean_page = ' '.join(page_words[:300])
                    
                    similarity = check_text_similarity_with_ollama(clean_search, clean_page)
                    checked_count += 1
                    
                    if similarity > best_score:
                        best_score = similarity
                        best_match = (page_num + 1, similarity)
                
                except Exception as e:
                    continue
            
            return best_match
    
    except Exception as e:
        logger.log(f"      ✗ Fehler: {e}", also_print=False)
        return None


def apply_correction(citation: Dict, new_page: int, logger: Logger) -> bool:
    """Wendet eine Korrektur SOFORT an"""
    try:
        filename = citation['file']
        filepath = CHAPTERS_DIR / filename
        
        content = filepath.read_text(encoding='utf-8')
        
        old_match = citation['full_match']
        old_page_info = citation['page_info']
        new_page_info = str(new_page)
        
        new_match = old_match.replace(f'[{old_page_info}]', f'[{new_page_info}]')
        content = content.replace(old_match, new_match, 1)
        
        filepath.write_text(content, encoding='utf-8')
        
        logger.log(f"      ✓ Geschrieben: {filename}", also_print=False)
        return True
        
    except Exception as e:
        logger.log(f"      ✗ Schreibfehler: {e}", also_print=False)
        return False


def load_progress() -> Dict:
    """Lädt Fortschritt"""
    if PROGRESS_FILE.exists():
        try:
            with open(PROGRESS_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return {'last_index': 0}
    return {'last_index': 0}


def save_progress(index: int):
    """Speichert Fortschritt"""
    with open(PROGRESS_FILE, 'w', encoding='utf-8') as f:
        json.dump({
            'last_index': index,
            'timestamp': datetime.now().isoformat()
        }, f, indent=2)


def auto_correct_all(confidence_threshold: float = 0.50, test_mode: int = None):
    """
    Hauptfunktion - korrigiert ALLE Zitationen automatisch
    
    confidence_threshold: Minimale Ähnlichkeit zum Korrigieren (0.50 = 50%)
    test_mode: Wenn gesetzt, nur X Zitationen testen
    """
    logger = Logger(LOG_FILE)
    
    # Test Ollama
    logger.log("📡 Teste Ollama...")
    try:
        test_response = requests.post(
            'http://localhost:11434/api/generate',
            json={'model': 'llama3.2:3b', 'prompt': 'OK', 'stream': False},
            timeout=30
        )
        if test_response.status_code != 200:
            logger.log("❌ Ollama nicht erreichbar!")
            return
        logger.log("✓ Ollama läuft\n")
    except Exception as e:
        logger.log(f"❌ Ollama Fehler: {e}")
        return
    
    # Sammle Zitationen
    logger.log("📚 Sammle Zitationen...")
    all_citations = []
    
    for tex_file in CHAPTERS_DIR.glob("*.tex"):
        content = tex_file.read_text(encoding='utf-8')
        citations = extract_citations(content, tex_file.name)
        all_citations.extend(citations)
    
    logger.log(f"✓ Gefunden: {len(all_citations)} Zitationen\n")
    
    # Lade Progress
    progress = load_progress()
    start_index = progress.get('last_index', 0)
    
    if start_index > 0:
        logger.log(f"📂 Fortsetzen ab Zitation {start_index + 1}\n")
    
    # Limitiere für Test
    if test_mode:
        all_citations = all_citations[start_index:start_index + test_mode]
        logger.log(f"⚠️ TEST-MODUS: Nur {len(all_citations)} Zitationen\n")
    else:
        all_citations = all_citations[start_index:]
    
    # Statistiken
    corrected = 0
    skipped = 0
    errors = 0
    
    # HAUPTSCHLEIFE - KEINE INTERAKTION
    logger.log(f"🚀 Starte automatische Korrektur (Schwelle: {confidence_threshold:.0%})\n")
    logger.log("=" * 80)
    
    for i, citation in enumerate(all_citations, 1):
        current_global_index = start_index + i
        
        logger.log(f"[{i}/{len(all_citations)}] {citation['bib_key']} - S. {citation['page_num']}")
        
        # Finde PDF
        pdf_path = find_pdf(citation['bib_key'])
        if not pdf_path:
            logger.log(f"      ⊘ PDF nicht gefunden")
            skipped += 1
            save_progress(current_global_index)
            continue
        
        # Suche beste Seite
        result = find_best_page_in_pdf(pdf_path, citation['context'], citation['page_num'], logger)
        
        if not result:
            logger.log(f"      ⊘ Keine Übereinstimmung gefunden")
            skipped += 1
            save_progress(current_global_index)
            continue
        
        suggested_page, confidence = result
        
        # AUTOMATISCHE ENTSCHEIDUNG
        if suggested_page != citation['page_num']:
            if confidence >= confidence_threshold:
                # KORRIGIEREN
                success = apply_correction(citation, suggested_page, logger)
                if success:
                    logger.log(f"      ✓ KORRIGIERT: S.{citation['page_num']} → S.{suggested_page} (Konfidenz: {confidence:.1%})")
                    corrected += 1
                else:
                    logger.log(f"      ✗ FEHLER beim Schreiben")
                    errors += 1
            else:
                # Zu niedrige Konfidenz
                logger.log(f"      ⊘ Übersprungen: S.{suggested_page} vorgeschlagen, aber Konfidenz zu niedrig ({confidence:.1%})")
                skipped += 1
        else:
            # Seite ist korrekt
            logger.log(f"      ✓ Bereits korrekt (Konfidenz: {confidence:.1%})")
        
        # Speichere Progress nach jeder Zitation
        save_progress(current_global_index)
    
    # Zusammenfassung
    logger.log("\n")
    logger.summary(corrected, skipped, errors, len(all_citations))
    
    # Lösche Progress wenn komplett fertig
    if not test_mode and current_global_index >= 426:
        PROGRESS_FILE.unlink()
        logger.log("\n✓ Progress-Datei gelöscht (alles fertig)")


def main():
    import argparse
    
    parser = argparse.ArgumentParser(description='Vollautomatische Zitations-Korrektur (KEINE GUI)')
    parser.add_argument('--threshold', type=float, default=0.50,
                       help='Konfidenz-Schwelle (default: 0.50)')
    parser.add_argument('--test', type=int, default=None,
                       help='Test-Modus: Nur X Zitationen (z.B. --test 3)')
    parser.add_argument('--reset', action='store_true',
                       help='Progress zurücksetzen und von vorne starten')
    
    args = parser.parse_args()
    
    if args.reset:
        if PROGRESS_FILE.exists():
            PROGRESS_FILE.unlink()
        print("✓ Progress zurückgesetzt\n")
    
    print("=" * 80)
    print("🤖 VOLLAUTOMATISCHE ZITATIONS-KORREKTUR")
    print("=" * 80)
    print()
    print("Dieses Script läuft OHNE Interaktion!")
    print("Alle Ergebnisse werden ins Protokoll geschrieben.")
    print()
    print(f"Protokoll: {LOG_FILE}")
    print(f"Progress:  {PROGRESS_FILE}")
    print()
    print("=" * 80)
    print()
    
    auto_correct_all(confidence_threshold=args.threshold, test_mode=args.test)


if __name__ == "__main__":
    main()
