# Zitations-Korrektur-Tools - Anleitung

## Übersicht

Du hast jetzt **2 Tools** zur Verfügung, um die 426 falschen Zitationen zu korrigieren:

### 1. **Interaktives Tool** (`fix-citations-interactive.py`)
- **Mit Ollama-Integration** für semantische Textsuche
- Zeigt jede Zitation einzeln an
- Du entscheidest bei jeder Zitation
- Tool zeigt: PDF-Name, Kontext, vorgeschlagene Seite
- Button zum PDF öffnen

### 2. **Automatisches Tool** (`auto-fix-citations.py`) ⭐ NEU
- **Vollautomatisch mit Ollama LLM**
- Analysiert alle Zitationen automatisch
- Bewertet semantische Ähnlichkeit zwischen Text und PDF-Seiten
- Zeigt nur Korrekturen zur Review an
- Schneller, aber weniger Kontrolle

---

## Tool 1: Interaktives Tool

### Verwendung

```powershell
cd c:\development\PrivProjects\BachlorsThesis
python scripts\fix-citations-interactive.py
```

### Funktionsweise

1. Zeigt jede Zitation mit Kontext
2. Sucht mit Ollama semantisch ähnliche Seiten im PDF
3. Schlägt beste Übereinstimmung vor
4. Du kannst:
   - Vorschlag akzeptieren (Enter)
   - Seitenzahl manuell ändern
   - PDF öffnen zum Überprüfen
   - Überspringen (behält alte Seite)
5. Am Ende: Alle Änderungen werden angewendet

### Vorteile
- ✅ Volle Kontrolle über jede Entscheidung
- ✅ Kannst PDF parallel öffnen und prüfen
- ✅ Siehst jeden Kontext

### Nachteile
- ❌ Zeitaufwändig (426 Zitationen!)
- ❌ Musst bei jeder Zitation entscheiden

---

## Tool 2: Automatisches Tool ⭐

### Verwendung

**Basis-Modus (mit GUI-Review):**
```powershell
cd c:\development\PrivProjects\BachlorsThesis
python scripts\auto-fix-citations.py
```

**Mit Optionen:**
```powershell
# Nur Report, keine GUI
python scripts\auto-fix-citations.py --no-gui

# Niedrigere Schwelle (mehr Korrekturen, weniger konservativ)
python scripts\auto-fix-citations.py --threshold 0.40

# Test mit nur 10 Zitationen
python scripts\auto-fix-citations.py --max-citations 10

# Kombiniert
python scripts\auto-fix-citations.py --threshold 0.40 --max-citations 50
```

### Funktionsweise

1. **Analyse-Phase** (automatisch):
   - Lädt alle Zitationen
   - Für jede Zitation:
     - Extrahiert Kontext aus LaTeX
     - Sucht im PDF mit Ollama LLM
     - Vergleicht semantische Ähnlichkeit
     - Bewertet Konfidenz (0-100%)
   
2. **Review-Phase** (GUI):
   - Zeigt nur Korrekturen über Konfidenz-Schwelle
   - Du kannst:
     - ✓ Akzeptieren (Enter)
     - ✗ Ablehnen (Esc)
     - PDF öffnen
   - Viel schneller als Tool 1!

3. **Anwendung**:
   - Nur akzeptierte Korrekturen werden angewendet

### Parameter

- `--threshold 0.50` (default): Nur Korrekturen mit ≥50% Konfidenz
  - `0.70`: Sehr konservativ (nur sehr sicher)
  - `0.50`: Balanciert ⭐
  - `0.40`: Aggressiver (mehr Korrekturen)
  - `0.30`: Sehr aggressiv

- `--max-citations N`: Limitiere auf N Zitationen (für Tests)

- `--no-gui`: Nur Report ausgeben, keine GUI

