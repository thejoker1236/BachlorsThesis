# Quellenrecherche — FOM Bachelor-Thesis
## Wie funktionieren KI-gestützte Monitoring-Systeme als digitale Informationssysteme und inwiefern ermöglichen sie datenbasierte Analyse und Beeinflussung von Verhalten?

**Autor:** Meshan Fernando | **Matrikelnummer:** 617993  
**Erstgutachter:** (Prof. Dr. Dieter Litzinger) Oliver Bach  
**FOM Hochschule Frankfurt** | Stand: Mai 2026

---

> Diese kuratierte Literaturliste ergänzt die bestehende Bibliografie des Exposés um rund **70 neue, verifizierte akademische Quellen**. Alle Quellen sind nach Thesiskapiteln gegliedert und enthalten DOI/URL sowie eine kurze Begründung der Relevanz. Keine Quelle dupliziert die bestehende Liste aus dem Exposé.

---

## Kapitel 1 — Theoretische und technologische Grundlagen

### 1.1 Informationssystem-Theorie

**Laudon, K. C., & Laudon, J. P. (2022).** *Management information systems: Managing the digital firm* (17th ed.). Pearson. ISBN 978-0-13-697127-6.  
→ Kanonisches IS-Lehrbuch; TPS/MIS/DSS/ESS-Hierarchie, IT-Infrastruktur. Fundament zur Einordnung von Monitoring-Systemen als digitale IS.  
https://www.pearson.com/en-us/subject-catalog/p/management-information-systems-managing-the-digital-firm/P200000001392/

---

**Stair, R. M., & Reynolds, G. W. (2020).** *Principles of information systems* (14th ed.). Cengage. ISBN 978-0-357-11241-0.  
→ Technisch orientierter Komplementärtext mit eigenem Kapitel zu KI und Automation.

---

**Alter, S. (2013).** Work system theory: Overview of core concepts, extensions, and challenges for the future. *Journal of the Association for Information Systems, 14*(2), 72–121.  
DOI: 10.17705/1jais.00323 | Open Access: https://aisel.aisnet.org/jais/vol14/iss2/1/  
→ Work-System-Framework; ideales soziotechnisches Analysegerüst für KI-Monitoring.

---

**Hevner, A. R., March, S. T., Park, J., & Ram, S. (2004).** Design science in information systems research. *MIS Quarterly, 28*(1), 75–105.  
DOI: 10.2307/25148625  
→ Methodischer Anker IS-Forschung; meistzitiert.

---

**Checkland, P. (2000).** Soft systems methodology: A thirty year retrospective. *Systems Research and Behavioral Science, 17*(S1), S11–S58.  
DOI: 10.1002/1099-1743(200011)17:1+  
→ „Weiche" Systemmethodik; für die kritisch-interpretative Dimension (auch Kap. 4).

---

**Vial, G. (2019).** Understanding digital transformation: A review and a research agenda. *Journal of Strategic Information Systems, 28*(2), 118–144.  
DOI: 10.1016/j.jsis.2019.01.003  
→ Systematisches Review zu digitaler Transformation als soziotechnischer Prozess.

---

**Davenport, T. H., & Harris, J. G. (2017).** *Competing on analytics: The new science of winning* (Updated ed.). Harvard Business Review Press. ISBN 978-1-63369-372-2.  
→ Reifegradmodell für datengetriebene Entscheidungslogik.

---

### 1.2 KI-/ML-Grundlagen (Deutschsprachig)

**Ertel, W. (2021).** *Grundkurs Künstliche Intelligenz: Eine praxisorientierte Einführung* (5. Aufl.). Springer Vieweg.  
DOI: 10.1007/978-3-658-32075-1 | ISBN 978-3-658-32074-4  
→ **Deutschsprachiges Standardlehrbuch**; deckt Agenten, Wissensbasen, ML, Deep Learning und ein Kapitel „KI und Gesellschaft" ab.

---

**Frochte, J. (2020).** *Maschinelles Lernen: Grundlagen und Algorithmen in Python* (3. Aufl.). Hanser. ISBN 978-3-446-46144-4.  
→ Verbindet Mathematik und Anwendung der zentralen ML-Verfahren.

---

