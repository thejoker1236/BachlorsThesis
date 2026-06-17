# Priorisierte Aufgabenliste – Thesis-Überarbeitung

Ich habe die aktuelle Thesis entlang der Forschungsfrage geprüft. Mein klares Urteil ist:

Dir fehlt nicht mehr Inhalt über gesellschaftliche Gefahren oder Verhaltensbeeinflussung. Davon hast du bereits sehr viel. Am stärksten fehlt derzeit die technische Mitte zwischen Datenerfassung und Verhaltensbeeinflussung: Wie werden Daten konkret analysiert, in Bewertungen übersetzt und anschließend für Entscheidungen beziehungsweise Interventionen verwendet?

Deine Forschungsfrage besteht eigentlich aus vier Teilen:

| Teil der Forschungsfrage | Aktueller Stand | Bewertung |
|---|---|---|
| Wie funktionieren Monitoring-Systeme? | Monitoring-Zyklus und Teilsysteme sind vorhanden | gut, aber noch zu abstrakt |
| Als digitale Informationssysteme | durch das neue Kapitel 2.3.1 deutlich verbessert | grundsätzlich gut |
| Datenbasierte Analyse | nur relativ knapp und unsystematisch behandelt | größte inhaltliche Lücke |
| Beeinflussung von Verhalten | sehr ausführlich in Kapitel 3 und 4 | stark, teilweise zu absolut formuliert |

Die neue Einordnung in Kapitel 2.3.1 war also die richtige erste Aufgabe. Sie erklärt jetzt das Monitoring-Gesamtsystem, die soziotechnischen Komponenten und den idealtypischen Zyklus.

---

## 1. Größte Lücke: Datenbasierte Analyse

Kapitel 2.1.2 und 2.3.3 sind dafür noch zu schwach. Der Text nennt einzelne Verfahren wie Hidden-Markov-Modelle, Anomalieerkennung, NLP und Sentiment Analysis. Es entsteht aber noch kein zusammenhängendes Bild davon, wie die Analyse innerhalb eines Monitoring-Systems tatsächlich abläuft. Kapitel 2.3.3 umfasst praktisch nur etwa eine Seite.

Es fehlen insbesondere:

- Datenbereinigung und Datenaufbereitung
- Merkmalsextraktion beziehungsweise Feature Engineering
- Unterscheidung zwischen Training und späterer Anwendung eines Modells
- Klassifikation, Regression und Clustering
- Erzeugung von Wahrscheinlichkeiten und Scores
- Bewertung der Modellgüte
- Auswirkungen von Datenqualität und verzerrten Trainingsdaten
- Übergang vom Analyseergebnis zur algorithmischen Entscheidung

Gerade dieser Übergang ist für die Forschungsfrage zentral:

**Rohdaten → Merkmale → Modell → Prognose oder Score → Ranking beziehungsweise Entscheidung → mögliche Intervention**

Aktuell springt die Arbeit relativ schnell von Datenerfassung zu Profilbildung und anschließend zu Ranking, Scoring und Nudging. Die tatsächliche analytische Verarbeitung dazwischen bleibt zu kurz.

**Empfehlung:** Kapitel 2.1.2 und 2.3.3 gezielt um ungefähr zwei bis drei Seiten erweitern. Das sollte unsere nächste einzelne Aufgabe werden.

---

## 2. Die Funktionsweise ist noch nicht als konkrete Systemarchitektur dargestellt

Du hast nun einen idealtypischen Monitoring-Zyklus:

**Datenerfassung → Profilbildung → Analyse → Prognose und Bewertung → Intervention → erneute Datenerfassung**

Das ist gut. Aber die Arbeit zeigt noch nicht ausreichend, welche technischen und organisatorischen Komponenten diese Schritte realisieren.

Eine sinnvolle Referenzarchitektur könnte unterscheiden zwischen:

- Datenquellen und Sensoren
- Datenerfassung und Integration
- Speicherung und Profilverwaltung
- Analyse- und KI-Schicht
- Entscheidungs- und Bewertungsschicht
- Ausgabekanäle und Interventionen
- Feedback und Governance

