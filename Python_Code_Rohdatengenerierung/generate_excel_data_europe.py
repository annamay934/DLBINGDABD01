import pandas as pd
import datetime
import random

# --- Konfiguration für den Umsatz-Datensatz ---
# Ziel: Bis zu 50 Millionen Euro Umsatz pro Jahr in 4 Jahren (2020-2024)
num_transactions_per_year_target = 8500 # Angestrebte Anzahl von Transaktionen pro Jahr (leicht erhöht für Umsatzziel)
num_customers_target = 600 # Ziel: Mehr Kunden für realistischere Datenbasis

start_date_range = datetime.date(2020, 1, 1)
end_date_range = datetime.date(2024, 12, 31) # Bis Ende 2024
total_years = (end_date_range.year - start_date_range.year) + 1
total_transactions_target = num_transactions_per_year_target * total_years

# Pumpenmodelle und ihre Basiskosten (Listenpreis vor Rabatten)
pump_models = {
    "Pumpe XS": {"base_cost": 2500, "avg_qty": 3},
    "Pumpe S":  {"base_cost": 4000, "avg_qty": 2},
    "Pumpe M":  {"base_cost": 7000, "avg_qty": 1},
    "Pumpe L":  {"base_cost": 12000, "avg_qty": 1},
    "Pumpe XL": {"base_cost": 20000, "avg_qty": 1}
}

# Vertriebsdaten
erstkontakt_options = ["Homepage", "Marketing Kampagne", "Messe", "Telefonakquise", "Empfehlung", "Bestandskunde"]
vertriebsart_options = ["Direktvertrieb", "Wiederverkäufer"] # Pool für die ERSTE Zuweisung

# Regionen und ihre Rabattstrategien
regional_discount_ranges = {
    "DACH": {"min_pct": 0.05, "max_pct": 0.15}, # 5-15% Rabatt
    "ROW_Europe": {"min_pct": 0.00, "max_pct": 0.08} # 0-8% Rabatt
}

# Fester Händler-Rabatt (auf den Listenpreis)
DEALER_DISCOUNT_PCT = 0.25 # 25% Rabatt für Händler

# Direktvertriebs-Rabatt (zusätzlich zum regionalen Rabatt, simuliert Verhandlungsspielraum)
DIRECT_SALES_ADDITIONAL_DISCOUNT_RANGE = {"min_pct": 0.07, "max_pct": 0.10} # 7-10% zusätzlich

# Europaweite Städte, Länder und Beispiel-PLZ und Regionen
locations_europe = [
    {"Land": "Deutschland", "Stadt": "Berlin", "PLZ": "10115", "Region": "DACH"},
    {"Land": "Deutschland", "Stadt": "München", "PLZ": "80331", "Region": "DACH"},
    {"Land": "Deutschland", "Stadt": "Hamburg", "PLZ": "20095", "Region": "DACH"},
    {"Land": "Deutschland", "Stadt": "Köln", "PLZ": "50667", "Region": "DACH"},
    {"Land": "Österreich", "Stadt": "Wien", "PLZ": "1010", "Region": "DACH"},
    {"Land": "Schweiz", "Stadt": "Zürich", "PLZ": "8001", "Region": "DACH"},
    {"Land": "Frankreich", "Stadt": "Paris", "PLZ": "75001", "Region": "ROW_Europe"},
    {"Land": "Frankreich", "Stadt": "Lyon", "PLZ": "69001", "Region": "ROW_Europe"},
    {"Land": "Italien", "Stadt": "Rom", "PLZ": "00118", "Region": "ROW_Europe"},
    {"Land": "Italien", "Stadt": "Mailand", "PLZ": "20121", "Region": "ROW_Europe"},
    {"Land": "Spanien", "Stadt": "Madrid", "PLZ": "28001", "Region": "ROW_Europe"},
    {"Land": "Spanien", "Stadt": "Barcelona", "PLZ": "08001", "Region": "ROW_Europe"},
    {"Land": "Niederlande", "Stadt": "Amsterdam", "PLZ": "1012 AA", "Region": "ROW_Europe"},
    {"Land": "Belgien", "Stadt": "Brüssel", "PLZ": "1000", "Region": "ROW_Europe"},
    {"Land": "Schweden", "Stadt": "Stockholm", "PLZ": "111 20", "Region": "ROW_Europe"},
    {"Land": "Dänemark", "Stadt": "Kopenhagen", "PLZ": "1050", "Region": "ROW_Europe"},
    {"Land": "Portugal", "Stadt": "Lissabon", "PLZ": "1000-001", "Region": "ROW_Europe"},
    {"Land": "Irland", "Stadt": "Dublin", "PLZ": "D01 X2R2", "Region": "ROW_Europe"},
    {"Land": "Finnland", "Stadt": "Helsinki", "PLZ": "00100", "Region": "ROW_Europe"},
    {"Land": "Polen", "Stadt": "Warschau", "PLZ": "00-001", "Region": "ROW_Europe"},
    {"Land": "Tschechien", "Stadt": "Prag", "PLZ": "110 00", "Region": "ROW_Europe"},
    {"Land": "UK", "Stadt": "London", "PLZ": "SW1A 0AA", "Region": "ROW_Europe"},
]


# --- Daten generieren ---
data = []
customer_ids = [f"CUST-{i:05d}" for i in range(1, num_customers_target + 1)]