### Vorteile
- ✅ **Viel schneller** (LLM macht die Arbeit)
- ✅ Konsistente Bewertung
- ✅ Zeigt nur relevante Korrekturen
- ✅ Konfidenz-Score für jede Korrektur
- ✅ Kann alle 426 Zitationen in ~1-2 Stunden verarbeiten

### Nachteile
- ❌ LLM kann Fehler machen
- ❌ Weniger Kontext als bei manuellem Review
- ❌ Langsam wegen vielen API-Aufrufen

---

## Empfehlung

### Option A: Schnell & Effizient ⭐
```powershell
# 1. Automatische Analyse mit moderater Schwelle
python scripts\auto-fix-citations.py --threshold 0.50

# 2. Review in GUI (dauert nur 5-10 Min statt Stunden)
# 3. Akzeptiere/Ablehne Vorschläge
```

### Option B: Volle Kontrolle
```powershell
# Interaktives Tool für alle 426 Zitationen
python scripts\fix-citations-interactive.py
# ⚠️ Dauert mehrere Stunden!
```

### Option C: Hybrid (BESTE OPTION) 🏆
```powershell
# 1. Automatisch mit hoher Schwelle (nur sehr sichere)
python scripts\auto-fix-citations.py --threshold 0.70

# 2. Rest mit interaktivem Tool
python scripts\fix-citations-interactive.py
```

---

## Technische Details

### Wie funktioniert die Ollama-Integration?

**Interaktives Tool:**
- Keyword-Matching als Fallback
- Ollama wurde integriert, aber funktioniert ähnlich

**Automatisches Tool:**
- Verwendet `llama3.2:3b` Modell
- Prompt: "Vergleiche TEXT 1 (Kontext) und TEXT 2 (PDF-Seite)"
- LLM gibt Ähnlichkeits-Score 0-100
- Prüft intelligente Auswahl an Seiten:
  - Aktuelle Seite ±10 Seiten (Priorität)
  - Erste 15 Seiten
  - Jede 10. Seite danach
- Maximal 30 Seiten pro Zitation (Performance)

### Performance

**Geschwindigkeit pro Zitation:**
- ~30 Seiten × ~2-3 Sekunden pro LLM-Aufruf
- ≈ 60-90 Sekunden pro Zitation
- 426 Zitationen = **~10-15 Stunden** für alles

**Optimierungen:**
- Intelligentes Sampling (nicht alle Seiten)
- Priorität auf aktuelle Seite und Umgebung
- Textlänge begrenzt auf 200-300 Wörter

---

## Aktuelle Situation

- **426 Zitationen** mit Fehlern
- **0% korrekt**
- **53.3% Mismatches** (Text passt nicht zur Seite)
- **44.1% Seitenfehler** (Seite existiert nicht)

Vollständiger Report: `.kiro\specs\quellenprufung\zitations-validierung.md`

---

## Nächste Schritte

1. **Entscheide** welches Tool oder welche Strategie
2. **Starte** Korrektur-Prozess
3. **Verifiziere** nach Korrektur:
   ```powershell
   python scripts\verify-citations.py
   ```
4. **Kompiliere** Thesis und prüfe Ausgabe

---

## Fragen?

- Beide Tools sind **sicher** (Backup wird nicht automatisch gemacht, aber Git!)
- Änderungen werden erst **am Ende** angewendet
- Du kannst **jederzeit abbrechen**
- **Test** zuerst mit `--max-citations 10`

---

## Beispiel-Workflow

```powershell
# 1. Test mit 10 Zitationen
python scripts\auto-fix-citations.py --max-citations 10 --threshold 0.50

# 2. Prüfe Ergebnisse in GUI

# 3. Wenn zufrieden, alle durchlaufen lassen
python scripts\auto-fix-citations.py --threshold 0.50

# ⏰ Gehe Kaffee trinken (dauert ~2 Stunden)

# 4. Review in GUI (schnell)

# 5. Verifiziere
python scripts\verify-citations.py

# 6. Kompiliere
.\scripts\compile.ps1
```
