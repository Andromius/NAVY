# Vizualizátor fraktálů - Mandelbrotova a Juliova množina

## Co program dělá?

Tento program vytváří interaktivní vizualizaci dvou známých fraktálů:
- Mandelbrotovy množiny
- Juliovy množiny

### Matematický základ

#### Společná rovnice
Obě množiny jsou založeny na iteraci komplexní rovnice:
```
z_{n+1} = z_n² + c
```

#### Rozdíl mezi množinami
1. **Mandelbrotova množina:**
   - Začíná s `z₀ = 0`
   - Pro každý bod `c` v komplexní rovině testuje, zda sekvence zůstane omezená
   - Bod `c` je v množině, pokud |z_n| ≤ 2 pro všechna n

2. **Juliova množina:**
   - Parametr `c` je fixní pro celou množinu
   - Pro každý počáteční bod `z₀` v komplexní rovině testuje konvergenci
   - Bod `z₀` je v množině, pokud sekvence zůstane omezená

### Hlavní funkce
1. **Zobrazení fraktálů**
   - Barevné vykreslení fraktálů
   - Možnost přepínání mezi množinami
   - Interaktivní přiblížení kliknutím myši

2. **Ovládací prvky**
   - Nastavení středu zobrazení (Re, Im)
   - Úroveň přiblížení
   - Počet iterací (ovlivňuje detail fraktálu)
   - Pro Juliovu množinu: nastavení parametru c

### Jak to funguje?
- Program počítá pro každý bod, zda sekvence:
  - Zůstane v oblasti |z| ≤ 2 (bod patří do množiny)
  - "Uteče" do nekonečna (bod nepatří do množiny)
- Barva bodu závisí na rychlosti úniku
- Tmavší barvy = body v množině
- Světlejší barvy = body mimo množinu