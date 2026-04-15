% Clear workspace
clc; clear; close all;

% First Gaussian parameters
mu1_x = 0;
mu1_y = 0;
sigma1_x = 1;
sigma1_y = 1;

% Second Gaussian parameters (shifted)
mu2_x = 1.5;
mu2_y = 1.5;
sigma2_x = 0.8;
sigma2_y = 1.2;

% Grid
x = linspace(-6, 6, 250);
y = linspace(-6, 6, 250);
[X, Y] = meshgrid(x, y);

% First Gaussian
Z1 = (1/(2*pi*sigma1_x*sigma1_y)) * ...
    exp(-(((X - mu1_x).^2)/(2*sigma1_x^2) + ...
          ((Y - mu1_y).^2)/(2*sigma1_y^2)));

% Second Gaussian
Z2 = (1/(2*pi*sigma2_x*sigma2_y)) * ...
    exp(-(((X - mu2_x).^2)/(2*sigma2_x^2) + ...
          ((Y - mu2_y).^2)/(2*sigma2_y^2)));

% Plot
figure;
surf(X, Y, Z1, 'FaceAlpha', 0.9)
hold on
surf(X, Y, Z2, 'FaceAlpha', 0.9)

xlabel('X Position')
ylabel('Y Position')
zlabel('Probability Density')

view(45, 30)