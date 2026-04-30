clear;clc;close all

satDensity = 470.10;

% Read the CSV file
data = readtable('satMassVolume2.csv');

dataPointSize = 7;

% Extract columns
mass = data.Mass;
volume = data.Volume;

% Create scatter plot
figure;
scatter(mass, volume,dataPointSize, 'filled');
hold on;

% Fit linear trendline
p = polyfit(mass, volume, 1);

% Generate smooth line
x_fit = linspace(min(mass), max(mass), 100);
y_fit = polyval(p, x_fit);

% Plot trendline
plot(x_fit, y_fit, '--', 'LineWidth', 2, ...
     'Color', [0.5 0.6 0.7]);

% Calculate R^2
y_pred = polyval(p, mass);
SS_res = sum((volume - y_pred).^2);
SS_tot = sum((volume - mean(volume)).^2);
R2 = 1 - (SS_res / SS_tot);

% Labels
xlabel('Mass ($kg$)', 'Interpreter', 'latex');
ylabel('Volume ($m^3$)', 'Interpreter', 'latex');
title('Satellite Volume against Satellite Mass');
ylim([0 3000])
grid on;

% Display equation + R^2
eqn = sprintf('y = %.3fx + %.3f', p(1), p(2));
text(min(mass), max(volume)*0.9, {['R^2 = ' num2str(R2,3)]});

ax = gca;              % get current axes
ax.XAxis.Exponent = 0; % remove scientific notation on x-axis
ax.YAxis.Exponent = 0; % remove scientific notation on y-axis

set(gcf, "Theme", "light");


xlim([0 20000])
ylim([0 3000])
zlim([-1.000 1.000])
hText = findobj(gcf,"Type","text")
hText.Position = [1.0180e+04,2.1967e+03,0]