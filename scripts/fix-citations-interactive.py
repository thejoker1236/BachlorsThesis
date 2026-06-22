#!/usr/bin/env python3
"""
Interaktives Zitations-Korrektur-Tool
Zeigt jede Zitation an und schlägt die korrekte Seite vor
"""

import re
import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
from pathlib import Path
from typing import List, Dict, Tuple
import PyPDF2
import requests
import json

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
                
                # MEHR KONTEXT: 300 Zeichen statt 150
                start = max(0, match.start() - 300)
                end = min(len(latex_content), match.end() + 300)
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


def find_pdf(bib_key: str) -> Path:
    """Findet PDF-Datei"""
    if bib_key in PDF_MAPPING:
        for subdir in ["", "new", "Webquellen"]:
            pdf_path = SOURCES_DIR / subdir / PDF_MAPPING[bib_key]
            if pdf_path.exists():
                return pdf_path
    return None


def get_ollama_embedding(text: str) -> List[float]:
    """
    Holt Embedding von Ollama für semantische Ähnlichkeit
    """
    try:
        response = requests.post(
            'http://localhost:11434/api/embeddings',
            json={
                'model': 'llama3.2:3b',
                'prompt': text
            },
            timeout=30
        )
        if response.status_code == 200:
            return response.json()['embedding']
        else:
            print(f"Ollama Fehler: {response.status_code}")
            return None
    except Exception as e:
        print(f"Ollama Verbindungsfehler: {e}")
        return None


def cosine_similarity(a: List[float], b: List[float]) -> float:
    """
    Berechnet Kosinus-Ähnlichkeit zwischen zwei Vektoren
    """
    if not a or not b or len(a) != len(b):
        return 0.0
    
    dot_product = sum(x * y for x, y in zip(a, b))
    magnitude_a = sum(x * x for x in a) ** 0.5
    magnitude_b = sum(x * x for x in b) ** 0.5
    
    if magnitude_a == 0 or magnitude_b == 0:
        return 0.0
    
    return dot_product / (magnitude_a * magnitude_b)


