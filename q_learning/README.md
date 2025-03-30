# Implementace Q-Learning algoritmu

## Přehled
Tato implementace demonstruje Q-learning v mřížkovém prostředí, kde se agent učí najít nejkratší cestu k sýru a zároveň se vyhýbá překážkám.

## Komponenty

### Prostředí
- Mřížkový svět o velikosti 10x10
- Agent (modrý kruh)
- Cíl/Sýr (žlutý čtverec)
- Překážky (červené čtverce)
- Počáteční pozice (konfigurovatelná)

### Parametry Q-Learningu
- **Alpha (Míra učení)**: Určuje, jak moc nové informace přepíší staré
  - Rozsah: 0-1
  - Výchozí hodnota: 0.1
  
- **Gamma (Diskontní faktor)**: Určuje důležitost budoucích odměn
  - Rozsah: 0-1
  - Výchozí hodnota: 0.9
  
- **Epsilon (Míra prozkoumávání)**: Řídí poměr mezi prozkoumáváním a využíváním
  - Rozsah: 0-1
  - Výchozí hodnota: 0.9
  - Postupně se snižuje pro omezení prozkoumávání

### Odměny
- Dosažení sýru: +100
- Naražení do překážky/zdi: -10
- Běžný pohyb: -1

### Proces učení
1. Agent začíná z počáteční pozice
2. Pro každý stav:
   - Výběr akce (prozkoumávání nebo využívání podle epsilon)
   - Provedení akce a pozorování nového stavu
   - Získání odměny
   - Aktualizace Q-hodnoty podle vzorce:
     ```
     Q(s,a) = Q(s,a) + alpha * (odměna + gamma * max(Q(s',a')) - Q(s,a))
     ```
   - Přesun do nového stavu
3. Epizoda končí, když agent dosáhne sýru
4. Proces se opakuje pro zadaný počet epizod

### Funkce
- Interaktivní editor prostředí
- Nastavitelné parametry učení
- Vizualizace průběhu učení
- Demonstrace optimální cesty
- Vizualizace Q-tabulky
- Statistiky tréninku

## Jak to funguje
1. Agent zpočátku prozkoumává náhodně kvůli vysoké hodnotě epsilon
2. Během tréninku se učí optimální akce pro každý stav
3. Q-tabulka ukládá hodnoty akcí pro každý stav
4. Po tréninku agent následuje nejvyšší Q-hodnoty k dosažení cíle
5. Demonstrace ukazuje naučenou optimální cestu