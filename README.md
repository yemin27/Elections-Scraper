# 3. Projekt Engeto Akademie
Projekt je tvořen dle zadání od Engeta.

# Scraper výsledků voleb 2017

Tento skript slouží k získání výsledků voleb z roku 2017 z webových stránek volby.cz, tady je přesný odkaz https://www.volby.cz/pls/ps2017nss/ps3?xjazyk=CZ.

## Instalace

1.  Vytvořte virtuální prostředí (doporučeno):
    ```bash
    python -m venv venv
    ```
2.  Aktivujte virtuální prostředí:
    * Windows:
        ```bash
        venv\Scripts\activate
        ```
    * macOS/Linux:
        ```bash
        source venv/bin/activate
        ```
3.  Nainstalujte potřebné knihovny:
    ```bash
    pip install requests beautifulsoup4
    ```

## Spuštění

#Spuštění projektu
Spuštění souboru Scraper.py v rámci příkazového řádku požaduje 2 povinné argumenty.

python election_scraper <odkaz-uzemniho-celku> <vysledny-soubor>
Následně se vám stáhnou výsledky jako soubor s příponou .csv.

Skript se spouští s dvěma argumenty:

1.  URL územního celku (např. `https://www.volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=2&xnumnuts=2101`)
2.  Název výstupního CSV souboru (např. `vysledky.csv`)

Příklad spuštění:

```bash
python Scrapper.py "https://www.volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=2&xnumnuts=2101" vysledky.csv
