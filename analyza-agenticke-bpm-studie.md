# Analýza studie: Agentic Business Process Management – A Research Manifesto

**arXiv ID:** 2603.18916v2
**Datum publikace:** 19.–20. března 2026
**Zdroj:** [https://arxiv.org/abs/2603.18916](https://arxiv.org/abs/2603.18916)

---

## 1. Základní informace

### Autoři a afiliace

| Autor | Afiliace |
|-------|----------|
| Diego Calvanese | Free University of Bozen-Bolzano, Itálie |
| Angelo Casciani | University of Oxford, Velká Británie |
| Giuseppe De Giacomo | University of Oxford, Velká Británie |
| Marlon Dumas | University of Tartu, Estonsko |
| Fabiana Fournier | IBM Research, Haifa, Izrael |
| Timotheus Kampik | Umeå University, Švédsko |
| Emanuele La Malfa | University of Oxford, Velká Británie |
| Lior Limonad | IBM Research, Izrael |
| Andrea Marrella | Sapienza Università di Roma, Itálie |
| Andreas Metzger | paluno (Ruhr Institute for Software Technology), University of Duisburg-Essen, Německo |
| Marco Montali | Free University of Bozen-Bolzano, Itálie |
| Daniel Amyot | University of Ottawa, Kanada |
| Peter Fettke | DFKI / Saarland University, Německo |
| Artem Polyvyanyy | University of Melbourne, Austrálie |
| Stefanie Rinderle-Ma | TU Munich, Německo |
| Sebastian Sardiña | RMIT University, Melbourne, Austrálie |
| Niek Tax | Meta, Londýn, Velká Británie |
| Barbara Weber | University of St. Gallen, Švýcarsko |

### Původ studie

Manifest vznikl na základě diskuzí během **Dagstuhl Seminar #25192 (AUTOBIZ)**, kde autoři s expertízou v BPM, process mining, softwarovém inženýrství, AI a multi-agentních systémech (MAS) identifikovali klíčové schopnosti a výzkumné výzvy APM.

---

## 2. Abstrakt a hlavní teze

Studie představuje **manifest**, který formuluje koncepční základy **Agentic Business Process Management (APM)** — rozšíření tradičního Business Process Management (BPM) pro řízení autonomních agentů vykonávajících procesy v organizacích.

Z manažerského pohledu APM představuje **paradigmatický posun** od tradičního procesního pohledu směrem k:

- **Procesnímu povědomí (process awareness)** — agenti jsou si vědomi kontextu a omezení procesu
- **Agentově orientované abstrakci** — softwaroví a lidští agenti vystupují jako primární funkční entity, které vnímají, uvažují a jednají v rámci explicitních **procesních rámců (process frames)**

Jedná se o posun od tradiční **automatizačně orientované BPM** k systémům, kde je **autonomie omezena, sladěna a zprovozněna prostřednictvím procesního povědomí**.

---

## 3. Klíčový koncept: Framed Agency (rámcová agentura)

Jádrem APM paradigmatu je pojem **framed agency** — agenti mají autonomii, ale ta je ohraničena procesním rámcem.

### Rozdíl mezi automatizací a autonomií

| Aspekt | Automatizace (tradiční BPM) | Autonomie (APM) |
|--------|---------------------------|-----------------|
| Provádění | Přesně podle předem definovaných pravidel | Agenti se rozhodují kontextově |
| Flexibilita | Fixní pravidla | Rozhodování v rámci procesních omezení |
| Adaptace | Žádná | Agenti se mohou přizpůsobit a vyvíjet |

### Příklad z praxe

APM systém pro **onboarding nových dodavatelů** v rámci procurement procesu: Systém zahrnuje agenta kupujícího a několik agentů dodavatelů (někteří lidští, někteří AI). Oba typy agentů disponují procesním povědomím — průběžně slaďují své individuální cíle a jednají ve shodě pro dosažení organizačních cílů procurement procesu.

---

## 4. Čtyři klíčové schopnosti APM agentů

Studie identifikuje čtyři klíčové schopnosti, které APM agenti musí podporovat (záměrně seřazené):

### 4.1 Framed Autonomy (rámcová autonomie)

- Zajišťuje, že agenti jsou **procesně uvědomělí** a jejich akce jsou **ohraničeny guardrails**
- Agenti mohou vnímat, uvažovat a volit, jak jednat v rámci procesního rámce
- Praktické výzvy sahají od základních otázek o tom, co je agent v business procesech, až po specifikaci a operacionalizaci

### 4.2 Explainability (vysvětlitelnost)

- Schopnost **artikulovat důvody rozhodnutí**
- Procesní stakeholdeři mohou obdržet specifická vysvětlení fungování socio-technického systému
- Zahrnuje nejen technickou trasovatelnost, ale i vývoj **"sociálních kontraktů"** mezi lidskými a digitálními agenty
- Definuje hranice delegace a přesné podmínky, za kterých je lidská intervence právně a operačně povinná

### 4.3 Conversational Actionability (konverzační akceschopnost)

- Umožňuje agentům **vyjednávat a koordinovat** s ostatními agenty
- Umožňuje procesním stakeholderům **spouštět akce** (v design-time i run-time) pro změnu chování systému
- Agent může jednat na základě konverzace s prostředím i s dalšími agenty

### 4.4 Self-Modification (sebemodifikace)

- Schopnost agenta **adaptovat se a vyvíjet v čase**
- Agenti se sebemodifikují pro lepší dosažení individuálních cílů
- Při správném rámcování přispívají k dosahování **kolektivních procesních cílů**

---

## 5. Architektura a abstrakce APM systémů

Studie zavádí **základní abstrakce a architektonické elementy** potřebné pro realizaci APM systémů:

- **Process Frame (procesní rámec)** — sada pravidel, omezení a regulací, která se může v čase vyvíjet. Na jednom extrému agent dostává velmi specifický cíl s detailní sadou striktních omezení (ekvivalent imperativního procesu), na druhém jsou dány pouze cíle a agent má úplnou volnost.
- **APM systém** — agentní socio-technický systém, společně realizovaný kolekcí agentů, z nichž někteří jsou alespoň částečně procesně uvědomělí.
- **Agent-oriented abstraction** — agenti (lidští i softwaroví) jako primární funkční entity
- **Process awareness** — zaručení, že vnitřní fungování agentů je v souladu s organizačními procesy a dodržuje operační omezení, regulace a cíle
- **Guardrails** — mechanismy omezující autonomii agentů

### Architektura A-BPMS (5 vrstev)

Doplňkový článek (arXiv:2601.18833) navrhuje podrobnou architekturu **Agentic BPMS** s pěti podsystémy:

1. **Datová vrstva (Data Layer)** — integruje strukturovaná i nestrukturovaná data o podnikových operacích, včetně eventových logů, repozitářů procesních modelů a záznamů minulých rozhodnutí
2. **Vrstva procesní inteligence (Process Intelligence Layer)** — analytická vrstva pro dolování a monitoring procesů
3. **Vrstva akcí (Action Layer)** — provádění akcí v prostředí
4. **Orchestrační vrstva (Orchestration Layer)** — koordinace více agentů a procesů
5. **Konverzační vrstva (Conversational Layer)** — interakce mezi uživateli a A-BPMS prostřednictvím konverzačních agentů poháněných generativní AI (např. LLM)

---

## 6. Souvislost s existujícím výzkumem

### Normativní multi-agentní systémy (MAS)

Řízení agentů (agent governance) je zavedená výzkumná linie, pocházející primárně z AI podoblasti **normativních MAS**, která se zaměřuje na regulaci chování autonomních agentů prostřednictvím norem — závazků, povolení a zákazů — pro zajištění sociálního řádu a shody.

### Agentově orientované metody

Studie navrhuje využití existujících metod analýzy a návrhu agentových systémů jako základ pro nové inženýrské metody APM:
- **AAII** (Australian AI Institute methodology)
- **Gaia**
- **Tropos**
- **Prometheus**

---

## 7. Výzkumné výzvy

### Specifické výzvy pro jednotlivé schopnosti

1. **Definice agenta v business procesech** — před rozšířením LLM pojem agenta nehrál větší roli v inženýringu podnikových informačních systémů; je třeba definovat robustnější a intuitivně pochopitelný pojem agenta pro BPM praktiky
2. **Specifikace a operacionalizace** rámcové autonomie
3. **Sociální kontrakty** mezi lidskými a digitálními agenty — definice hranic delegace
4. **Právní a operační podmínky** lidské intervence
5. **Inženýrské metody** pro návrh APM systémů
6. **Překlenutí komunit** BPM, AI a MAS
7. **Zajištění, že sebemodifikace neporušuje procesní rámce** — mechanismy pro řízené učení a adaptaci

### Průřezové výzvy

- **Bezpečnostní rámce** — řízení kompromisu mezi autonomií agentů a informační bezpečností; zajištění, že agenti mohou vyjednávat a adaptovat se, aniž by byla ohrožena integrita a důvěrnost
- **Hodnoticí rámce** — tradiční BPM charakteristiky (čas, náklady, kvalita) nestačí k souhrnné charakterizaci kvalit agentů; chybí holistické hodnoticí rámce
- **Přemostění disciplín** — manifest slouží jako roadmapa pro sblížení komunit BPM, AI a MAS

---

## 8. Přínos a závěry

### Hlavní přínosy studie

1. **Koncepční základy** — první systematická formulace APM jako rozšíření BPM
2. **Paradigmatický posun** — od automatizace k řízené autonomii
3. **Čtyři klíčové schopnosti** — jasně definovaný rámec pro APM agenty
4. **Roadmapa** — manifest slouží jako vodítko pro překlenutí komunit BPM, AI a MAS a pro praktický vývoj APM systémů

### Cílový journal

Studie je připravena pro publikaci v **Information Systems**.

---

## 9. Související práce

| Studie | arXiv ID | Zaměření |
|--------|----------|----------|
| AI-Augmented BPM Systems: A Research Manifesto (předchůdce) | 2201.12855 | Definoval ABPMS jako novou třídu procesně vědomých IS; postuloval 5 schopností: autonomie, konverzační akcionovatelnost, adaptivita, sebezlepšování, vysvětlitelnost |
| Agentic BPM Systems | 2601.18833 | Architektonická vize A-BPMS s integrací autonomie, reasoning a learning |
| Agentic BPM: Practitioner Perspectives | 2504.03693 | Kvalitativní studie s 22 BPM praktiky — očekávají zvýšení efektivity a lepší compliance, ale varují před riziky zaujatosti, nadměrné závislosti a nejasného rozhodování |
| PMAx: Agentic Framework for AI-Driven Process Mining | 2603.15351 | Nástroj pro agentický process mining |

---

## 10. Shrnutí

Studie "Agentic Business Process Management: A Research Manifesto" je **průlomový manifest** 18 předních akademiků a průmyslových expertů, který definuje nové paradigma řízení podnikových procesů prostřednictvím autonomních agentů. Klíčovým konceptem je **rámcová agentura (framed agency)** — agenti mají autonomii, ale jsou omezeni procesním rámcem. Manifest identifikuje čtyři klíčové schopnosti (rámcová autonomie, vysvětlitelnost, konverzační akceschopnost, sebemodifikace) a slouží jako **roadmapa pro budoucí výzkum** na průsečíku BPM, umělé inteligence a multi-agentních systémů.

---

*Analýza vytvořena: 25. března 2026*
*Zdroj: [arXiv:2603.18916](https://arxiv.org/abs/2603.18916)*