# Speichert die Erstkontakt-Infos pro Kunde, um Konsistenz zu gewährleisten
# Enthält nun auch die Vertriebsart des Kunden
customer_initial_info = {}

# Generiere Transaktionen
for _ in range(total_transactions_target):
    customer_id = random.choice(customer_ids)

    # Prüfen, ob der Kunde bereits initiale Informationen hat
    if customer_id not in customer_initial_info:
        # Erster Kauf: Initialisierung der Kundeninformationen
        lead = "Ja"
        erstkontakt = random.choice([opt for opt in erstkontakt_options if opt != "Bestandskunde"])
        chosen_location = random.choice(locations_europe)
        land = chosen_location["Land"]
        stadt = chosen_location["Stadt"]
        postleitzahl = chosen_location["PLZ"]
        region = chosen_location["Region"]
        # Vertriebsart wird hier einmalig für den Kunden festgelegt
        vertriebsart = random.choice(vertriebsart_options)

        customer_initial_info[customer_id] = {
            "Land": land, "Stadt": stadt, "PLZ": postleitzahl, "Region": region,
            "Erstkontakt": erstkontakt, "Lead": lead, "Vertriebsart": vertriebsart
        }
    else:
        # Folgekäufe: Nutze vorhandene Kundeninformationen
        lead = "Nein"
        erstkontakt = "Bestandskunde"
        land = customer_initial_info[customer_id]["Land"]
        stadt = customer_initial_info[customer_id]["Stadt"]
        postleitzahl = customer_initial_info[customer_id]["PLZ"]
        region = customer_initial_info[customer_id]["Region"]
        vertriebsart = customer_initial_info[customer_id]["Vertriebsart"] # Vertriebsart aus initialer Info

    kaufzeitpunkt = start_date_range + datetime.timedelta(days=random.randint(0, (end_date_range - start_date_range).days))

    model_name, model_info = random.choice(list(pump_models.items()))
    listenpreis_pro_pumpe = model_info["base_cost"]
    anzahl_pumpe = random.randint(1, model_info["avg_qty"] * 2)

    # Berechnung der Rabatte
    rabatt_prozent_regional = random.uniform(
        regional_discount_ranges[region]["min_pct"],
        regional_discount_ranges[region]["max_pct"]
    )
    final_discount_factor = 1.0 # Start mit keinem Rabatt

    if vertriebsart == "Wiederverkäufer":
        final_discount_factor = (1 - DEALER_DISCOUNT_PCT)
        # Die hier angezeigten Rabattprozente beziehen sich auf den angewendeten Rabatt
        rabatt_prozent_vertrieb_gesamt = DEALER_DISCOUNT_PCT * 100
    else: # Direktvertrieb
        zusatz_rabatt_direkt = random.uniform(
            DIRECT_SALES_ADDITIONAL_DISCOUNT_RANGE["min_pct"],
            DIRECT_SALES_ADDITIONAL_DISCOUNT_RANGE["max_pct"]
        )
        total_discount_for_direct = rabatt_prozent_regional + zusatz_rabatt_direkt
        total_discount_for_direct = min(total_discount_for_direct, 0.95) # Max 95% Rabatt zur Sicherheit

        final_discount_factor = (1 - total_discount_for_direct)
        rabatt_prozent_vertrieb_gesamt = total_discount_for_direct * 100

    umsatz_in_euro = (listenpreis_pro_pumpe * anzahl_pumpe) * final_discount_factor
    umsatz_in_euro = round(umsatz_in_euro, 2)

    data.append({
        "Kunden ID": customer_id,
        "Kaufzeitpunkt": kaufzeitpunkt,
        "Umsatz in Euro": umsatz_in_euro,
        "Modell Pumpe": model_name,
        "Listenpreis pro Pumpe": listenpreis_pro_pumpe,
        "Anzahl/Menge Pumpe": anzahl_pumpe,
        "Lead (Ja/Nein)": lead,
        "Erstkontakt": erstkontakt,
        "Land": land,
        "Stadt": stadt,
        "Postleitzahl": postleitzahl,
        "Region": region,
        "Vertriebsart": vertriebsart, # Jetzt konsistent pro Kunde
        "Rabatt_Prozent_Regional_Basis": round(rabatt_prozent_regional * 100, 2), # Regionaler Anteil des Rabatts
        "Rabatt_Prozent_Vertrieb_Gesamt": round(rabatt_prozent_vertrieb_gesamt, 2) # Gesamter angewendeter Rabatt
    })

# Erstelle einen Pandas DataFrame
df = pd.DataFrame(data)

# Sortiere die Daten nach Kunden ID und Kaufzeitpunkt für bessere Lesbarkeit
df = df.sort_values(by=["Kunden ID", "Kaufzeitpunkt"]).reset_index(drop=True)

# --- DataFrame in Excel-Datei schreiben ---
output_excel_filename = "umsatz_daten_pumpwerk_europa_v3_final.xlsx" # Neuer Dateiname zur Abgrenzung
df.to_excel(output_excel_filename, index=False)

total_generated_revenue = df["Umsatz in Euro"].sum()
print(f"Excel-Datei '{output_excel_filename}' erfolgreich mit {len(df)} Einträgen erstellt.")
print(f"Gesamtumsatz in der Datei: {total_generated_revenue:,.2f} Euro")