clc; clear; close all;

%% Means of satellite centre uncertainty (2D encounter plane)
mu1 = [0, 0];
mu2 = [2.5, 1.5];

%% 1-sigma uncertainties in x and y (diagonal covariances here)
sig1 = [1.0, 1.0];
sig2 = [0.8, 1.2];

Sigma1 = diag(sig1.^2);
Sigma2 = diag(sig2.^2);

%% Satellite hard-body radii
r1 = 0.4;
r2 = 0.4;
R  = r1 + r2;              % collision radius in relative space

%% Relative distribution r = x2 - x1 ~ N(muR, SigmaR)
muR    = mu2 - mu1;
SigmaR = Sigma1 + Sigma2;

%% ---- GRID INTEGRATION (toolbox-free) ----
% Grid extent: mean offset + several sigmas + collision radius
smax = sqrt(max(eig(SigmaR)));     % typical scale
L = max(abs(muR)) + 6*smax + R;    % half-width of grid

n = 700;                           % increase for accuracy (500-1000 typical)
x = linspace(-L, L, n);
y = linspace(-L, L, n);
[X, Y] = meshgrid(x, y);
dx = x(2) - x(1);
dy = y(2) - y(1);

% Bivariate normal PDF (no toolbox)
P = [X(:) Y(:)];
dP = P - muR;                      % subtract mean
invS = inv(SigmaR);
detS = det(SigmaR);

quad = sum((dP * invS) .* dP, 2);  % quadratic form for each grid point
pdfR = exp(-0.5 * quad) / (2*pi*sqrt(detS));
pdfR = reshape(pdfR, size(X));

% Collision region mask: ||r|| <= R
mask = (X.^2 + Y.^2) <= R^2;

% Probability integral over disk
Pcoll_grid = sum(pdfR(mask), "all") * dx * dy;

fprintf("Collision radius R = %.4f\n", R);
fprintf("Grid estimate P(coll) = %.8g\n", Pcoll_grid);

%% ---- OPTIONAL: MONTE CARLO sanity check (still toolbox-free) ----
doMC = true;
if doMC
    N = 5e5; % adjust up/down for speed/accuracy

    % Sample r ~ N(muR, SigmaR) using Cholesky: r = muR + z*L', z~N(0,I)
    Lchol = chol(SigmaR, 'lower');          % SigmaR = L*L'
    z = randn(N, 2);
    r = z * Lchol.' + muR;                  % Nx2 samples

    Pcoll_mc = mean(sum(r.^2, 2) <= R^2);
    fprintf("MC estimate   P(coll) = %.8g (N=%.0f)\n", Pcoll_mc, N);
end

%% ---- PLOT: relative PDF + collision disk ----
figure;
surf(X, Y, pdfR, 'FaceAlpha', 0.95);
shading interp
colormap turbo
colorbar
hold on

t = linspace(0, 2*pi, 400);
plot3(R*cos(t), R*sin(t), 0*t, 'k--', 'LineWidth', 2);        % collision boundary
plot3(muR(1), muR(2), 0, 'ko', 'MarkerFaceColor', 'k');       % mean relative position

xlabel('Relative X (x_2 - x_1)');
ylabel('Relative Y (y_2 - y_1)');
zlabel('PDF of relative position');
title(sprintf('Collision Probability = %.3g (grid)', Pcoll_grid));
view(45, 30);
grid on
axis off