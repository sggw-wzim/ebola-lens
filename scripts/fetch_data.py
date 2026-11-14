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
    Pobiera oficjalny zbiór danych dla Demokratycznej Republiki Konga przez stabilne API.
    """
    print("[1/3] Pobieranie rzeczywistych danych z Humanitarian Data Exchange (HDX)...")
    
    # Oficjalny endpoint metadanych datasetu Eboli w DRK w serwisie HDX
    api_url = "https://data.humdata.org/api/3/action/package_show?id=drc-ebola-outbreak"
    sciezka_pliku = os.path.join(BRONZE_DIR, f"hdx_ebola_drc_{DZIS}.csv")
    
    odpowiedz = requests.get(api_url, timeout=30)
    odpowiedz.raise_for_status() # W razie błędu serwera natychmiast przerywa działanie
    
    dane_api = odpowiedz.json()
    zasoby = dane_api.get("result", {}).get("resources", [])
    
    # Wyszukujemy bezpośredni link do pliku CSV wewnątrz pakietu
    csv_url = None
    for zasob in zasoby:
        if zasob.get("format", "").upper() == "CSV":
            csv_url = zasob.get("download_url") or zasob.get("url")
            break
            
    if not csv_url:
        raise ValueError("Krytyczny błąd: Nie znaleziono zasobu CSV w oficjalnym pakiecie HDX dla Eboli w DRK.")
        
    print(f"  -> Pobieranie pliku z adresu: {csv_url}")
    plik_csv = requests.get(csv_url, timeout=45)
    plik_csv.raise_for_status()
    
    with open(sciezka_pliku, "w", encoding="utf-8") as f:
        f.write(plik_csv.text)
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