**Lenzen, M. (2023).** *Künstliche Intelligenz: Was sie kann & was uns erwartet* (4. Aufl.). C.H. Beck. ISBN 978-3-406-80663-6.  
→ Wissenschaftsjournalistisch fundiert, zitierfähig; verknüpft Funktionsweise mit Überwachung/Verhaltensbeeinflussung (auch Kap. 4).

---

### 1.3 Technische Schlüsselpapiere — NLP & Computer Vision

**Vaswani, A. et al. (2017).** Attention is all you need. *NeurIPS 30*, 5998–6008.  
arXiv: 1706.03762 | https://arxiv.org/abs/1706.03762  
→ **Transformer-Architektur**; technische Grundlage moderner Sprach- und Monitoring-Modelle.

---

**Devlin, J., Chang, M.-W., Lee, K., & Toutanova, K. (2019).** BERT: Pre-training of deep bidirectional transformers for language understanding. *NAACL-HLT 2019*, 4171–4186.  
DOI: 10.18653/v1/N19-1423 | https://aclanthology.org/N19-1423/  
→ Standardmodell für Content-Moderation und Hate-Speech-Detection.

---

**Brown, T. B. et al. (2020).** Language models are few-shot learners. *NeurIPS 33*, 1877–1901.  
arXiv: 2005.14165 | https://papers.nips.cc/paper/2020/hash/1457c0d6bfcb4967418bfb8ac142f64a-Abstract.html  
→ GPT-3; Skalierungssprung generativer LLMs (auch Kap. 3).

---

**He, K., Zhang, X., Ren, S., & Sun, J. (2016).** Deep residual learning for image recognition. *CVPR 2016*, 770–778.  
DOI: 10.1109/CVPR.2016.90  
→ **ResNet** als Backbone von Video-Überwachung und Face Recognition.

---

**Krizhevsky, A., Sutskever, I., & Hinton, G. E. (2017).** ImageNet classification with deep convolutional neural networks. *Communications of the ACM, 60*(6), 84–90.  
DOI: 10.1145/3065386  
→ AlexNet; historischer Anker der Deep-Learning-Revolution in Computer Vision.

---

**Ren, S., He, K., Girshick, R., & Sun, J. (2015).** Faster R-CNN. *NeurIPS 28*, 91–99.  
arXiv: 1506.01497 | https://arxiv.org/abs/1506.01497  
→ Fundament zweistufiger Echtzeit-Objekterkennung in CCTV.

---

**Redmon, J., Divvala, S., Girshick, R., & Farhadi, A. (2016).** You Only Look Once: Unified, real-time object detection. *CVPR 2016*.  
arXiv: 1506.02640  
→ **YOLO**; dominierende Architektur in Überwachungskameras.

---

**Schmidhuber, J. (2015).** Deep learning in neural networks: An overview. *Neural Networks, 61*, 85–117.  
DOI: 10.1016/j.neunet.2014.09.003  
→ Autoritative Übersicht zur DL-Historie.

---

**Wang, M., & Deng, W. (2021).** Deep face recognition: A survey. *Neurocomputing, 429*, 215–244.  
DOI: 10.1016/j.neucom.2020.10.081  
→ Umfassender Überblick zur Kerntechnologie biometrischer Überwachung (auch Kap. 4).

---

## Kapitel 2 — KI-Monitoring in digitalen Informationsumgebungen

### 2.1 Plattformökonomie und Plattform-Governance

**Srnicek, N. (2017).** *Platform capitalism*. Polity Press. ISBN 978-1-5095-0487-9.  
→ **Referenzwerk**; Daten als Rohstoff, Typologisierung von Plattformen (auch Kap. 3 & 4).

---

**Van Dijck, J., Poell, T., & De Waal, M. (2018).** *The platform society: Public values in a connective world*. Oxford University Press.  
DOI: 10.1093/oso/9780190889760.001.0001 | ISBN 978-0-19-088976-0  
→ Plattform-Mechanismen (Datafication, Commodification, Selection) vs. öffentliche Werte.

---

**Parker, G. G., Van Alstyne, M. W., & Choudary, S. P. (2016).** *Platform revolution*. W. W. Norton. ISBN 978-0-393-24913-2.  
→ Zweiseitige Märkte und Netzwerkeffekte.

---

**Cusumano, M. A., Gawer, A., & Yoffie, D. B. (2019).** *The business of platforms*. HarperBusiness. ISBN 978-0-06-289632-2.  
→ Innovations- vs. Transaktionsplattformen, Governance, Regulierung (auch Kap. 4).

