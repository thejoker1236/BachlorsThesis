#!/usr/bin/env python3
"""
Automatisches Zitations-Korrektur-Tool mit Ollama LLM
Findet und korrigiert Seitenzahlen automatisch basierend auf semantischer Ähnlichkeit
"""

import re
import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
from pathlib import Path
from typing import List, Dict, Tuple, Optional
import PyPDF2
import requests
import json
from datetime import datetime

# Progress-Datei - im selben Ordner wie das Script
SCRIPT_DIR = Path(__file__).parent
PROGRESS_FILE = SCRIPT_DIR / "korrektur-progress.json"

# Pfade
PAPER_DIR = Path(r"c:\development\PrivProjects\BachlorsThesis\Paper")
SOURCES_DIR = Path(r"c:\development\PrivProjects\BachlorsThesis\sources")
CHAPTERS_DIR = PAPER_DIR / "chapters"

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


def load_progress() -> Dict:
    """Lädt Fortschritt aus JSON-Datei"""
    if PROGRESS_FILE.exists():
        try:
            with open(PROGRESS_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"⚠️ Konnte Fortschritt nicht laden: {e}")
    
    return {
        "last_processed_index": 0,
        "total_citations": 0,
        "completed_citations": 0,
        "corrections_made": [],
        "session_start": datetime.now().isoformat(),
        "last_update": datetime.now().isoformat()
    }


def save_progress(progress: Dict):
    """Speichert Fortschritt in JSON-Datei"""
    try:
        progress["last_update"] = datetime.now().isoformat()
        PROGRESS_FILE.parent.mkdir(parents=True, exist_ok=True)
        with open(PROGRESS_FILE, 'w', encoding='utf-8') as f:
            json.dump(progress, f, indent=2, ensure_ascii=False)
    except Exception as e:
        print(f"⚠️ Konnte Fortschritt nicht speichern: {e}")


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
                    'temperature': 0.1,  # Niedrig für konsistente Bewertung
                    'num_predict': 5     # Nur 5 Tokens (die Zahl) - schneller
                }
            },
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()['response'].strip()
            # Extrahiere Zahl aus Antwort
            match = re.search(r'(\d+)', result)
            if match:
                score = int(match.group(1))
                return min(score / 100.0, 1.0)  # Normalisiere auf 0-1
            else:
                # Fallback: wenn keine Zahl, dann 0.5 (unsicher)
                return 0.5
        
        return 0.0
        
    except Exception as e:
        print(f"      LLM-Fehler: {e}")
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
            
            # Extrahiere Seitenzahl
            page_match = re.search(r'S\.[\s~]*(\d+)', page_info)
            if not page_match:
                page_match = re.search(r'^(\d+)$', page_info.strip())
            if not page_match:
                page_match = re.search(r'(\d+)', page_info)
            
            if page_match:
                page_num = int(page_match.group(1))
                
                # Kontext extrahieren (400 Zeichen für besseres Matching)
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


