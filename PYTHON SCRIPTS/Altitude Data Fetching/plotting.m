clear;clc;
data = readmatrix("AltitudeBands2.csv");
bar(data(1,:),data(2,:))
set(gcf, "Theme", "light");
xlabel("Altitude Bands (km)")
ylabel("Number of Satellites")
set(gcf, "Theme", "dark");
title("Satellite Population in Altitude Bands", "Position", [875.2676 4610.9879 0.0000])
hBar = findobj(gcf,"Type","bar");
hBar.FaceColor = [0.4196,0.1725,0.5647];