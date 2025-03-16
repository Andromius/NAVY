# Řešení XOR problému pomocí neruonové sítě

## Popis problému
Problém nelze řešit pouze jedním perceptronem (neuronem), jelikož není lineárně separovatelný a je tedy nutné využít více neuronů resp. neuronovou síť.

## Popis Implementace Neuronové Sítě

Tato implementace neuronové sítě se skládá ze čtyř hlavních tříd: Neuron, Layer, NeuralNetwork a main. Každá třída má svou specifickou roli v procesu vytváření, trénování a testování neuronové sítě.

### Třída Neuron

Třída Neuron reprezentuje jednotlivý neuron v neuronové síti. Každý neuron má své váhy, bias, aktivační funkci a metody pro forward a backward propagaci.

### Třída Layer

Třída Layer reprezentuje vrstvu neuronů v neuronové síti. Každá vrstva obsahuje několik neuronů a provádí forward a backward propagaci pro celou vrstvu.

### Třída NeuralNetwork

Třída NeuralNetwork reprezentuje celou neuronovou síť, která se skládá z několika vrstev. Tato třída obsahuje metody pro trénování sítě, predikci a výpočet chyby.

## Hlavní metody
`fit(inputs, targets)`
- Trénuje síť na zadaných datech.

Popis:
- Síť opakovaně prochází vstupy (inputs) a cílové hodnoty (targets)
- Pro každý vstup provede forward propagaci (výpočet výstupu)
- Porovná výstup s cílovou hodnotou a provede backward propagaci (úpravu vah)
- Tento proces se opakuje po dobu zadaného počtu epoch

`predict(inputs)`
- Používá natrénovanou síť k předpovědi výstupu pro nové vstupy.
Popis:
- Síť provede forward propagaci pro zadané vstupy.
- Vrátí výstup, který je zaokrouhlen na 0 nebo 1 (protože řešíme binární problém jako XOR).

`plot_decision_boundary`
- Vizualizace rozhodovací hranice neuronové sítě

`plot_error_history`
- Vizualizace změny chyby v trénovacích epochách sítě

### Forward propagace
Forward propagace je proces, kdy síť počítá výstup na základě vstupů. 
Probíhá od první vrstvy k poslední.

Postup:
- Vstupy se předají první vrstvě
- Každý neuron ve vrstvě:
    - Násobí vstupy svými váhami
    - Přidá bias
    - Aplikuje aktivační funkci (např. sigmoid) a spočítá svůj výstup
- Výstupy z jedné vrstvy se předají jako vstupy do další vrstvy
- Tento proces pokračuje, dokud se nedosáhne výstupní vrstvy

Příklad:

    Vstup: [0, 1]

    Síť má dvě vrstvy:

    První vrstva spočítá své výstupy.

    Druhá vrstva vezme tyto výstupy a spočítá konečný výsledek (např. 0.9).

### Backward propagace

Backward propagace je proces, kdy síť upravuje své váhy a bias, aby se zlepšila. Probíhá od poslední vrstvy zpět k první.

Postup:
- Síť spočítá chybu porovnáním svého výstupu s cílovou hodnotou.
- Pro každou vrstvu (od poslední k první):
    - Spočítá, jak moc každý neuron přispěl k chybě.
    - Upraví váhy a bias neuronů tak, aby příště udělal menší chybu.
    - K úpravě vah se používá learning rate, která určuje, jak velké budou změny.

Příklad:

    Cílová hodnota: 1

    Výstup sítě: 0.9

    Síť spočítá chybu: 1 - 0.9 = 0.1

    Upraví váhy a bias tak, aby příště byl výstup blíže k 1.

## Konfigurace použita pro řešení XOR problému
- 2 vstupy
- 2 vrstvy
    - skrytá: 2 neurony, aktivační funkce sigmoid
    - výstupní: 1 neuron, aktivační funkce sigmoid

Výstup sítě velmi úzce závisí na inicializaci vah a biasů, při nesprávné inicializaci vah nemusí dojít ke konvergenci sítě.
Proto je v kódu seed se spránvými vahami.

## Výstup
- Vizualizace rozhodovací hranice
- Průběh změny chyby během trénování
- Výstup odpovídající očekávaným hodnotám

## Možné úpravy
Síť je implementována vcelku "genericky", takže by s její pomocí bylo možné řešit i jiné problémy. Jednalo by se pouze o změny počáteční konfigurace.