---

**Gawer, A. (2014).** Bridging differing perspectives on technological platforms: Toward an integrative framework. *Research Policy, 43*(7), 1239–1249.  
DOI: 10.1016/j.respol.2014.03.006 (Open Access)  
→ Integration ökonomischer und ingenieurstechnischer Plattform-Perspektive (Core + Periphery).

---

**Gawer, A. (2021).** Digital platforms and ecosystems. *Innovation: Organization & Management, 24*(1), 110–124.  
DOI: 10.1080/14479338.2021.1965888  
→ Aktuelles Update zur Ökosystem-Logik.

---

**Plantin, J.-C., Lagoze, C., Edwards, P. N., & Sandvig, C. (2018).** Infrastructure studies meet platform studies in the age of Google and Facebook. *New Media & Society, 20*(1), 293–310.  
DOI: 10.1177/1461444816661553  
→ **Plattformen als hybride Infrastruktur**; zentral für den infrastrukturellen Charakter von KI-Monitoring.

---

**Helmond, A. (2015).** The platformization of the web. *Social Media + Society, 1*(2).  
DOI: 10.1177/2056305115603080 (Open Access)  
→ Begriff „Platformization"; technisch-architektonische Analyse der Datenflüsse.

---

**Rahman, K. S., & Thelen, K. (2019).** The rise of the platform business model and the transformation of twenty-first-century capitalism. *Politics & Society, 47*(2), 177–204.  
DOI: 10.1177/0032329219838932  
→ Politökonomische Analyse von Plattform-Macht (auch Kap. 3).

---

**Poell, T., Nieborg, D., & Van Dijck, J. (2019).** Platformisation. *Internet Policy Review, 8*(4).  
DOI: 10.14763/2019.4.1425 (Open Access)  
→ Operationalisierbare Definition; Brücke zwischen IS- und kritischer Plattformforschung.

---

### 2.2 Recommender Systems und Personalisierung

**Ricci, F., Rokach, L., & Shapira, B. (Eds.) (2022).** *Recommender systems handbook* (3rd ed.). Springer.  
DOI: 10.1007/978-1-0716-2197-4  
→ **Autoritatives Handbuch** zu Collaborative Filtering, Content-Based, Deep Learning-Methoden und Wirkungsfragen.

---

**Aggarwal, C. C. (2016).** *Recommender systems: The textbook*. Springer.  
DOI: 10.1007/978-3-319-29659-3 | ISBN 978-3-319-29657-9  
Open PDF: http://charuaggarwal.net/Recommender-Systems.pdf  
→ Standardlehrbuch der Algorithmen.

---

**Covington, P., Adams, J., & Sargin, E. (2016).** Deep neural networks for YouTube recommendations. *RecSys '16*, 191–198.  
DOI: 10.1145/2959100.2959190  
→ **Primärquelle aus Google-Engineering**; zweistufige DL-Architektur im Produktivbetrieb.

---

**Beer, D. (2017).** The social power of algorithms. *Information, Communication & Society, 20*(1), 1–13.  
DOI: 10.1080/1369118X.2016.1216147  
→ Theoretische Konzeptualisierung algorithmischer Macht (auch Kap. 1 & 4).

---

### 2.3 Scoring- und Reputationssysteme

**Citron, D. K., & Pasquale, F. (2014).** The scored society: Due process for automated predictions. *Washington Law Review, 89*(1), 1–33.  
Open Access: https://digitalcommons.law.uw.edu/wlr/vol89/iss1/2/  
→ **Fundamentale Analyse** algorithmischer Scoring-Systeme und ihrer Opazität (auch Kap. 4).

---

**Fourcade, M., & Healy, K. (2013).** Classification situations: Life-chances in the neoliberal era. *Accounting, Organizations and Society, 38*(8), 559–572.  
DOI: 10.1016/j.aos.2013.11.002  
→ Soziologische Theoriebildung zu aktuarischer Klassifikation (auch Kap. 3).  
*Aktualisierung als Monografie:* **Fourcade, M., & Healy, K. (2024).** *The Ordinal Society*. Harvard UP. ISBN 978-0-674-29609-3.

---

