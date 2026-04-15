% Clear workspace
clc; clear; close all;

% First Gaussian parameters
mu1_x = 0;  mu1_y = 0;
sigma1_x = 1; sigma1_y = 1;

% Second Gaussian parameters (shifted)
mu2_x = 2.5;  mu2_y = 2.5;
sigma2_x = 0.8; sigma2_y = 1.2;

% --- Shift both Gaussians so the mixture centre is at (0,0) ---
% For equal-weight mixture Z1 + Z2, centre = average of means
mu_mix_x = (mu1_x + mu2_x) / 2;
mu_mix_y = (mu1_y + mu2_y) / 2;

% Shift both means by subtracting the mixture centre
mu1_x = mu1_x - mu_mix_x;   mu1_y = mu1_y - mu_mix_y;
mu2_x = mu2_x - mu_mix_x;   mu2_y = mu2_y - mu_mix_y;

n = 100;

% Grid (already centred at 0, so no need to change)
x = linspace(-6, 6, n);
y = linspace(-6, 6, n);
[X, Y] = meshgrid(x, y);

% First Gaussian PDF
Z1 = (1/(2*pi*sigma1_x*sigma1_y)) .* ...
     exp(-(((X - mu1_x).^2)/(2*sigma1_x^2) + ...
           ((Y - mu1_y).^2)/(2*sigma1_y^2)));

% Second Gaussian PDF
Z2 = (1/(2*pi*sigma2_x*sigma2_y)) .* ...
     exp(-(((X - mu2_x).^2)/(2*sigma2_x^2) + ...
           ((Y - mu2_y).^2)/(2*sigma2_y^2)));

% --- Combined probability options ---
Z_sum = Z1 + Z2;          % mixture (unnormalised unless you weight)
Z_overlap = Z1 .* Z2;     % overlap "interaction" hotspot

% Optional: normalise Z_sum to be a valid PDF (integral = 1)
dx = x(2) - x(1);
dy = y(2) - y(1);
Z_sum_norm = Z_sum / (sum(Z_sum, "all") * dx * dy);

%% Plot combined mixture (normalised)
figure;
surf(X, Y, Z_sum_norm)
view(45, 30)
axis off

%% Plot overlap interaction (product)
figure;
surf(X, Y, Z_overlap)
zlim([0 0.003])
view(45, 30)
axis off

hold on

% ---- Collision probability level ----
z_level = 0.0005;

% Compute contour at that level
C = contourc(x, y, Z_overlap, [z_level z_level]);

% Parse contour matrix and plot in 3D
i = 1;
while i < size(C,2)
    level = C(1,i);
    npts  = C(2,i);
    x_cont = C(1, i+1:i+npts);
    y_cont = C(2, i+1:i+npts);

    % Plot directly at the surface height
    z_cont = z_level * ones(size(x_cont));

    plot3(x_cont, y_cont, z_cont, 'r', 'LineWidth', 3)

    i = i + npts + 1;
end