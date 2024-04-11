%% TelloNav
clear, clc, close all;

allfiles = dir('./data/*.csv');
filepattern = "Kp(?<Kp>\d+(?:\.\d+)?)_Ki(?<Ki>\d+(?:\.\d+)?)_Kd(?<Kd>\d+(?:\.\d+)?)\.csv";

for i = 1:length(allfiles)
    file = allfiles(i);
    tokens = regexp(file.name, filepattern, "names");
    data = readmatrix(file.name);
    plotdata(data);
    title(sprintf("Kp = %s, Ki = %s, Kd = %s", tokens.Kp, tokens.Ki, tokens.Kd));
end

function plotdata(data)
time_s = data(:,1);
height_cm = data(:,2);
output = data(:,3);

fig = figure();
% fig.Theme = 'light';
hold on;
grid on;

yyaxis left
plot(time_s, height_cm);
ylabel("Height (cm)");
xlabel("Time (sec)");
ylim([0, 140])

yline(100, 'r--', 'Setpoint');

yyaxis right
plot(time_s, output, '--');
ylabel("PID Output");
ylim([-100 100]);
end
