import json
import datetime
import random

# Konfiguration für die Maschinen
machines_config = {
    "MAS-001": {"standort": "Werk Bochum", "typ": "Fräsmaschine XYZ", "temp_norm": 45, "temp_var": 2, "vib_norm": 3.0, "vib_var": 0.5, "druck_norm": 15, "druck_var": 1, "strom_norm": 2.5, "strom_var": 0.3, "wartung_intervall_std": 2000},
    "MAS-002": {"standort": "Werk Essen", "typ": "Montageroboter A", "temp_norm": 38, "temp_var": 1, "vib_norm": 1.5, "vib_var": 0.3, "druck_norm": 8, "druck_var": 0.5, "strom_norm": 1.2, "strom_var": 0.1, "wartung_intervall_std": 1000},
    "MAS-003": {"standort": "Werk Bochum", "typ": "Schweißanlage B", "temp_norm": 55, "temp_var": 3, "vib_norm": 4.0, "vib_var": 1.0, "druck_norm": 22, "druck_var": 1.5, "strom_norm": 5.0, "strom_var": 0.5, "wartung_intervall_std": 2000},
    "MAS-004": {"standort": "Werk Dortmund", "typ": "Prüfstand C", "temp_norm": 30, "temp_var": 1, "vib_norm": 0.8, "vib_var": 0.2, "druck_norm": 5, "druck_var": 0.3, "strom_norm": 0.8, "strom_var": 0.1, "wartung_intervall_std": 1500},
    "MAS-005": {"standort": "Werk Essen", "typ": "Lackierstrasse D", "temp_norm": 42, "temp_var": 2, "vib_norm": 2.0, "vib_var": 0.4, "druck_norm": 12, "druck_var": 0.8, "strom_norm": 3.0, "strom_var": 0.4, "wartung_intervall_std": 2000},
}

# Startzeitpunkt für die Simulation (aktuelles Datum, 1. Mai 2025, 8:00 Uhr CEST)
start_date = datetime.datetime(2025, 5, 1, 8, 0, 0)
# Dauer der Simulation: 30 Tage
simulation_duration_days = 30
# Intervalle der Messungen: alle 5 Minuten
interval_minutes = 5

data = []
messung_id = 1  # Start der Messungs-ID

# Initialisiere die Betriebsstunden für jede Maschine
betriebsstunden_aktuell = {mid: random.randint(500, config["wartung_intervall_std"] - 100) for mid, config in machines_config.items()}
letzte_wartung_dates = {mid: start_date - datetime.timedelta(hours=h) for mid, h in zip(machines_config.keys(), [random.randint(100, 1500) for _ in machines_config])} # Simuliere vergangene Wartungen

for day in range(simulation_duration_days):
    for minute_of_day in range(0, 24 * 60, interval_minutes):
        current_datetime = start_date + datetime.timedelta(days=day, minutes=minute_of_day)

        for machine_id, config in machines_config.items():
            # Erhöhe Betriebsstunden basierend auf dem Intervall (simuliert)
            betriebsstunden_aktuell[machine_id] += interval_minutes / 60

            # Normale Sensorwerte mit Zufallsschwankung
            temp = round(random.gauss(config["temp_norm"], config["temp_var"]), 1)
            vib = round(random.gauss(config["vib_norm"], config["vib_var"]), 2)
            druck = round(random.gauss(config["druck_norm"], config["druck_var"]), 1)
            strom = round(random.gauss(config["strom_norm"], config["strom_var"]), 2)

            # Simulieren von Anomalien: Erhöhte Werte, wenn Betriebsstunden nahe am Wartungsintervall sind
            if betriebsstunden_aktuell[machine_id] > config["wartung_intervall_std"] * 0.9 or random.random() < 0.02:
                temp += random.uniform(2, 8)
                vib += random.uniform(0.5, 2.0)
                druck += random.uniform(1, 5)
                strom += random.uniform(0.5, 1.5)

            # Simulieren von einem Wartungsereignis und Reset der Betriebsstunden
            if betriebsstunden_aktuell[machine_id] >= config["wartung_intervall_std"]:
                betriebsstunden_aktuell[machine_id] = random.randint(0, 50)
                letzte_wartung_dates[machine_id] = current_datetime

            data.append({
                "messung_id": messung_id,  # Hier kommt die ID rein!
                "maschinen_id": machine_id,
                "timestamp": current_datetime.isoformat() + "Z",
                "fabrikstandort": config["standort"],
                "maschinentyp": config["typ"],
                "sensor_daten": {
                    "temperatur_C": round(temp, 1),
                    "vibration_mm_s": round(vib, 2),
                    "druck_bar": round(druck, 1),
                    "stromverbrauch_kW": round(strom, 2)
                },
                "betriebsstunden_seit_wartung": round(betriebsstunden_aktuell[machine_id], 2),
                "letzte_wartung_datum": letzte_wartung_dates[machine_id].isoformat() + "Z"
            })
            messung_id += 1  # Nach jedem Datensatz erhöhen

# Speichern der Daten in einer JSON-Datei
output_filename = "produktionsmaschinen_sensordaten.json"
with open(output_filename, 'w') as f:
    json.dump(data, f, indent=2)

print(f"JSON-Datei '{output_filename}' erfolgreich mit {len(data)} Einträgen erstellt.")