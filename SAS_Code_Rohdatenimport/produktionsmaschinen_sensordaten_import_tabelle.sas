/* Schritt 1: JSON-Datei als Library einbinden */
libname masjson JSON "/home/u64238799/sasuser.v94/produktionsmaschinen_sensordaten2.json";

/* Schritt 2: Überblick – Struktur der Daten anzeigen */
proc contents data=masjson.alldata; run;

/* Schritt 3: Daten von Long nach Wide umwandeln und in WORK speichern */
data maschinen_wide (drop=p1 p2 value);
    length 
        maschinen_id $20
        fabrikstandort $50
        maschinentyp $50
        timestamp $30
        temperatur_C vibration_mm_s druck_bar stromverbrauch_kW betriebsstunden_seit_wartung 8.
        letzte_wartung_datum $30
        messung_id 8
    ;
    retain 
        messung_id maschinen_id fabrikstandort maschinentyp timestamp
        temperatur_C vibration_mm_s druck_bar stromverbrauch_kW 
        betriebsstunden_seit_wartung letzte_wartung_datum;

    set masjson.alldata;

    /* Werte zuweisen */
    if p1 = "messung_id" then messung_id = input(value, best32.);
    else if p1 = "maschinen_id" then maschinen_id = value;
    else if p1 = "timestamp" then timestamp = value;
    else if p1 = "fabrikstandort" then fabrikstandort = value;
    else if p1 = "maschinentyp" then maschinentyp = value;
    else if p2 = "temperatur_C" then temperatur_C = input(value, best32.);
    else if p2 = "vibration_mm_s" then vibration_mm_s = input(value, best32.);
    else if p2 = "druck_bar" then druck_bar = input(value, best32.);
    else if p2 = "stromverbrauch_kW" then stromverbrauch_kW = input(value, best32.);
    else if p1 = "betriebsstunden_seit_wartung" then betriebsstunden_seit_wartung = input(value, best32.);
    else if p1 = "letzte_wartung_datum" then do;
        letzte_wartung_datum = value;
        output;
        call missing(messung_id, maschinen_id, fabrikstandort, maschinentyp, timestamp,
                     temperatur_C, vibration_mm_s, druck_bar, stromverbrauch_kW, betriebsstunden_seit_wartung, letzte_wartung_datum);
    end;
run;

/* Schritt 4: Tabelle dauerhaft in deiner persönlichen Library speichern */
libname meinlib '/home/u64238799/sasuser.v94/';

data meinlib.maschinen_wide;
    set maschinen_wide;
run;

/* Kurzer Check der gespeicherten Tabelle */
proc print data=meinlib.maschinen_wide (obs=20); run;