**Rona-Tas, Á. (2020).** Predicting the future: Art and algorithms. *Socio-Economic Review, 18*(3), 893–911.  
DOI: 10.1093/ser/mwaa040  
→ Vergleich algorithmischer vs. menschlicher Prognosen; Self-fulfilling Prophecy als Risiko.

---

**Esposito, E., & Stark, D. (2019).** What's observed in a rating? *Theory, Culture & Society, 36*(4), 3–26.  
DOI: 10.1177/0263276419826276  
→ Luhmannianisches Reframing als „Beobachtung zweiter Ordnung".

---

**Kostka, G. (2019).** China's social credit systems and public opinion. *New Media & Society, 21*(7), 1565–1593.  
DOI: 10.1177/1461444819826402  
→ Peer-reviewed empirische Studie zur öffentlichen Akzeptanz (ergänzt Creemers).

---

### 2.4 Technische Survey-Papiere

**Stark, L. (2019).** Facial recognition is the plutonium of AI. *XRDS: Crossroads, 25*(3), 50–55.  
DOI: 10.1145/3313129  
→ **Einflussreiches Positionspapier** zur sozialen Toxizität biometrischer Erkennung (auch Kap. 4).

---

**Medhat, W., Hassan, A., & Korashy, H. (2014).** Sentiment analysis algorithms and applications: A survey. *Ain Shams Engineering Journal, 5*(4), 1093–1113.  
DOI: 10.1016/j.asej.2014.04.011  
→ Hochzitierter Survey zum Opinion Mining.

---

**Fortuna, P., & Nunes, S. (2018).** A survey on automatic detection of hate speech in text. *ACM Computing Surveys, 51*(4), Art. 85.  
DOI: 10.1145/3232676  
→ Schlüsselübersicht zur automatisierten Content-Moderation.

---

**Duong, H.-T., Le, V.-T., & Hoang, V. T. (2023).** Deep learning-based anomaly detection in video surveillance: A survey. *Sensors, 23*(11), 5024.  
DOI: 10.3390/s23115024 (Open Access)  
→ Aktuelle Übersicht zur Anomalieerkennung in CCTV.

---

## Kapitel 3 — Sozioökonomische Implikationen

### 3.1 Verhaltensbeeinflussung, Nudging, Choice Architecture

**Thaler, R. H., & Sunstein, C. R. (2021).** *Nudge: The final edition*. Yale University Press. ISBN 978-0-300-26228-0.  
→ Aktualisierte Auflage mit Digital-Kapitel und „Sludge".

---

**Weinmann, M., Schneider, C., & Vom Brocke, J. (2016).** Digital nudging. *Business & Information Systems Engineering, 58*(6), 433–436.  
DOI: 10.1007/s12599-016-0453-1  
→ **Seminales Papier** zur Einführung des Begriffs „Digital Nudging" in die IS-Forschung.

---

**Schneider, C., Weinmann, M., & Vom Brocke, J. (2018).** Digital nudging: Guiding online user choices through interface design. *Communications of the ACM, 61*(7), 67–73.  
DOI: 10.1145/3213765  
→ Praktische Taxonomie (Anchoring, Defaults, Decoy).

---

**Jesse, M., & Jannach, D. (2021).** Digital nudging with recommender systems: Survey and future directions. *Computers in Human Behavior Reports, 3*, 100052.  
DOI: 10.1016/j.chbr.2020.100052 (Open Access) | https://arxiv.org/abs/2011.03413  
→ **Brückenpapier**: Recommender Systems = Digital Nudges. Direkte Verbindung zur Forschungsfrage.

---

**Susser, D., Roessler, B., & Nissenbaum, H. (2019a).** Online manipulation: Hidden influences in a digital world. *Georgetown Law Technology Review, 4*(1), 1–45.  
SSRN: 3306006  
→ Konzeptionelle Abgrenzung von Manipulation, Persuasion und Nudging.

---

**Lanzing, M. (2019).** „Strongly recommended": Revisiting decisional privacy to judge hypernudging in self-tracking technologies. *Philosophy & Technology, 32*(3), 549–568.  
DOI: 10.1007/s13347-018-0316-4  
→ **Direktes Komplement zu Yeungs Hypernudge-Konzept**; fokussiert Self-Tracking.

---

