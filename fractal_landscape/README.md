# Generátor Fraktálové Krajiny

## Jak to funguje?

### Základní princip
Program vytváří 3D fraktálovou krajinu pomocí algoritmu "Diamond-Square" (prostorového dělení). 

### Algoritmus prostorového dělení
1. **Inicializace**
   - Vytvoří se čtvercová mřížka o velikosti 2^n + 1
   - Nastaví se výška v rozích na počáteční hodnotu

2. **Rekurzivní dělení**
   - Program postupně dělí čtverec na menší části
   - V každém kroku:
     1. Vypočítá střed čtverce (průměr výšek rohů + náhodná odchylka)
     2. Vypočítá středy stran (průměr krajních bodů + náhodná odchylka)
     3. Rozdělí čtverec na 4 menší čtverce
     4. Opakuje proces pro každý nový čtverec

3. **Parametry ovlivňující výsledek**
   - `Roughness` (Drsnost): 0.1 - 1.0
     - Určuje velikost náhodných odchylek
     - Vyšší hodnota = drsnější terén
   - `Detail Level` (Úroveň detailů): 0 - 8
     - Určuje počet dělení (iterací)
     - Vyšší hodnota = více detailů

### Ovládací prvky
- Posuvník drsnosti terénu
- Posuvník úrovně detailů
- Tlačítko pro generování nové krajiny
- 3D vizualizace s možností rotace

### Technické detaily
- Využívá NumPy pro efektivní práci s maticemi
- Matplotlib pro 3D vizualizaci
- Tkinter pro uživatelské rozhraní
