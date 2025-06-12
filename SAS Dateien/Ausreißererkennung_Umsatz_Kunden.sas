libname meinlib '/home/u64238799/sasuser.v94/';

proc univariate data=meinlib.Umsatzdaten_Europa;
    var "Umsatz in Euro"n;
    id "Kunden ID"n;
run;

proc sgplot data=meinlib.Umsatzdaten_Europa;
    vbox "Umsatz in Euro"n;
run;

proc sgplot data=meinlib.Umsatzdaten_Europa;
    vbox "Umsatz in Euro"n / category="Modell Pumpe"n group="Vertriebsart"n;
    yaxis values=(0 5000 10000 15000 20000 25000 30000 35000 40000)
          label="Umsatz in Euro";
run;