**Gigerenzer, G. (2021).** *Klick: Wie wir in einer digitalen Welt die Kontrolle behalten*. C. Bertelsmann. ISBN 978-3-570-10445-3.  
→ **Deutschsprachige Schlüsselquelle** zur Verhaltensbeeinflussung durch algorithmische Systeme.

---

**Fogg, B. J. (2003).** *Persuasive technology: Using computers to change what we think and do*. Morgan Kaufmann. ISBN 978-1-55860-643-2.  
→ Fundamentaltext „Captology"; historischer Anker zur persuasiven Systemgestaltung.

---

### 3.2 Filter Bubbles, Echo Chambers, Informationsumgebung

**Pariser, E. (2011).** *The filter bubble: What the Internet is hiding from you*. Penguin Press. ISBN 978-1-594-20300-8.  
→ Originalwerk des Begriffs; kanonisch zu zitieren.

---

**Sunstein, C. R. (2017).** *#Republic: Divided democracy in the age of social media*. Princeton University Press.  
DOI: 10.1515/9781400884711 | ISBN 978-0-691-17551-5  
→ Group Polarization; wissenschaftliche Aktualisierung von *Republic.com*.

---

**Bakshy, E., Messing, S., & Adamic, L. A. (2015).** Exposure to ideologically diverse news and opinion on Facebook. *Science, 348*(6239), 1130–1132.  
DOI: 10.1126/science.aaa1160  
→ **Empirische Großstudie** (10,1 Mio. Nutzer); Methodik kritisch reflektieren (Insider-Studie).

---

**Flaxman, S., Goel, S., & Rao, J. M. (2016).** Filter bubbles, echo chambers, and online news consumption. *Public Opinion Quarterly, 80*(S1), 298–320.  
DOI: 10.1093/poq/nfw006  
→ Nuancierte empirische Befunde; widerlegt vereinfachende Filter-Bubble-Narrative.

---

**Cinelli, M. et al. (2021).** The echo chamber effect on social media. *PNAS, 118*(9), e2023301118.  
DOI: 10.1073/pnas.2023301118 (Open Access)  
→ Großvergleich Facebook/Twitter/Reddit/Gab; algorithmische Plattformen verstärken Echokammern.

---

**Möller, J., Trilling, D., Helberger, N., & Van Es, B. (2018).** Do not blame it on the algorithm. *Information, Communication & Society, 21*(7), 959–977.  
DOI: 10.1080/1369118X.2018.1444076  
→ Recommender-Design entscheidet über Diversitätseffekte.

---

### 3.3 Überwachung — Erweiterte Perspektiven

**Solove, D. J. (2008).** *Understanding privacy*. Harvard University Press. ISBN 978-0-674-02772-5.  
→ **Kanonische pluralistische Taxonomie** von Privatheit (16 Sub-Typen).

---

**Nissenbaum, H. (2010).** *Privacy in context*. Stanford University Press. ISBN 978-0-8047-5237-4.  
→ **Contextual Integrity** als Theorie kontextspezifischer Normverletzung (auch Kap. 4).

---

**Bauman, Z., & Lyon, D. (2013).** *Liquid surveillance: A conversation*. Polity. ISBN 978-0-7456-6283-1.  
→ Erweiterung Lyons um „liquid modernity".

---

**Andrejevic, M. (2020).** *Automated media*. Routledge. DOI: 10.4324/9780429242595.  
→ Kaskadenlogik der Automation (Erfassung → Verarbeitung → Entscheidung).

---

**Eubanks, V. (2018).** *Automating inequality*. St. Martin's Press. ISBN 978-1-250-07431-7.  
→ Drei Fallstudien (Indiana Welfare, LA Homeless, Allegheny Risk Model).

---

**Brayne, S. (2020).** *Predict and surveil: Data, discretion, and the future of policing*. Oxford University Press.  
DOI: 10.1093/oso/9780190684099.001.0001 | ISBN 978-0-19-068409-9  
→ Ethnografie zu LAPD Big-Data-Policing.

---

**Couldry, N., & Mejias, U. A. (2019).** *The costs of connection*. Stanford University Press. ISBN 978-1-5036-0366-0.  
→ **Daten-Kolonialismus-These**; strukturelle Alternative zu Zuboff (auch Kap. 4).

---

**Fuchs, C. (2021).** *Social media: A critical introduction* (3rd ed.). SAGE. ISBN 978-1-5297-5274-8.  
→ Marxistische politische Ökonomie sozialer Medien.

