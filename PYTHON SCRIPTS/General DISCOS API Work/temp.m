data = readmatrix('dataRearranged.csv');

year = data(:,1);
values = data(:,2:10);

% Make cumulative down the rows
values = cumsum(values, 1);

% Plot
figure;
b=bar(year, values, 'stacked');

xlabel('Year');
ylabel('Cumulative Counts');
title('Cumulative Stacked Bar Chart');

object_classes = ["Rocket Body","Rocket Mission Related Object","Rocket Fragmentation Debris","Rocket Debris","Payload","Payload Mission Related Object","Payload Fragmentation Debris","Payload Debris","Unknown"];
object_classes_alt = ["Payload","Payload Mission Related Object","Payload Fragmentation Debris","Payload Debris","Rocket Body","Rocket Mission Related Object","Rocket Fragmentation Debris","Rocket Debris","Unknown"];
legend(object_classes, 'Location','eastoutside');
grid on;

set(gcf, "Theme", "light");
 
legend(object_classes_alt, "Location", "none", "Position", [0.1758 0.6340 0.1714, 0.2528])
title("Evolution of Earth""s Space Environment")
xlabel("Epoch Year")
ylabel("Object Count")

% Define colors
blue_shades = [
    0.2 0.4 0.8
    0.3 0.5 0.9
    0.4 0.6 1.0
    0.6 0.7 1.0
];

red_shades = [
    0.8 0.2 0.2
    0.9 0.3 0.3
    1.0 0.4 0.4
    1.0 0.6 0.6
];

gray_color = [0.5 0.5 0.5];

% Apply colors
for i = 1:4
    b(i).FaceColor = blue_shades(i,:);
end

for i = 5:8
    b(i).FaceColor = red_shades(i-4,:);
end

b(9).FaceColor = gray_color;