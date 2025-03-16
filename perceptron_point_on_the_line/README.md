# Řešení problému klasifikace bodů

## Hlavní komponenty:
### Třída Perceptron:
Perceptron má váhy (weights), bias (bias) a learning rate (learning_rate), které se během trénování upravují tak, aby minimalizovaly chybu klasifikace.

**Metody**:

`train` 
- provádí trénování perceptronu na základě vstupních bodů a jejich skutečných tříd (nad/na/pod čárou)

`predict` 
- slouží k předpovědi tříd pro body na základě naučených vah a biasu

### Generování dat:

`generate_points`
- generuje náhodné body

`get_true_labels` 
- přiřazuje každému bodu třídu (1, -1 nebo 0) na základě jeho polohy vůči cílové lineární funkci

### Vizualizace:
`visualize_perceptron` 
- vizualizuje body, cílovou funkci a rozhodovací hranici perceptronu

Rozhodovací hranice perceptronu je vykreslena jako zelená čára, která odděluje body klasifikované jako nad/na/pod čárou.

### Průběh programu:
Program generuje náhodné body a přiřazuje jim třídy na základě cílové lineární funkce.

Perceptron je trénován na těchto datech.

Po trénování jsou body klasifikovány a výsledky jsou vizualizovány spolu s cílovou funkcí a rozhodovací hranicí perceptronu.