def search_text_in_pdf(pdf_path: Path, search_text: str, max_pages: int = None) -> List[Tuple[int, float]]:
    """
    Sucht Text in PDF mit Ollama semantischer Ähnlichkeit
    Gibt Liste von (page_num, score) zurück
    """
    results = []
    
    try:
        # Bereite Suchtext vor - entferne LaTeX und Sonderzeichen
        clean_search = re.sub(r'\\[a-zA-Z]+(\{[^}]*\}|\[[^\]]*\])?', '', search_text)
        clean_search = re.sub(r'[^a-zA-Z0-9äöüÄÖÜß\s.,;:-]', ' ', clean_search)
        clean_search = re.sub(r'\s+', ' ', clean_search).strip()
        
        # Begrenze auf ~200 Wörter für besseres Matching
        words = clean_search.split()
        if len(words) > 200:
            clean_search = ' '.join(words[:200])
        
        print(f"  Suche mit Ollama: '{clean_search[:100]}...'")
        
        # Hole Embedding für Suchtext
        search_embedding = get_ollama_embedding(clean_search)
        if not search_embedding:
            print("  ⚠️ Ollama nicht verfügbar, fallback auf Keyword-Suche")
            return search_text_in_pdf_fallback(pdf_path, clean_search)
        
        print(f"  ✓ Suchtext-Embedding erhalten ({len(search_embedding)} dim)")
        
        with open(pdf_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            total_pages = len(reader.pages)
            
            print(f"  Durchsuche {total_pages} Seiten...")
            
            # Sample pages intelligenter: 
            # - Erste 10 Seiten (oft Einleitung)
            # - Jede 5. Seite danach bis 100
            # - Jede 10. Seite danach
            pages_to_check = list(range(min(10, total_pages)))
            pages_to_check.extend(range(10, min(100, total_pages), 5))
            pages_to_check.extend(range(100, total_pages, 10))
            pages_to_check = sorted(set(pages_to_check))
            
            for page_num in pages_to_check:
                try:
                    page = reader.pages[page_num]
                    page_text = page.extract_text()
                    
                    if not page_text or len(page_text.strip()) < 50:
                        continue
                    
                    # Bereite Seitentext vor
                    clean_page = re.sub(r'\s+', ' ', page_text).strip()
                    # Begrenze auf ~500 Wörter für Performance
                    page_words = clean_page.split()
                    if len(page_words) > 500:
                        clean_page = ' '.join(page_words[:500])
                    
                    # Hole Embedding für Seite
                    page_embedding = get_ollama_embedding(clean_page)
                    if not page_embedding:
                        continue
                    
                    # Berechne semantische Ähnlichkeit
                    similarity = cosine_similarity(search_embedding, page_embedding)
                    
                    if similarity > 0.3:  # Schwellwert für Relevanz
                        results.append((page_num + 1, similarity))  # +1 weil 1-indiziert
                        print(f"    Seite {page_num + 1}: {similarity:.2%} Ähnlichkeit")
                
                except Exception as e:
                    print(f"    Fehler bei Seite {page_num + 1}: {e}")
                    continue
            
            print(f"  ✓ {len(results)} relevante Seiten gefunden")
    
    except Exception as e:
        print(f"  ✗ Fehler beim Durchsuchen: {e}")
    
    # Sortiere nach Score
    results.sort(key=lambda x: x[1], reverse=True)
    return results[:10]  # Top 10


def search_text_in_pdf_fallback(pdf_path: Path, search_text: str) -> List[Tuple[int, float]]:
    """
    Fallback: Keyword-basierte Suche wenn Ollama nicht verfügbar
    """
    results = []
    
    try:
        all_words = [w.lower() for w in re.findall(r'\w+', search_text) if len(w) > 4]
        search_words = set(all_words[:15]) if len(all_words) > 15 else set(all_words)
        
        if not search_words:
            return []
        
        with open(pdf_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            total_pages = len(reader.pages)
            
            for page_num in range(total_pages):
                try:
                    page = reader.pages[page_num]
                    page_text = page.extract_text().lower()
                    
                    if not page_text:
                        continue
                    
                    page_words = set(re.findall(r'\w+', page_text))
                    common = search_words & page_words
                    
                    if common:
                        score = len(common) / len(search_words)
                        if score > 0.1:
                            results.append((page_num + 1, score))
                except Exception:
                    continue
    except Exception as e:
        print(f"Fallback-Fehler: {e}")
    
    results.sort(key=lambda x: x[1], reverse=True)
    return results[:10]


class CitationFixerGUI:
    def __init__(self, citations: List[Dict]):
        self.citations = citations
        self.corrections = []
        
        # Lade Progress
        self.current_index = self.load_progress()
        
        # GUI
        self.root = tk.Tk()
        self.root.title("Zitations-Korrektur-Tool")
        self.root.geometry("1000x700")
        
        # Progress
        progress_frame = ttk.Frame(self.root, padding="10")
        progress_frame.pack(fill=tk.X)
        
        self.progress_label = ttk.Label(progress_frame, text="", font=("Arial", 10))
        self.progress_label.pack()
        
        self.progress_bar = ttk.Progressbar(progress_frame, length=800, mode='determinate')
        self.progress_bar.pack(pady=5)
        
        # Info Frame
        info_frame = ttk.LabelFrame(self.root, text="Zitation", padding="10")
        info_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # BibKey und Datei
        ttk.Label(info_frame, text="Quelle:", font=("Arial", 10, "bold")).grid(row=0, column=0, sticky=tk.W)
        self.bibkey_label = ttk.Label(info_frame, text="", font=("Arial", 10))
        self.bibkey_label.grid(row=0, column=1, sticky=tk.W, padx=10)
        
        ttk.Label(info_frame, text="Datei:", font=("Arial", 10, "bold")).grid(row=1, column=0, sticky=tk.W)
        self.file_label = ttk.Label(info_frame, text="", font=("Arial", 10))
        self.file_label.grid(row=1, column=1, sticky=tk.W, padx=10)
        
        ttk.Label(info_frame, text="PDF:", font=("Arial", 10, "bold")).grid(row=2, column=0, sticky=tk.W)
        self.pdf_label = ttk.Label(info_frame, text="", font=("Arial", 9), foreground="blue")
        self.pdf_label.grid(row=2, column=1, sticky=tk.W, padx=10)
        
        ttk.Label(info_frame, text="Aktuelle Seite:", font=("Arial", 10, "bold")).grid(row=3, column=0, sticky=tk.W)
        self.current_page_label = ttk.Label(info_frame, text="", font=("Arial", 10))
        self.current_page_label.grid(row=3, column=1, sticky=tk.W, padx=10)
        
        # Button zum PDF öffnen
        self.open_pdf_button = ttk.Button(info_frame, text="📄 PDF öffnen", command=self.open_pdf)
        self.open_pdf_button.grid(row=3, column=2, sticky=tk.W, padx=10)
        
        # Kontext
        ttk.Label(info_frame, text="Kontext im Text:", font=("Arial", 10, "bold")).grid(row=4, column=0, sticky=tk.NW, pady=10)
        self.context_text = scrolledtext.ScrolledText(info_frame, height=12, width=90, wrap=tk.WORD, font=("Arial", 9))
        self.context_text.grid(row=4, column=1, columnspan=2, sticky=tk.EW, pady=10)
        
        # Vorschläge
        suggest_frame = ttk.LabelFrame(self.root, text="Vorgeschlagene Seiten (basierend auf Textsuche)", padding="10")
        suggest_frame.pack(fill=tk.X, padx=10, pady=5)
        
        self.suggestions_label = ttk.Label(suggest_frame, text="", font=("Arial", 10))
        self.suggestions_label.pack()
        
        # Eingabe
        input_frame = ttk.Frame(self.root, padding="10")
        input_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Label(input_frame, text="Neue Seite:", font=("Arial", 10, "bold")).pack(side=tk.LEFT, padx=5)
        self.page_entry = ttk.Entry(input_frame, width=10, font=("Arial", 12))
        self.page_entry.pack(side=tk.LEFT, padx=5)
        self.page_entry.bind('<Return>', lambda e: self.next_citation())
        
        # Buttons
        button_frame = ttk.Frame(self.root, padding="10")
        button_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Button(button_frame, text="Übernehmen", command=self.next_citation).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Überspringen (beh alten)", command=self.skip_citation).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Fertig & Speichern", command=self.finish).pack(side=tk.RIGHT, padx=5)
        
        # Zeige erste Zitation
        self.show_citation()
    
    def load_progress(self) -> int:
        """Lädt Progress aus JSON-Datei"""
        if PROGRESS_FILE.exists():
            try:
                data = json.loads(PROGRESS_FILE.read_text(encoding='utf-8'))
                index = data.get('current_index', 0)
                print(f"📂 Progress geladen: Starte bei Zitation {index + 1}")
                if index > 0:
                    messagebox.showinfo("Progress", f"Fortschritt wiederhergestellt!\nStarte bei Zitation {index + 1}")
                return index
            except:
                return 0
        return 0
    
    def save_progress(self):
        """Speichert Progress in JSON-Datei nach jeder Entscheidung"""
        data = {
            'current_index': self.current_index,
            'corrections_count': len(self.corrections),
            'total': len(self.citations),
            'timestamp': str(Path(__file__).stat().st_mtime)
        }
        PROGRESS_FILE.write_text(json.dumps(data, indent=2), encoding='utf-8')
        print(f"💾 Progress: {self.current_index}/{len(self.citations)}")
    
    def show_citation(self):
        if self.current_index >= len(self.citations):
            self.finish()
            return
        
        citation = self.citations[self.current_index]
        
        # Progress
        self.progress_label.config(text=f"Zitation {self.current_index + 1} von {len(self.citations)}")
        self.progress_bar['value'] = (self.current_index / len(self.citations)) * 100
        
        # Info
        self.bibkey_label.config(text=citation['bib_key'])
        self.file_label.config(text=citation['file'])
        self.current_page_label.config(text=f"S. {citation['page_num']}")
        
        # PDF-Info
        pdf_path = find_pdf(citation['bib_key'])
        if pdf_path:
            self.pdf_label.config(text=pdf_path.name)
            self.current_pdf_path = pdf_path  # Speichere für open_pdf
        else:
            self.pdf_label.config(text="❌ PDF nicht gefunden", foreground="red")
            self.current_pdf_path = None
        
        # Kontext
        self.context_text.delete(1.0, tk.END)
        self.context_text.insert(1.0, citation['context'])
        
        # Suche bessere Seite
        if pdf_path:
            self.suggestions_label.config(text="Suche im PDF...", foreground="blue")
            self.root.update()  # Update GUI
            
            # Extrahiere relevanten Text aus Kontext (ohne LaTeX-Befehle)
            clean_context = re.sub(r'\\[a-zA-Z]+(\{[^}]*\}|\[[^\]]*\])?', '', citation['context'])
            clean_context = re.sub(r'\s+', ' ', clean_context).strip()
            
            # Entferne auch Sonderzeichen
            clean_context = re.sub(r'[^a-zA-Z0-9äöüÄÖÜß\s]', ' ', clean_context)
            
            print(f"Suche für {citation['bib_key']} in {pdf_path.name}...")
            print(f"Suchtext: {clean_context[:100]}...")
            
            suggestions = search_text_in_pdf(pdf_path, clean_context)
            
            print(f"Gefunden: {len(suggestions)} Vorschläge")
            
            if suggestions:
                suggest_text = "Vorschläge: " + ", ".join([f"S. {p} ({s:.0%})" for p, s in suggestions[:5]])
                self.suggestions_label.config(text=suggest_text, foreground="green")
                # Setze besten Vorschlag in Entry
                self.page_entry.delete(0, tk.END)
                self.page_entry.insert(0, str(suggestions[0][0]))
            else:
                self.suggestions_label.config(text="Keine Vorschläge gefunden (Text nicht im PDF gefunden)", foreground="orange")
                self.page_entry.delete(0, tk.END)
                self.page_entry.insert(0, str(citation['page_num']))
        else:
            self.suggestions_label.config(text="PDF nicht gefunden", foreground="red")
            self.page_entry.delete(0, tk.END)
            self.page_entry.insert(0, str(citation['page_num']))
        
        self.page_entry.focus()
        self.page_entry.select_range(0, tk.END)
    
    def open_pdf(self):
        """Öffnet das aktuelle PDF"""
        if hasattr(self, 'current_pdf_path') and self.current_pdf_path:
            import subprocess
            import os
            try:
                os.startfile(str(self.current_pdf_path))  # Windows
            except:
                try:
                    subprocess.run(['xdg-open', str(self.current_pdf_path)])  # Linux
                except:
                    messagebox.showerror("Fehler", f"Konnte PDF nicht öffnen: {self.current_pdf_path}")
        else:
            messagebox.showwarning("Kein PDF", "Keine PDF-Datei für diese Zitation gefunden.")
    
    def next_citation(self):
        citation = self.citations[self.current_index]
        new_page = self.page_entry.get().strip()
        
        if new_page and new_page.isdigit():
            new_page_num = int(new_page)
            if new_page_num != citation['page_num']:
                # SOFORT anwenden!
                self.apply_single_correction(citation, citation['page_num'], new_page_num)
                self.corrections.append({
                    'citation': citation,
                    'old_page': citation['page_num'],
                    'new_page': new_page_num
                })
        
        self.current_index += 1
        self.save_progress()  # Speichere nach jeder Entscheidung!
        self.show_citation()
    
    def apply_single_correction(self, citation, old_page, new_page):
        """Wendet EINE Korrektur SOFORT an"""
        filename = citation['file']
        filepath = CHAPTERS_DIR / filename
        
        # Lese Datei
        content = filepath.read_text(encoding='utf-8')
        
        # Ersetze
        old_match = citation['full_match']
        old_page_info = citation['page_info']
        new_page_info = str(new_page)
        
        new_match = old_match.replace(f'[{old_page_info}]', f'[{new_page_info}]')
        content = content.replace(old_match, new_match, 1)
        
        # Schreibe SOFORT zurück
        filepath.write_text(content, encoding='utf-8')
        
        print(f"✓ Geschrieben: {filename} - {citation['bib_key']} S.{old_page} → S.{new_page}")
    
    def skip_citation(self):
        self.current_index += 1
        self.save_progress()  # Auch beim Überspringen speichern!
        self.show_citation()
    
    def finish(self):
        messagebox.showinfo("Fertig", f"{len(self.corrections)} Korrekturen wurden bereits angewendet!")
        self.root.quit()
    
    def apply_corrections(self):
        """DEPRECATED - Wird nicht mehr verwendet, weil wir sofort schreiben"""
        pass
    
    def run(self):
        self.root.mainloop()


def main():
    print("Sammle Zitationen...")
    all_citations = []
    
    for tex_file in CHAPTERS_DIR.glob("*.tex"):
        content = tex_file.read_text(encoding='utf-8')
        citations = extract_citations(content, tex_file.name)
        all_citations.extend(citations)
    
    print(f"Gefunden: {len(all_citations)} Zitationen mit Seitenangaben")
    
    # Starte GUI
    app = CitationFixerGUI(all_citations)
    app.run()


if __name__ == "__main__":
    main()