Kapitel 2.2 beschreibt zwar Client-Server-Systeme, SOA, Cloud-Systeme und Plattformen. Diese allgemeinen Architekturen werden aber noch nicht vollständig zu einer spezifischen Architektur eines KI-gestützten Monitoring-Systems zusammengesetzt.

Dafür wäre später eine Abbildung des Monitoring-Systems sehr wertvoll. Dadurch würdest du zugleich das aktuell leere Abbildungsverzeichnis sinnvoll nutzen.

---

## 3. Kapitel 3 sollte den Monitoring-Zyklus tatsächlich anwenden

Kapitel 3 behandelt Social Media, Nutzerprofile, Personalisierung, Ranking und Scoring ausführlich. Der neu eingeführte Monitoring-Zyklus wird dort aber noch nicht konsequent als Analyserahmen verwendet.

Bei jedem Systemtyp sollte erkennbar werden:

- Was wird erfasst?
- Von wem?
- Mit welchem Ziel?
- Wie werden die Daten analysiert?
- Welches Modell oder welche Bewertung entsteht?
- Welche Entscheidung folgt daraus?
- Wie wird auf das Verhalten eingewirkt?
- Welche neuen Daten entstehen durch die Reaktion?

Aktuell sind diese Bestandteile vorhanden, aber über mehrere Unterkapitel verteilt. Eine kriteriengeleitete Zusammenführung würde die Beantwortung der Forschungsfrage wesentlich klarer machen.

Besonders für Kapitel 3.3 wäre eine Vergleichstabelle sinnvoll:

| Kriterium | Plattformzentriertes System | Staatlich integriertes System |
|---|---|---|
| Überwachtes Subjekt | Nutzer/Konsument | Bürger/Organisation |
| Primäres Ziel | Engagement und Monetarisierung | Compliance und Governance |
| Datenquellen | Interaktionen, Klicks, Profile | Verwaltungs-, Verhaltens- und Sensordaten |
| Analyse | Präferenz- und Engagement-Prognose | Risiko-, Regel- und Vertrauensbewertung |
| Intervention | Ranking, Empfehlungen, Werbung | Anreize, Einschränkungen, Sanktionen |
| Rückkopplung | erneute Nutzerinteraktion | erneutes beobachtetes Verhalten |

Das würde ungefähr eine bis zwei sinnvolle Seiten bringen, ohne künstlich zu strecken.

---

## 4. „Ermöglichen" und „tatsächlich bewirken" müssen sauber getrennt werden

Das Wort „ermöglichen" in deiner Forschungsfrage ist wichtig.

Du musst zeigen, durch welche Systemfähigkeiten Beeinflussung möglich wird:

- Auswahl von Informationen
- Reihenfolge und Sichtbarkeit
- Personalisierung
- zeitliche Platzierung
- psychologisches Profiling
- Anreize und Sanktionen
- iterative Anpassung durch Feedback

Das ist nicht dasselbe wie der Nachweis, dass jeder Nutzer tatsächlich in der gewünschten Weise reagiert.

An mehreren Stellen verwendet die Thesis sehr starke Formulierungen wie:

- „bewies"
- „massiv beeinflussen"
- „garantierte kommerzielle Ergebnisse"
- „gezielte Verhaltenssteuerung"
- „fundamentale Transformation"

Deine kritischen Kapitel relativieren diese Aussagen später zwar teilweise. Trotzdem sollte schon in Kapitel 3 und 4 sauber unterschieden werden zwischen:

- technischer Möglichkeit,
- intendierter Wirkung,
- beobachteter Korrelation,
- experimentell nachgewiesenem Effekt,
- langfristiger kausaler Wirkung.

Das würde die wissenschaftliche Qualität deutlich erhöhen, ohne zwingend viele zusätzliche Seiten zu benötigen.

---

## 5. Die Methodik ist noch nicht ausreichend reproduzierbar

