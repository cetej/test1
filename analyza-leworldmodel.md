# Analýza – LeWorldModel (LeWM): Stabilní end-to-end JEPA z pixelů

## 1. Základní údaje o práci

- **Název:** LeWorldModel: Stable End-to-End Joint-Embedding Predictive Architecture from Pixels
- **Autoři:** Lucas Maes (Mila & Université de Montréal), Quentin Le Lidec (NYU), Damien Scieur (Mila & Samsung SAIL), Yann LeCun (NYU), Randall Balestriero (Brown University)
- **Typ:** Preprint (výzkumný článek)
- **Kontakt:** lucas.maes@mila.quebec

## 2. Kontext a motivace

Joint Embedding Predictive Architectures (JEPA) jsou slibným rámcem pro učení světových modelů (world models) v kompaktních latentních prostorech. Dosavadní metody však trpí:

- **Křehkostí trénování** – snadno dochází ke kolapsu reprezentací
- **Komplexními ztrátovými funkcemi** s mnoha členy
- **Závislostí na hacích** jako exponenciální klouzavé průměry (EMA), stop-gradient, předtrénované enkodéry nebo pomocná supervize
- **Velkým počtem hyperparametrů** (typicky 6+)

## 3. Klíčový přínos LeWM

LeWM je **první JEPA, která trénuje stabilně end-to-end z raw pixelů** pouze se dvěma ztrátovými členy:

1. **Next-embedding prediction loss** – MSE (mean squared error) mezi predikovaným a skutečným dalším latentním stavem
2. **SIGReg regularizátor** – vynucuje Gaussovské rozložení latentních embeddingů

### Výhody oproti existujícím přístupům

| Vlastnost | LeWM | Ostatní JEPA |
|-----------|------|--------------|
| Počet laditelných hyperparametrů ztrátové funkce | **1** | 6+ |
| Potřeba stop-gradientu | Ne | Typicky ano |
| Potřeba EMA | Ne | Typicky ano |
| Potřeba předtrénovaného enkodéru | Ne | Často ano |
| End-to-end trénování z pixelů | Ano | Omezené |

## 4. Architektura (Training Pipeline)

1. **Enkodér** – mapuje pozorování (frames) $o_{1:T}$ do nízkorozměrných latentních reprezentací $z_{1:T}$
2. **Prediktor** – autoregresivně predikuje další latentní stav $\hat{z}_{t+1}$ z aktuálního stavu $z_t$ a akce $a_t$
3. **MSE loss** – mezi predikovaným $\hat{z}_{t+1}$ a skutečným $z_{t+1}$ (z enkodéru)
4. **SIGReg** – regularizace:
   - Latentní embeddingy se projektují na náhodné jednorozměrné směry
   - Na každou projekci se aplikuje test normality
   - Agregace statistik směřuje celé rozložení k izotropnímu Gaussiánu

## 5. SIGReg – mechanismus regularizace

SIGReg (Sliced Isotropic Gaussian Regularization) je klíčová inovace:

- Zabraňuje **triviálnímu kolapsu** (kdy by enkodér mapoval vše na konstantu)
- Zajišťuje **diverzitu features** v latentním prostoru
- Pracuje přes **náhodné jednorozměrné projekce** (sliced approach) – efektivní i ve vysokých dimenzích
- Optimalizuje normalitu podél každé projekce → celkové rozložení konverguje k izotropnímu Gaussiánu

## 6. Výkonnostní parametry

- **Velikost modelu:** 15M parametrů
- **Trénování:** Na jednom GPU během několika hodin
- **Rychlost plánování:** Až **48× rychlejší** než world modely založené na foundation modelech
- **Konkurenceschopnost:** Srovnatelná s state-of-the-art na rozmanitých 2D a 3D řídicích úlohách (control tasks)

## 7. Interpretovatelnost a fyzikální smysluplnost

Autoři ukazují, že latentní prostor LeWM kóduje **smysluplnou fyzikální strukturu**:

- **Probing fyzikálních veličin** – lineární sondy nad latentním prostorem dokáží predikovat fyzikální vlastnosti (pozice, rychlost apod.)
- **Surprise evaluation** – model spolehlivě detekuje **fyzikálně nepravděpodobné události** (např. objekt procházející zdí), což naznačuje porozumění základní fyzice prostředí

## 8. Silné stránky

- **Jednoduchost** – minimální počet hyperparametrů, žádné tréninkové triky
- **Stabilita** – end-to-end trénování bez kolapsu
- **Efektivita** – malý model, rychlé trénování na jednom GPU
- **Škálovatelnost** – jednoduchá architektura umožňuje snadné škálování
- **Interpretovatelnost** – latentní prostor má fyzikální význam

## 9. Potenciální omezení a otevřené otázky

- **Preprint** – dosud neprocházel plným peer-review procesem
- **Škálování na komplexnější prostředí** – 15M parametrů je relativně malý model; otázka, jak se přístup chová na složitějších úlohách (realistické 3D prostředí s bohatou fyzikou)
- **Generalizace** – jak dobře se naučené reprezentace přenášejí na nové, neviděné úlohy?
- **Dlouhodobé predikce** – autoregresivní predikce typicky akumuluje chybu; jak daleko do budoucnosti model spolehlivě plánuje?
- **Srovnání s model-free přístupy** – v některých benchmarcích mohou být model-free RL metody stále konkurenceschopnější

## 10. Zasazení do širšího kontextu

LeWM navazuje na vizi Yanna LeCuna o **autonomních strojích řízených světovými modely** v latentním prostoru (JEPA framework, prezentovaný v "A Path Towards Autonomous Machine Intelligence", 2022). Klíčový posun je v tom, že LeWM ukazuje, že JEPA lze trénovat **jednoduše a stabilně**, bez složité inženýrské mašinérie, která dosud bránila širšímu přijetí tohoto přístupu.

## 11. Shrnutí

LeWorldModel představuje významný krok k **jednoduchým, stabilním a efektivním světovým modelům** v latentním prostoru. Kombinace MSE predikční ztráty a SIGReg regularizace eliminuje potřebu složitých trénovacích triků a umožňuje end-to-end učení z pixelů s minimem hyperparametrů. Model je malý, rychlý a přitom konkurenceschopný – což otevírá cestu k praktickému nasazení JEPA světových modelů v robotice a plánování.