---

### 3.4 Digitale Gesellschaft (Deutschsprachig)

**Stalder, F. (2016).** *Kultur der Digitalität*. Suhrkamp. ISBN 978-3-518-12679-0.  
→ **Konzeptioneller Rahmen**: Referentialität, Gemeinschaftlichkeit, **Algorithmizität** als Strukturformen.

---

**Nassehi, A. (2019).** *Muster: Theorie der digitalen Gesellschaft*. C.H. Beck. ISBN 978-3-406-74024-4.  
→ Digitalisierung als Antwort auf das Problem gesellschaftlicher Mustererkennung.

---

**Reckwitz, A. (2017).** *Die Gesellschaft der Singularitäten*. Suhrkamp. ISBN 978-3-518-58706-5.  
→ Singularisierung als Rahmen für Personalisierung/Profilbildung.

---

**Staab, P. (2019).** *Digitaler Kapitalismus: Markt und Herrschaft in der Ökonomie der Unknappheit*. Suhrkamp. ISBN 978-3-518-07515-9.  
→ Ökonomischer Rahmen für Monitoring-Geschäftsmodelle.

---

**Mau, S. (2017).** *Das metrische Wir: Über die Quantifizierung des Sozialen*. Suhrkamp. ISBN 978-3-518-07292-9.  
→ **Brückenwerk**: Verhaltensbeeinflussung via Rankings, Scores, Likes.

---

**Kucklick, C. (2014).** *Die granulare Gesellschaft*. Ullstein/Econ. ISBN 978-3-430-20167-3.  
→ Drei-Revolutionen-These; „Ausdeutung" statt Ausbeutung.

---

**Schaar, P. (2014).** *Überwachung total*. Aufbau. ISBN 978-3-351-03295-1.  
→ Systemische Perspektive auf Überwachungsarchitekturen (ehem. Bundesdatenschutzbeauftragter).

---

**Kurz, C., & Rieger, F. (2011).** *Die Datenfresser*. S. Fischer. ISBN 978-3-10-048518-2.  
→ Technische Seite der Überwachung; einflussreich im deutschen Diskurs.

---

**Hofstetter, Y. (2016).** *Das Ende der Demokratie: Wie die künstliche Intelligenz die Politik übernimmt*. C. Bertelsmann. ISBN 978-3-570-10306-7.  
→ Praktikerperspektive zu Big Data, Mustererkennung und Nudging *(meinungsstark — entsprechend einordnen)*.

---

## Kapitel 4 — Kritische Analyse: Ethik, Normativität, Recht

### 4.1 KI-Ethik und Fairness

**Mittelstadt, B. D., Allo, P., Taddeo, M., Wachter, S., & Floridi, L. (2016).** The ethics of algorithms: Mapping the debate. *Big Data & Society, 3*(2), 1–21.  
DOI: 10.1177/2053951716679679  
→ **Standard-Mapping** algorithmischer Ethik mit sechs Konfliktdimensionen.

---

**Mittelstadt, B. (2019).** Principles alone cannot guarantee ethical AI. *Nature Machine Intelligence, 1*(11), 501–507.  
DOI: 10.1038/s42256-019-0114-4  
→ Kritik des Prinzipien-Ansatzes; zentrales Gegengewicht.

---

**Jobin, A., Ienca, M., & Vayena, E. (2019).** The global landscape of AI ethics guidelines. *Nature Machine Intelligence, 1*(9), 389–399.  
DOI: 10.1038/s42256-019-0088-2  
→ Systematisches Review von 84 Leitlinien; fünf Konvergenzprinzipien.

---

**Floridi, L. et al. (2018).** AI4People — An ethical framework for a good AI society. *Minds and Machines, 28*(4), 689–707.  
DOI: 10.1007/s11023-018-9482-5  
→ **Einflussreichster Synthese-Rahmen**; intellektuelle Basis des EU-Trustworthy-AI-Ansatzes.

---

**High-Level Expert Group on AI (2019).** *Ethics guidelines for trustworthy AI*. European Commission.  
https://digital-strategy.ec.europa.eu/en/library/ethics-guidelines-trustworthy-ai  
→ **Offizieller EU-Rahmen** mit sieben Schlüsselanforderungen; unverzichtbar für europäischen Regulierungskontext.

