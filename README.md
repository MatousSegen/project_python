# Třetí python projekt v Engeto academy
V tomto projektu se scrapují výsledky parlamentních voleb z roku [2017](https://www.volby.cz/pls/ps2017nss/ps3?xjazyk=CZ)
## Popis
Program automaticky stáhne a zpracuje data všech obcí v okrese zvoleným uživatelem a uloží je do souboru `.csv`
## Instalace knihoven
Použité knihovny jsou uloženy v souboru requirements.txt.
Instalace do virtuálního prostředí:
```
1. python -m venv venv

2. venv\Scripts\activate              #windows
2. source venv/bin/activate           #linux/macOS

3. pip install -r requirements.txt
```
## Spuštění programu
Program přijímá 2 argumenty:
1. odkaz na scrapovaný okres, například [tento](https://www.volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=9&xnumnuts=5303)
2. název výsledného souboru, který uloží do adresáře, kde program je spuštěn
```
python main.py <url_okresu> <název_souboru>
```
## Příklad spuštění
spuštění programu
```
python main.py "https://www.volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=2&xnumnuts=2109" output.csv
```
průběh programu
```
INITIALIZING SCRAPER
Downloading election results  [####################################]  100%
Data successfully obtained.
Exporting data to output.csv
File output.csv successfully created
```
Ukázka části výstupu
| code   | location                         | registered | envelopes | valid | Občanská demokratická strana | Řád národa - Vlastenecká unie | CESTA ODPOVĚDNÉ SPOLEČNOSTI | Česká str.sociálně demokrat. | Radostné Česko |
|--------|----------------------------------|------------|-----------|-------|------------------------------|-------------------------------|-----------------------------|------------------------------|----------------|
| 538043 | Babice                           | 732        | 533       | 531   | 79                           | 0                             | 1                           | 17                           | 0              |
| 538051 | Bašť                             | 1409       | 966       | 961   | 212                          | 4                             | 0                           | 39                           | 3              |
| 534684 | Borek                            | 242        | 170       | 170   | 27                           | 1                             | 0                           | 11                           | 0              |
| 538086 | Bořanovice                       | 627        | 440       | 440   | 110                          | 1                             | 0                           | 23                           | 0              |
| 538094 | Brandýs nad Labem-Stará Boleslav | 13374      | 8625      | 8580  | 1326                         | 26                            | 9                           | 488                          | 5              |
| 538108 | Brázdim                          | 533        | 374       | 373   | 49                           | 0                             | 0                           | 15                           | 1              |
| 564869 | Březí                            | 375        | 241       | 241   | 37                           | 1                             | 0                           | 8                            | 0              |
| 538132 | Čelákovice                       | 9011       | 6016      | 5977  | 1044                         | 56                            | 3                           | 359                          | 5              |
| 533254 | Černé Voděrady                   | 288        | 195       | 193   | 19                           | 4                             | 0                           | 11                           | 0              |
| 538141 | Čestlice                         | 497        | 360       | 360   | 58                           | 1                             | 0                           | 17                           | 0              |