Du bezeichnest dein Vorgehen als systematische Literaturrecherche. Es fehlen aber wesentliche Angaben, damit ein Leser die Suche nachvollziehen könnte:

- genaue Suchstrings
- Suchzeitraum
- Datum der letzten Suche
- Anzahl gefundener Quellen
- Ausschlusskriterien
- Anzahl ausgeschlossener Quellen
- Vorgehen bei Vorwärts- und Rückwärtssuche
- Zuordnung der Literatur zu den Analysekategorien

Kapitel 1.3 und 2.4 beschreiben das Vorgehen momentan eher allgemein.

Eine kleine Tabelle mit Datenbanken, Suchbegriffen, Suchzeitraum und Auswahlkriterien würde ungefähr eine bis zwei Seiten schaffen und die methodische Glaubwürdigkeit erheblich stärken.

---

## 6. Kritisches Problem: Quellen und Seitenzahlen

Ich habe in der aktuellen PDF 61 sichtbare „TODO: Quelle einfügen"-Platzhalter gezählt. Sie befinden sich vor allem in Kapitel 1 und 2. In diesem Zustand wäre die Arbeit noch nicht abgabefähig.

Zusätzlich erscheinen einige Seitenangaben in späteren Kapiteln verdächtig, beispielsweise Seitenzahlen von über 500 oder 800 bei Büchern. Dabei könnte es sich um E-Book-Positionen statt um echte Seitenzahlen handeln. Das muss gegen die tatsächliche verwendete Ausgabe geprüft werden.

Das ist kein kleiner Formatfehler, sondern ein wissenschaftlich kritisches Thema. Die Quellen sollten jedoch jeweils zusammen mit der Überarbeitung des entsprechenden Abschnitts ergänzt werden, statt alle TODOs blind durch irgendeine Literatur zu ersetzen.

---

## 7. Inhaltliche Wiederholungen

Mehrere Themen erscheinen mehrfach:

- Plattformökosysteme in 2.2.3, 3.1.2 und 4.3
- Datafication und digitale Fußabdrücke in 2.3.2, 3.1 und 4.1
- Ranking und Personalisierung in 2.1.3, 3.2 und 4.1/4.2
- Black-Box-Probleme in Kapitel 3, 4 und 5

Das bedeutet nicht, dass du diese Abschnitte löschen sollst. Sie müssen aber unterschiedliche Funktionen erfüllen:

- Kapitel 2: Begriffe und Funktionsweise
- Kapitel 3: Anwendung und Systemvergleich
- Kapitel 4: Auswirkungen
- Kapitel 5: Grenzen und kritische Bewertung

Neue Seiten sollten deshalb nicht durch weitere Wiederholungen entstehen, sondern durch Analyse, Vergleich und Synthese.

---

## Priorisierte Empfehlung

1. Datenbasierte Analyse in 2.1.2 und 2.3.3 ausbauen und belegen.
2. Monitoring-Zyklus als technische Referenzarchitektur darstellen.
3. Monitoring-Zyklus in Kapitel 3 auf Plattform- und staatliche Systeme anwenden.
4. Ermöglichung von Einfluss von tatsächlich nachgewiesener Wirkung trennen.
5. Methodisches Vorgehen reproduzierbar dokumentieren.
6. Alle Quellenplatzhalter und fragwürdigen Seitenangaben prüfen.
7. Abbildungs-, Tabellen- und Formelverzeichnisse bereinigen.

Mit diesen Ergänzungen kommst du voraussichtlich von derzeit 51 Textseiten auf ungefähr 58 bis 61 Textseiten, ohne die Arbeit künstlich aufzublähen.

---

## Nächster einzelner Arbeitsschritt

**Kapitel 2.1.2 und 2.3.3 so überarbeiten, dass die vollständige datenbasierte Analysekette eines KI-gestützten Monitoring-Systems wissenschaftlich nachvollziehbar erklärt wird.**

Das ist momentan die größte inhaltliche Lücke zwischen deiner Forschungsfrage und dem vorhandenen Text.