---

**Selbst, A. D., Boyd, D., Friedler, S. A., Venkatasubramanian, S., & Vertesi, J. (2019).** Fairness and abstraction in sociotechnical systems. *FAT* '19*, 59–68.  
DOI: 10.1145/3287560.3287598  
→ **Fünf „Fallen" rein technischer Fairness-Ansätze**; zentrale soziotechnische Korrektur.

---

**Crawford, K. (2021).** *Atlas of AI*. Yale University Press. ISBN 978-0-300-20957-0.  
→ KI als extraktive Industrie (Mineralien, Arbeit, Daten).

---

**Benjamin, R. (2019).** *Race after technology: Abolitionist tools for the new Jim Code*. Polity. ISBN 978-1-5095-2640-6.  
→ Konzept „New Jim Code"; codierte Diskriminierung.

---

**Noble, S. U. (2018).** *Algorithms of oppression*. NYU Press. ISBN 978-1-4798-3724-3.  
→ Empirische Demonstration diskriminierender Effekte in Suchmaschinen.

---

**D'Ignazio, C., & Klein, L. F. (2020).** *Data feminism*. MIT Press. ISBN 978-0-262-04400-4.  
Open Access: https://data-feminism.mitpress.mit.edu/  
→ Sieben Prinzipien intersektionaler Datenwissenschaft.

---

**Birhane, A. (2021).** Algorithmic injustice: A relational ethics approach. *Patterns, 2*(2), 100205.  
DOI: 10.1016/j.patter.2021.100205 (Open Access)  
→ Relationale statt prinzipien-basierte Ethik.

---

### 4.2 Recht und Regulierung (Deutschsprachig)

**Datenethikkommission der Bundesregierung (2019).** *Gutachten der Datenethikkommission*. BMI/BMJV.  
https://www.bmi.bund.de/SharedDocs/downloads/DE/publikationen/themen/it-digitalpolitik/gutachten-datenethikkommission.html  
→ **240 Seiten, 75 Handlungsempfehlungen**; maßgebliches Referenzdokument.

---

**Martini, M. (2019).** *Blackbox Algorithmus – Grundfragen einer Regulierung Künstlicher Intelligenz*. Springer.  
DOI: 10.1007/978-3-662-59010-2 | ISBN 978-3-662-59009-6  
→ **Rechtswissenschaftliche Standardarbeit**; normatives Gerüst.

---

**Hoffmann-Riem, W. (2022).** *Recht im Sog der digitalen Transformation*. Mohr Siebeck. ISBN 978-3-16-161199-5.  
→ Verfassungsrechtliche Perspektive auf private Normsetzung und IT-Vermachtung. Open Access CC BY-NC-ND.

---

**Chiusi, F., Fischer, S., Kayser-Bril, N., & Spielkamp, M. (Hg.) (2020).** *Automating Society Report 2020 – Deutsche Ausgabe*. AlgorithmWatch & Bertelsmann Stiftung.  
https://automatingsociety.algorithmwatch.org  
→ Über 100 ADM-Fälle aus 16 europäischen Ländern. Open Access.

---

**Plattform Lernende Systeme / acatech (2020).** *Ethik-Briefing: Leitfaden für eine verantwortungsvolle Entwicklung und Anwendung von KI-Systemen*.  
https://www.plattform-lernende-systeme.de/publikationen.html  
→ Whitepaper der nationalen KI-Plattform.

---

## Supplementärquellen — Podcasts, Vorlesungen, Dokumentationen

> ⓘ **Hinweis FOM-Richtlinien**: Diese Quellen sind nach den FOM-Richtlinien zulässig, da das Medium für den Quellenwert irrelevant ist. Flüchtige Quellen müssen gesichert und als Quellsammlung der Arbeit beigefügt werden. Alle Quellen mit Abrufdatum: **11.05.2026**.

### Dokumentationen

**Orlowski, J. (Regie). (2020).** *The Social Dilemma* [Docudrama, 94 Min.]. Exposure Labs / Netflix.  
https://www.netflix.com/title/81254224  
→ Meistzitierte populäre Dokumentation zu algorithmischer Verhaltensbeeinflussung; Tristan Harris u.a. (Kap. 3 & 4). *Hinweis: Mischform mit dramatisierten Reenactments.*

---

