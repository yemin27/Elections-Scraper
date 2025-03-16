# Scraper výsledků voleb 2017

Tento skript slouží k získání výsledků voleb z roku 2017 z webových stránek volby.cz.

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

Skript se spouští s dvěma argumenty:

1.  URL územního celku (např. `https://www.volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=2&xnumnuts=2101`)
2.  Název výstupního CSV souboru (např. `vysledky_benesov.csv`)

Příklad spuštění:

```bash
python Scrapper.py "https://www.volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=2&xnumnuts=2101" vysledky_benesov.csv