/* 1. Bibliothek zuweisen */
libname meinlib '/home/u64238799/sasuser.v94/';

/* 2. Clusteranalyse durchführen, Ergebnisdatensatz mit Cluster-Zuordnung erzeugen */
proc fastclus data=meinlib.maschinen_wide maxclusters=3 out=cluster_ergebnis;
    var betriebsstunden_seit_wartung temperatur_C vibration_mm_s stromverbrauch_kW;
run;

/* 3. Beispielhafte Ausgabe der ersten 10 Beobachtungen mit Cluster-Zuordnung */
proc print data=cluster_ergebnis (obs=10);
run;

/* 4. Streudiagramm: Betriebsstunden vs Temperatur, Cluster farbig nach Standardfarben */
proc sgplot data=cluster_ergebnis;
    scatter x=betriebsstunden_seit_wartung y=temperatur_C / group=cluster;
run;

/* 5. Streudiagramm: Betriebsstunden vs Vibration, Cluster farbig nach Standardfarben */
proc sgplot data=cluster_ergebnis;
    scatter x=betriebsstunden_seit_wartung y=vibration_mm_s / group=cluster;
run;

/* 6. Streudiagramm: Betriebsstunden vs Druck, Cluster farbig nach Standardfarben */
proc sgplot data=cluster_ergebnis;
    scatter x=betriebsstunden_seit_wartung y=druck_bar / group=cluster;
run;


