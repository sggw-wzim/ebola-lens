"""
Projekt Nadzieja (Ebola Lens) - Produkcyjny potok danych surowych (Warstwa Bronze)
----------------------------------------------------------------------------------
Cel: Automatyczne pobieranie wyłącznie RZECZYWISTYCH, oficjalnych danych epidemiologicznych 
i kryzysowych z otwartych rejestrów instytucjonalnych (HDX, WHO, Africa CDC).
Zasada: Brak kompromisów — w przypadku niedostępności źródła skrypt zgłasza błąd, 
chroniąc repozytorium przed zanieczyszczeniem danymi syntetycznymi.
"""

import os
import requests
from datetime import datetime

# Ścieżka do warstwy surowej zgodnie z Architekturą Medalionową
BRONZE_DIR = "data/01_bronze_raw"
os.makedirs(BRONZE_DIR, exist_ok=True)

# Precyzyjny stempel czasowy dla wersjonowania historycznego migawek
DZIS = datetime.now().strftime("%Y-%m-%d")

def pobierz_dane_hdx():
    """
    ŹRÓDŁO 1: UN OCHA Humanitarian Data Exchange (HDX)
    Elastyczne wyszukiwanie i pobieranie pierwszego dostępnego pliku danych z pakietu.
    """
    print("[1/3] Pobieranie rzeczywistych danych z Humanitarian Data Exchange (HDX)...")
    
    search_url = "https://data.humdata.org/api/3/action/package_search"
    params = {"q": "ebola drc", "rows": 1}
    sciezka_pliku = os.path.join(BRONZE_DIR, f"hdx_ebola_drc_{DZIS}.csv")
    
    response = requests.get(search_url, params=params, timeout=30)
    response.raise_for_status()
    
    results = response.json().get("result", {}).get("results", [])
    if not results:
        raise ValueError("Nie znaleziono żadnych pakietów pasujących do zapytania o Ebolę w DRK w serwisie HDX.")
        
    resources = results[0].get("resources", [])
    if not resources:
        raise ValueError("Znaleziono dataset na HDX, ale lista zasobów (resources) jest pusta.")
        
    # Szukamy najpierw pliku CSV, a jeśli nie ma, bierzemy pierwszy z brzegu plik danych (np. XLSX lub ZIP/API)
    docelowy_zasob = None
    for res in resources:
        format_pliku = res.get("format", "").upper()
        if "CSV" in format_pliku or "XLS" in format_pliku or "DATA" in format_pliku:
            docelowy_zasob = res
            break
            
    # Jeśli nadal brak dopasowania po formacie, bierzemy po prostu pierwszy zasób z listy
    if not docelowy_zasob:
        docelowy_zasob = resources[0]
        
    data_url = docelowy_zasob.get("download_url") or docelowy_zasob.get("url")
    if not data_url:
        raise ValueError("Wybrany zasób HDX nie posiada adresu URL do pobrania.")
        
    print(f"  -> Pobieranie pliku z HDX (format: {docelowy_zasob.get('format')}): {data_url}")
    file_resp = requests.get(data_url, timeout=45)
    file_resp.raise_for_status()
    
    with open(sciezka_pliku, "w", encoding="utf-8") as f:
        f.write(file_resp.text)
    print(f"  -> Sukces! Zapisano autentyczny plik HDX: {sciezka_pliku}")


def pobierz_dane_who():
    """
    ŹRÓDŁO 2: World Health Organization (WHO AFRO / Disease Outbreak News)
    Pobiera oficjalne, ustrukturyzowane komunikaty epidemiologiczne.
    """
    print("[2/3] Pobieranie biuletynów z WHO AFRO...")
    
    # Stabilny strumień danych o ogniskach chorób w Regionie Afryki WHO
    url = "https://eatlas.afro.who.int/api/outbreaks/reports/json"
    sciezka_pliku = os.path.join(BRONZE_DIR, f"who_outbreaks_{DZIS}.json")
    
    odpowiedz = requests.get(url, timeout=30)
    odpowiedz.raise_for_status()
    
    with open(sciezka_pliku, "w", encoding="utf-8") as f:
        f.write(odpowiedz.text)
    print(f"  -> Sukces! Zapisano autentyczny plik WHO: {sciezka_pliku}")


def pobierz_dane_africacdc():
    """
    ŹRÓDŁO 3: Africa CDC (Centers for Disease Control and Prevention)
    Pobiera kontynentalne rejestry zagrożeń zdrowia publicznego.
    """
    print("[3/3] Pobieranie statystyk z Africa CDC...")
    
    url = "https://africacdc.org/wp-json/wp/v2/outbreaks?search=ebola"
    sciezka_pliku = os.path.join(BRONZE_DIR, f"africacdc_ebola_{DZIS}.json")
    
    odpowiedz = requests.get(url, timeout=30)
    odpowiedz.raise_for_status()
    
    with open(sciezka_pliku, "w", encoding="utf-8") as f:
        f.write(odpowiedz.text)
    print(f"  -> Sukces! Zapisano autentyczny plik Africa CDC: {sciezka_pliku}")


if __name__ == "__main__":
    print(f"=== PRODUKCYJNY POBÓR DANYCH RZECZYWISTYCH (BRONZE LAYER) [{DZIS}] ===")
    try:
        pobierz_dane_hdx()
        pobierz_dane_who()
        pobierz_dane_africacdc()
        print("=== PROCES ZAKOŃCZONY POMYŚLNIE. Dane gotowe dla analityków i MSF. ===")
    except Exception as e:
        print(f"[BŁĄD KRYTYCZNY] Nie udało się pobrać danych ze źródeł zewnętrznych: {e}")
        # Zgłaszamy wyjątek systemowy, aby GitHub Actions wyraźnie zasygnalizował awarię potoku,
        # zamiast cicho zapisywać niekompletne lub zmyślone dane.
        exit(1)