def find_best_page_in_pdf(pdf_path: Path, search_text: str, current_page: int) -> Optional[Tuple[int, float]]:
    """
    Findet die beste Seite im PDF basierend auf semantischer Ähnlichkeit mit Ollama
    """
    try:
        # Bereite Suchtext vor
        clean_search = re.sub(r'\\[a-zA-Z]+(\{[^}]*\}|\[[^\]]*\])?', '', search_text)
        clean_search = re.sub(r'[^a-zA-Z0-9äöüÄÖÜß\s.,;:-]', ' ', clean_search)
        clean_search = re.sub(r'\s+', ' ', clean_search).strip()
        
        # Begrenze auf ~200 Wörter
        words = clean_search.split()
        if len(words) > 200:
            clean_search = ' '.join(words[:200])
        
        with open(pdf_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            total_pages = len(reader.pages)
            
            # Intelligentes Sampling - PRIORISIERE aktuelle Seite und Umgebung
            pages_to_check = []
            
            # 1. Prüfe aktuelle Seite und ±10 Seiten (höchste Priorität)
            for offset in range(-10, 11):
                page = current_page - 1 + offset  # -1 weil 0-indiziert
                if 0 <= page < total_pages:
                    pages_to_check.append((page, 'high_priority'))
            
            # 2. Erste 15 Seiten
            for page in range(min(15, total_pages)):
                if (page, 'high_priority') not in pages_to_check:
                    pages_to_check.append((page, 'medium'))
            
            # 3. Jede 10. Seite danach
            for page in range(15, total_pages, 10):
                pages_to_check.append((page, 'low'))
            
            # Sortiere: high_priority zuerst
            pages_to_check.sort(key=lambda x: (0 if x[1] == 'high_priority' else 1 if x[1] == 'medium' else 2, x[0]))
            
            best_match = None
            best_score = 0.0
            checked_count = 0
            max_checks = 15  # Begrenze auf 15 Seiten für bessere Performance
            
            for page_num, priority in pages_to_check:
                if checked_count >= max_checks:
                    break
                
                try:
                    page = reader.pages[page_num]
                    page_text = page.extract_text()
                    
                    if not page_text or len(page_text.strip()) < 50:
                        continue
                    
                    # Bereite Seitentext vor
                    clean_page = re.sub(r'\s+', ' ', page_text).strip()
                    page_words = clean_page.split()
                    if len(page_words) > 300:
                        clean_page = ' '.join(page_words[:300])
                    
                    # LLM-Vergleich
                    similarity = check_text_similarity_with_ollama(clean_search, clean_page)
                    checked_count += 1
                    
                    if similarity > best_score:
                        best_score = similarity
                        best_match = (page_num + 1, similarity)  # +1 weil 1-indiziert
                        print(f"      → Seite {page_num + 1}: {similarity:.1%} (neue Bestmarke)")
                
                except Exception as e:
                    continue
            
            print(f"      Geprüft: {checked_count} Seiten")
            return best_match
    
    except Exception as e:
        print(f"    ✗ Fehler: {e}")
        return None


def auto_correct_citations(citations: List[Dict], confidence_threshold: float = 0.50, start_index: int = 0) -> List[Dict]:
    """
    Korrigiert Zitationen automatisch mit Ollama
    
    confidence_threshold: Minimale Ähnlichkeit (0.0-1.0) um Korrektur vorzuschlagen
                         0.50 = 50% Ähnlichkeit (konservativ)
                         0.40 = 40% Ähnlichkeit (moderat)
                         0.30 = 30% Ähnlichkeit (aggressiv)
    start_index: Ab welcher Zitation beginnen (für Fortsetzung)
    """
    corrections = []
    
    # Lade Fortschritt
    progress = load_progress()
    if start_index == 0 and progress["last_processed_index"] > 0:
        print(f"\n📌 Fortschritt gefunden: {progress['completed_citations']} von {progress['total_citations']} bereits bearbeitet")
        response = input(f"   Fortsetzen ab Zitation {progress['last_processed_index'] + 1}? (j/n): ").lower()
        if response == 'j' or response == 'y':
            start_index = progress["last_processed_index"]
            print(f"   ✓ Setze fort ab Zitation {start_index + 1}")
        else:
            # Reset progress
            progress = {
                "last_processed_index": 0,
                "total_citations": len(citations),
                "completed_citations": 0,
                "corrections_made": [],
                "session_start": datetime.now().isoformat(),
                "last_update": datetime.now().isoformat()
            }
            save_progress(progress)
            print("   ✓ Starte von vorne")
    
    progress["total_citations"] = len(citations)
    
    print(f"\n🔍 Analysiere {len(citations) - start_index} Zitationen mit Ollama (ab #{start_index + 1})...")
    print(f"📊 Konfidenz-Schwelle: {confidence_threshold:.0%}\n")
    
    for i in range(start_index, len(citations)):
        citation = citations[i]
        print(f"[{i + 1}/{len(citations)}] {citation['bib_key']} - S. {citation['page_num']}")
        
        pdf_path = find_pdf(citation['bib_key'])
        if not pdf_path:
            print(f"    ⚠️ PDF nicht gefunden")
            # Update progress
            progress["last_processed_index"] = i
            progress["completed_citations"] = i + 1
            save_progress(progress)
            continue
        
        # Suche beste Seite
        result = find_best_page_in_pdf(pdf_path, citation['context'], citation['page_num'])
        
        if result:
            suggested_page, confidence = result
            
            if suggested_page != citation['page_num']:
                correction_entry = {
                    'citation_index': i,
                    'bib_key': citation['bib_key'],
                    'old_page': citation['page_num'],
                    'new_page': suggested_page,
                    'confidence': confidence,
                    'timestamp': datetime.now().isoformat()
                }
                
                if confidence >= confidence_threshold:
                    corrections.append({
                        'citation': citation,
                        'old_page': citation['page_num'],
                        'new_page': suggested_page,
                        'confidence': confidence,
                        'pdf_name': pdf_path.name,
                        'status': 'auto_correct'
                    })
                    progress["corrections_made"].append(correction_entry)
                    print(f"    ✓ Korrektur: S. {citation['page_num']} → S. {suggested_page} (Konfidenz: {confidence:.1%})")
                else:
                    corrections.append({
                        'citation': citation,
                        'old_page': citation['page_num'],
                        'new_page': suggested_page,
                        'confidence': confidence,
                        'pdf_name': pdf_path.name,
                        'status': 'low_confidence'
                    })
                    print(f"    ⚠️ Vorschlag: S. {citation['page_num']} → S. {suggested_page} (Konfidenz: {confidence:.1%}, zu niedrig)")
            else:
                print(f"    ✓ Korrekt (Konfidenz: {confidence:.1%})")
        else:
            print(f"    ⚠️ Keine Übereinstimmung gefunden")
        
        # Update progress nach jeder Zitation
        progress["last_processed_index"] = i
        progress["completed_citations"] = i + 1
        save_progress(progress)
    
    return corrections


class AutoCorrectionReviewGUI:
    """GUI zur Überprüfung der automatischen Korrekturen"""
    
    def __init__(self, corrections: List[Dict], start_index: int = 0):
        self.corrections = [c for c in corrections if c['status'] == 'auto_correct']
        self.low_confidence = [c for c in corrections if c['status'] == 'low_confidence']
        self.approved = []
        self.rejected = []
        self.current_index = start_index
        
        # Load progress
        progress = load_progress()
        if progress['last_index'] > 0 and start_index == 0:
            if messagebox.askyesno("Fortschritt gefunden", 
                f"Fortschritt bei Zitation {progress['last_index']} gefunden.\n"
                f"{len(progress['completed'])} bereits bearbeitet.\n\n"
                f"Fortsetzen?"):
                self.current_index = progress['last_index']
                self.approved = progress.get('completed', [])
                self.rejected = progress.get('skipped', [])
        
        self.root = tk.Tk()
        self.root.title("Automatische Korrekturen überprüfen")
        self.root.geometry("1100x750")
        
        # Header
        header = ttk.Frame(self.root, padding="10")
        header.pack(fill=tk.X)
        
        ttk.Label(header, text="🤖 Automatische Zitations-Korrekturen", 
                 font=("Arial", 14, "bold")).pack()
        
        self.summary_label = ttk.Label(header, text="", font=("Arial", 10))
        self.summary_label.pack(pady=5)
        
        # Progress
        progress_frame = ttk.Frame(self.root, padding="10")
        progress_frame.pack(fill=tk.X)
        
        self.progress_label = ttk.Label(progress_frame, text="", font=("Arial", 10))
        self.progress_label.pack()
        
        self.progress_bar = ttk.Progressbar(progress_frame, length=900, mode='determinate')
        self.progress_bar.pack(pady=5)
        
        # Info Frame
        info_frame = ttk.LabelFrame(self.root, text="Korrektur-Details", padding="10")
        info_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Grid layout
        row = 0
        ttk.Label(info_frame, text="Quelle:", font=("Arial", 10, "bold")).grid(row=row, column=0, sticky=tk.W)
        self.bibkey_label = ttk.Label(info_frame, text="", font=("Arial", 10))
        self.bibkey_label.grid(row=row, column=1, sticky=tk.W, padx=10)
        
        row += 1
        ttk.Label(info_frame, text="PDF:", font=("Arial", 10, "bold")).grid(row=row, column=0, sticky=tk.W)
        self.pdf_label = ttk.Label(info_frame, text="", font=("Arial", 9), foreground="blue")
        self.pdf_label.grid(row=row, column=1, sticky=tk.W, padx=10)
        
        row += 1
        ttk.Label(info_frame, text="LaTeX-Datei:", font=("Arial", 10, "bold")).grid(row=row, column=0, sticky=tk.W)
        self.file_label = ttk.Label(info_frame, text="", font=("Arial", 9))
        self.file_label.grid(row=row, column=1, sticky=tk.W, padx=10)
        
        row += 1
        ttk.Label(info_frame, text="Seitenänderung:", font=("Arial", 11, "bold")).grid(row=row, column=0, sticky=tk.W, pady=10)
        self.change_label = ttk.Label(info_frame, text="", font=("Arial", 12, "bold"), foreground="blue")
        self.change_label.grid(row=row, column=1, sticky=tk.W, padx=10, pady=10)
        
        row += 1
        ttk.Label(info_frame, text="Konfidenz:", font=("Arial", 10, "bold")).grid(row=row, column=0, sticky=tk.W)
        self.confidence_label = ttk.Label(info_frame, text="", font=("Arial", 10))
        self.confidence_label.grid(row=row, column=1, sticky=tk.W, padx=10)
        
        row += 1
        ttk.Label(info_frame, text="Kontext:", font=("Arial", 10, "bold")).grid(row=row, column=0, sticky=tk.NW, pady=10)
        self.context_text = scrolledtext.ScrolledText(info_frame, height=15, width=95, wrap=tk.WORD, font=("Arial", 9))
        self.context_text.grid(row=row, column=1, columnspan=2, sticky=tk.EW, pady=10)
        
        # Buttons
        button_frame = ttk.Frame(self.root, padding="10")
        button_frame.pack(fill=tk.X, padx=10, pady=10)
        
        ttk.Button(button_frame, text="✓ Akzeptieren (Enter)", 
                  command=self.approve_correction, 
                  style="Accent.TButton").pack(side=tk.LEFT, padx=5)
        
        ttk.Button(button_frame, text="✗ Ablehnen (Esc)", 
                  command=self.reject_correction).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(button_frame, text="📄 PDF öffnen", 
                  command=self.open_pdf).pack(side=tk.LEFT, padx=20)
        
        ttk.Button(button_frame, text="💾 Fertig & Anwenden", 
                  command=self.finish).pack(side=tk.RIGHT, padx=5)
        
        # Keyboard shortcuts
        self.root.bind('<Return>', lambda e: self.approve_correction())
        self.root.bind('<Escape>', lambda e: self.reject_correction())
        
        self.update_summary()
        self.show_correction()
    
    def update_summary(self):
        text = f"Gefunden: {len(self.corrections)} automatische Korrekturen"
        if self.low_confidence:
            text += f" + {len(self.low_confidence)} niedrige Konfidenz"
        self.summary_label.config(text=text)
    
    def show_correction(self):
        if self.current_index >= len(self.corrections):
            self.finish()
            return
        
        corr = self.corrections[self.current_index]
        citation = corr['citation']
        
        # Progress
        self.progress_label.config(text=f"Korrektur {self.current_index + 1} von {len(self.corrections)}")
        self.progress_bar['value'] = (self.current_index / len(self.corrections)) * 100
        
        # Info
        self.bibkey_label.config(text=citation['bib_key'])
        self.pdf_label.config(text=corr['pdf_name'])
        self.file_label.config(text=citation['file'])
        self.change_label.config(text=f"S. {corr['old_page']} → S. {corr['new_page']}")
        
        # Konfidenz mit Farbe
        confidence = corr['confidence']
        conf_text = f"{confidence:.1%}"
        if confidence >= 0.70:
            conf_color = "green"
            conf_text += " (hoch)"
        elif confidence >= 0.50:
            conf_color = "orange"
            conf_text += " (mittel)"
        else:
            conf_color = "red"
            conf_text += " (niedrig)"
        
        self.confidence_label.config(text=conf_text, foreground=conf_color)
        
        # Kontext
        self.context_text.delete(1.0, tk.END)
        self.context_text.insert(1.0, citation['context'])
        
        self.current_pdf_path = find_pdf(citation['bib_key'])
    
    def open_pdf(self):
        if self.current_pdf_path:
            import subprocess
            import os
            try:
                os.startfile(str(self.current_pdf_path))
            except:
                try:
                    subprocess.run(['xdg-open', str(self.current_pdf_path)])
                except:
                    messagebox.showerror("Fehler", f"Konnte PDF nicht öffnen: {self.current_pdf_path}")
        else:
            messagebox.showwarning("Kein PDF", "PDF nicht gefunden.")
    
    def approve_correction(self):
        corr = self.corrections[self.current_index]
        self.approved.append(corr)
        
        # SOFORT anwenden!
        self.apply_single_correction(corr)
        
        self.current_index += 1
        
        # Speichere Fortschritt
        save_progress(self.current_index, self.approved, self.rejected)
        
        self.show_correction()
    
    def reject_correction(self):
        self.rejected.append(self.corrections[self.current_index])
        self.current_index += 1
        
        # Speichere Fortschritt
        save_progress(self.current_index, self.approved, self.rejected)
        
        self.show_correction()
    
    def apply_single_correction(self, corr):
        """Wendet EINE Korrektur SOFORT an"""
        citation = corr['citation']
        filename = citation['file']
        filepath = CHAPTERS_DIR / filename
        
        # Lese Datei
        content = filepath.read_text(encoding='utf-8')
        
        # Ersetze
        old_match = citation['full_match']
        old_page_info = citation['page_info']
        new_page_info = str(corr['new_page'])
        
        new_match = old_match.replace(f'[{old_page_info}]', f'[{new_page_info}]')
        content = content.replace(old_match, new_match, 1)
        
        # Schreibe SOFORT zurück
        filepath.write_text(content, encoding='utf-8')
        
        print(f"✓ Geschrieben: {filename} - {citation['bib_key']} S.{corr['old_page']} → S.{corr['new_page']}")
    
    def finish(self):
        message = f"{len(self.approved)} Korrekturen angewendet\n"
        message += f"{len(self.rejected)} Korrekturen abgelehnt"
        
        # Lösche Progress-Datei wenn fertig
        if PROGRESS_FILE.exists():
            PROGRESS_FILE.unlink()
        
        messagebox.showinfo("Fertig", message)
        self.root.quit()
    
    def apply_corrections(self):
        """DEPRECATED - Wird nicht mehr verwendet, weil wir sofort schreiben"""
        pass
    
    def run(self):
        self.root.mainloop()


def main():
    import argparse
    
    parser = argparse.ArgumentParser(description='Automatische Zitations-Korrektur mit Ollama')
    parser.add_argument('--threshold', type=float, default=0.50,
                       help='Konfidenz-Schwelle (0.0-1.0, default: 0.50)')
    parser.add_argument('--no-gui', action='store_true',
                       help='Ohne GUI (nur Report)')
    parser.add_argument('--max-citations', type=int, default=None,
                       help='Maximale Anzahl zu prüfender Zitationen (für Tests)')
    parser.add_argument('--reset-progress', action='store_true',
                       help='Fortschritt zurücksetzen und von vorne beginnen')
    parser.add_argument('--continue', dest='continue_from_last', action='store_true',
                       help='Automatisch von letzter Position fortsetzen')
    
    args = parser.parse_args()
    
    print("=" * 80)
    print("🤖 AUTOMATISCHE ZITATIONS-KORREKTUR MIT OLLAMA")
    print("=" * 80)
    
    # Reset progress if requested
    if args.reset_progress:
        if PROGRESS_FILE.exists():
            PROGRESS_FILE.unlink()
            print("\n✓ Fortschritt zurückgesetzt\n")
    
    # Test Ollama
    print("\n📡 Teste Ollama-Verbindung...")
    try:
        test_response = requests.post(
            'http://localhost:11434/api/generate',
            json={
                'model': 'llama3.2:3b',
                'prompt': 'Say only: OK',
                'stream': False
            },
            timeout=30
        )
        if test_response.status_code != 200:
            print("❌ FEHLER: Ollama nicht erreichbar!")
            print("   Starte Ollama mit: ollama serve")
            return
        print(f"✓ Ollama läuft (llama3.2:3b)")
    except Exception as e:
        print(f"❌ FEHLER: Ollama nicht erreichbar! {e}")
        print("   Starte Ollama mit: ollama serve")
        return
    
    # Sammle Zitationen
    print("\n📚 Sammle Zitationen...")
    all_citations = []
    
    for tex_file in CHAPTERS_DIR.glob("*.tex"):
        content = tex_file.read_text(encoding='utf-8')
        citations = extract_citations(content, tex_file.name)
        all_citations.extend(citations)
    
    print(f"✓ Gefunden: {len(all_citations)} Zitationen mit Seitenangaben")
    
    # Limitiere für Tests
    if args.max_citations:
        all_citations = all_citations[:args.max_citations]
        print(f"⚠️ Limitiert auf {len(all_citations)} Zitationen für Test")
    
    # Automatische Korrektur
    corrections = auto_correct_citations(all_citations, confidence_threshold=args.threshold)
    
    # Statistiken
    auto_corrections = [c for c in corrections if c['status'] == 'auto_correct']
    low_confidence = [c for c in corrections if c['status'] == 'low_confidence']
    
    print("\n" + "=" * 80)
    print("📊 ERGEBNIS")
    print("=" * 80)
    print(f"✓ Automatische Korrekturen: {len(auto_corrections)}")
    print(f"⚠️ Niedrige Konfidenz: {len(low_confidence)}")
    print(f"✓ Korrekt: {len(all_citations) - len(corrections)}")
    
    if not auto_corrections:
        print("\n✅ Keine Korrekturen nötig oder alle unter Schwelle!")
        return
    
    if args.no_gui:
        # Zeige Report
        print("\nKorrekturen:")
        for corr in auto_corrections[:10]:
            print(f"  {corr['citation']['bib_key']}: S. {corr['old_page']} → S. {corr['new_page']} ({corr['confidence']:.1%})")
        if len(auto_corrections) > 10:
            print(f"  ... und {len(auto_corrections) - 10} weitere")
    else:
        # Starte GUI
        print("\n🖥️ Starte Review-GUI...")
        app = AutoCorrectionReviewGUI(corrections)
        app.run()


if __name__ == "__main__":
    main()
