/* Import der Umsatzdaten aus der Excel-Datei */

/* Korrigierter 2. Schritt: PROC IMPORT direkt mit dem Dateipfad verwenden */
PROC IMPORT DATAFILE="/home/u64238799/sasuser.v94/umsatz_daten_pumpwerk_europa_v3_final.xlsx"
            OUT=WORK.Umsatzdaten_Europa /* Name des SAS-Datasets, das erstellt wird */
            DBMS=XLSX                  /* Dateityp: XLSX für neuere Excel-Dateien */
            REPLACE;                   /* Ersetzt das Dataset, falls es bereits existiert */
    SHEET="Sheet1";                    /* Standard-Name des Arbeitsblatts in Excel, wenn nicht anders benannt */
    GETNAMES=YES;                      /* Nimmt die erste Zeile als Spaltennamen */
RUN;

/* Überprüfung des importierten Datasets */
PROC CONTENTS DATA=WORK.Umsatzdaten_Europa;
RUN;

PROC PRINT DATA=WORK.Umsatzdaten_Europa (OBS=10); /* Zeigt die ersten 10 Zeilen an */
RUN;

%put &=SYSLAST;

libname meinlib '/home/u64238799/sasuser.v94/';

data meinlib.Umsatzdaten_Europa;
    set WORK.Umsatzdaten_Europa;
run;