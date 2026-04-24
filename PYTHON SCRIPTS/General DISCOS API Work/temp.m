data = readmatrix('orbit_counts_by_year.csv');

year = data(:,1);
values = data(:,2:10);

object_classes = [
    "Payload"
    "Payload Mission Related Object"
    "Payload Fragmentation Debris"
    "Payload Debris"
    "Rocket Body"
    "Rocket Mission Related Object"
    "Rocket Fragmentation Debris"
    "Rocket Debris"
    "Unknown"
];

figure;
b = bar(year, values, 'stacked');

title("Evolution of Earth's Space Environment")
xlabel("Epoch Year")
ylabel("Object Count")

legend(object_classes, "Location", "eastoutside");
grid on;

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

% Payload classes = blue
for i = 1:4
    b(i).FaceColor = blue_shades(i,:);
end

% Rocket classes = red
for i = 5:8
    b(i).FaceColor = red_shades(i-4,:);
end

% Unknown = gray
b(9).FaceColor = gray_color;