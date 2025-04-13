# L-Systems (Lindenmayerovy systémy)

## Popis implementace

Tento program implementuje L-systémy s grafickým uživatelským rozhraním pomocí knihoven Tkinter a Turtle Graphics.

### Hlavní komponenty

#### 1. Výpočet L-systému (`compute_system`)
- Generuje řetězec podle pravidel L-systému
- Parametry:
  - `axiom`: Počáteční řetězec
  - `rules`: Slovník přepisovacích pravidel
  - `iterations`: Počet iterací

#### 2. Vykreslování (`draw_l_system`)
- Interpretuje vygenerovaný řetězec jako grafické příkazy
- Využívá knihovnu Turtle Graphics pro vykreslování
- Podporované příkazy:
  - `F`: Pohyb vpřed s kreslením čáry
  - `b`: Pohyb vpřed bez kreslení čáry
  - `+`: Otočení doprava
  - `-`: Otočení doleva
  - `[`: Uložení aktuální pozice a úhlu
  - `]`: Návrat na uloženou pozici a úhel

#### 3. Grafické rozhraní (`LSystemGUI`)
- Hlavní okno s plátnem pro vykreslování
- Ovládací prvky:
  - Vstupní pole pro počáteční pozici (X, Y)
  - Nastavení počtu iterací
  - Tloušťka a délka čáry pomocí posuvníků
  - Přednastavené L-systémy
  - Možnost vlastní definice L-systému

### Přednastavené L-systémy
1. Koch-like obrazec (`F+F+F+F`)
2. Trojúhelníková struktura (`F++F++F`)
3. Rostlinná struktura (`F` s větvením)
4. Komplexní rostlinná struktura

### Technické detaily
- Využívá knihovny:
  - Tkinter pro GUI
  - Turtle Graphics pro vykreslování
  - StringIO pro efektivní práci s řetězci
- Podporuje:
  - Scrollování plátna
  - Dynamické překreslování při změně velikosti okna
  - Ošetření chyb při zadávání vlastních pravidel
