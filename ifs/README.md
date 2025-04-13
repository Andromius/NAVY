# IFS (Iterative Function System)

## Popis implementace

Tento program implementuje iterativní funkční systém (IFS) pro generování fraktálních struktur ve 3D prostoru.

### Hlavní komponenty

1. **Vizualizační funkce** (`visualize_points`)
   - Zobrazuje body v 3D prostoru pomocí knihovny matplotlib
   - Vytváří interaktivní 3D graf s popisky os X, Y, Z

2. **Transformační funkce** (`apply_transform`)
   - Aplikuje lineární transformaci na bod v prostoru
   - Využívá maticové násobení a translaci
   - Parametry:
     - `point`: Bod v prostoru (numpy array)
     - `transform`: Transformační matice
     - `translate`: Translační vektor

3. **IFS algoritmus** (`ifs`)
   - Generuje fraktální strukturu pomocí iterativních transformací
   - V každé iteraci:
     - Náhodně vybere jednu z definovaných transformací
     - Aplikuje ji na aktuální bod
     - Ukládá výsledné body
   - Parametry:
     - `point`: Počáteční bod
     - `iterations`: Počet iterací
     - `transforms`: Seznam dostupných transformací

### Použití

Program generuje dva různé fraktály pomocí předem definovaných sad transformací (MODELS[0] a MODELS[1]). 
Každý fraktál je vygenerován z počátečního bodu [0,0,0] pomocí 1500 iterací.

### Technické detaily
- Využívá knihovny:
  - NumPy pro maticové operace
  - Matplotlib pro 3D vizualizaci
  - Random pro náhodný výběr transformací