**Kantayya, S. (Regie). (2020).** *Coded Bias* [Doku, 90 Min.]. PBS Independent Lens / Netflix.  
https://www.pbs.org/independentlens/documentaries/coded-bias/  
→ Joy Buolamwinis MIT-Forschung zu Bias in Gesichtserkennung (Kap. 4).

---

**Hessen Schei, T. (Regie). (2019).** *iHuman* [Doku, 99 Min.]. UpNorth Film.  
https://upnorthfilm.no/film/ihuman  
→ Globale KI-Industrie, Sozialkredit, Predictive Policing (Kap. 2–4).

---

**Heeder, M., & Hielscher, M. (Regie). (2017).** *Pre-Crime* [Doku, 88 Min.]. Kloos & Co. Medien.  
→ **Deutsche Produktion** zu Predictive Policing (PredPol, Chicago, London) (Kap. 2 & 4).

---

### Podcasts

**Center for Humane Technology (2019–lfd.).** *Your Undivided Attention* [Podcast]. Hosts: T. Harris, A. Raskin.  
https://www.humanetech.com/podcast  
→ Episoden mit Zuboff, Bengio, Buolamwini (Kap. 3 & 4).

---

**Deutschlandfunk (2023–lfd.).** *KI verstehen* [Podcast].  
https://podcasts.apple.com/de/podcast/ki-verstehen/id1697851853  
→ **Deutschsprachiger öffentlich-rechtlicher Podcast**; wöchentlich zu Überwachung, Predictive Analytics, biometrischer Identifikation (Kap. 2 & 3).

---

**Fridman, L. (Host). (2018, 9. Dezember).** Stuart Russell: Long-term future of AI (Nr. 9). *Lex Fridman Podcast*.  
https://lexfridman.com/stuart-russell/  
→ Ergänzt die Russell-2022-Quelle aus dem Exposé (Kap. 1 & 4).

---

### TED Talks & Vorlesungen

**Harris, T. (2017).** *How a handful of tech companies control billions of minds every day* [TED, 17 Min.].  
https://www.ted.com/talks/tristan_harris_how_a_handful_of_tech_companies_control_billions_of_minds_every_day  
→ Fundament zur Attention Economy (Kap. 3).

---

**Harari, Y. N. (2018).** *Why fascism is so tempting – and how your data could power it* [TED2018, 22 Min.].  
https://www.ted.com/talks/yuval_noah_harari_why_fascism_is_so_tempting_and_how_your_data_could_power_it  
→ Datengetriebener Autoritarismus (Kap. 3 & 4).

---

**Sanderson, G. (2017–lfd.).** *Neural networks* [YouTube-Playlist]. 3Blue1Brown.  
https://www.youtube.com/playlist?list=PLZZWrBYkx7Otcjr3eCLZDCgfpqnxMY29s  
→ Visualisierungsbasierte Erklärungen zu Feedforward, Backprop, Transformern (Kap. 1).

---

**Stanford University. (2025).** *CS231N: Deep Learning for Computer Vision – Spring 2025* [YouTube].  
https://cs231n.stanford.edu/  
→ Autoritative Vorlesungsreihe zu CNNs, Object Detection (Kap. 1 & 2).

---

## Empfohlene Kern-Lese-Cluster

| Cluster | Neue Quellen | Vorhandene Quellen (Exposé) | Zweck |
|---|---|---|---|
| **IS-Architektur** | Laudon/Laudon, Alter, Hevner, Vial, Ertel | — | IS-theoretische Basis für Kap. 1 |
| **Plattform-Monitoring** | Srnicek, Van Dijck et al., Plantin et al., Helmond, Gawer 2021 | Gillespie, Kitchin | Vollständige Plattform-Theorie für Kap. 2 |
| **Hypernudge-Brücke** | Jesse & Jannach, Weinmann et al., Susser et al., Lanzing | Yeung (2017) | Verbindet Recommender Systems mit Verhaltensbeeinflussung |
| **Kritisch-Deutsch** | Datenethikkommission, Martini, Hoffmann-Riem, AlgorithmWatch | Zurawski, Rothmann/Mayer | Deutsche Rechtsdogmatik + internationale Ethik-Debatte |

---

*Erstellt mit Claude (Anthropic) als Thesis-Assistent | FOM Frankfurt | Mai 2026*
