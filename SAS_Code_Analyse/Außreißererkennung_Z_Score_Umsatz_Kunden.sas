libname meinlib '/home/u64238799/sasuser.v94/';

/* Z-Score Berechnung */
proc standard data=meinlib.Umsatzdaten_Europa mean=0 std=1
    out=meinlib.Umsatzdaten_Europa_ZScore;
    var "Umsatz in Euro"n;
run;

/* Markieren der Z-Score-Ausreißer */
data meinlib.Umsatzdaten_Europa_ZScore;
    set meinlib.Umsatzdaten_Europa_ZScore;
    if abs("Umsatz in Euro"n) > 3 then Z_Ausreisser = 1;
        else Z_Ausreisser = 0;
run;

/* Optional: Z-Score-Ausreißer ausgeben */
proc print data=meinlib.Umsatzdaten_Europa_ZScore;
    where Z_Ausreisser = 1;
    var "Kunden ID"n "Umsatz in Euro"n;
run;

proc sgplot data=meinlib.Umsatzdaten_Europa_ZScore;
    scatter x="Kunden ID"n y="Umsatz in Euro"n / group=Z_Ausreisser;
run;
