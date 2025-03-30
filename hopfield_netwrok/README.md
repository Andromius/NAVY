# Hopfieldova Neuronová Síť

## Přehled
Implementace Hopfieldovy sítě - typu rekurentní umělé neuronové sítě používané pro rozpoznávání vzorů a ukládání do paměti.

## Hlavní Komponenty

### 1. Matice Vah
- Ukládá sílu spojení mezi neurony
- Aktualizována během tréninku pomocí Hebbova pravidla učení
- Symetrická matice s nulovou diagonálou

### 2. Proces Trénování
- Využívá Hebbovo pravidlo učení
- Váhy se aktualizují podle vzorce: váhy += vzor^T * vzor
- Diagonála matice je nastavena na nulu pro zabránění samo-spojení

### 3. Vybavování Vzorů
Implementovány dva režimy:
- **Synchronní Režim**: Všechny neurony jsou aktualizovány současně
- **Asynchronní Režim**: Neurony jsou aktualizovány postupně jeden po druhém
- Síť konverguje buď k uloženému vzoru nebo k lokálnímu minimu

### 4. Dynamika Sítě
- Využívá binární prahové neurony (hodnoty -1 nebo 1)
- Aktualizace probíhají dokud síť nedosáhne:
  - Konvergence (stabilního stavu)
  - Maximálního počtu povolených iterací

## Použití
1. Vytvoření vzoru pomocí GUI rozhraní
2. Trénování sítě na vytvořeném vzoru
3. Testování vybavování pomocí částečných nebo zašuměných vzorů
4. Možnost zobrazení uložených vzorů a jejich detailů