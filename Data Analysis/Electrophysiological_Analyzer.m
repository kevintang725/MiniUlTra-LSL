%% EEG Analysis
% Author: Kai Wing Kevin Tang, 2023

clc
clear all
close all

%% Set up Filter
fs = 4096; %sampling frequency

% Third Order Butterworth Filters
[b1,a1] = butter(4,[2 100]/(fs/2), 'bandpass');
[b2,a2] = butter(4,[59 61]/(fs/2), 'stop');

% Bandstop
bsFilt = designfilt('bandstopfir','FilterOrder',2, ...
         'CutoffFrequency1',59.5,'CutoffFrequency2',60.5, ...
         'SampleRate',fs);
     
% Bandpass
bpFilt = designfilt('bandpassiir','FilterOrder',2, ...
         'HalfPowerFrequency1',2,'HalfPowerFrequency2',50, ...
         'SampleRate',fs);
    
% High Pass
hpFilt = designfilt('highpassiir','FilterOrder',2, ...
         'PassbandFrequency',2,'PassbandRipple',0.2, ...
         'SampleRate',fs);
%fvtool(hpFilt)
%% Import File
filename = "/Users/KevinTang/Desktop/UTAustin/Code/GitHub/Human Trials/FUS + EEG (SEP)/JJ_08152023/JJ_FUS-FES-.csv";
data = importfile(filename);
data = table2array(data);

% Initialize Time to Start from Zero
%time = 1e-6*(data(:,1) - data(1,1)); % Convert s to ms
time = 1000*[0:1/fs:(length(data(:,1)) - 1)/fs];

%% Pre-Processing
figure
hold on
for i = 2:5
    filtered_data(:,i) = data(:,i);
    %filtered_data(:,i) = medfilt1(filtered_data(:,i), fs/2);
    %filtered_data(:,i) = filtfilt(hpFilt, filtered_data(:,i));
    %filtered_data(:,i) = filtfilt(bsFilt, filtered_data(:,i));
    filtered_data(:,i) = filtfilt(b1, a1, filtered_data(:,i));
    filtered_data(:,i) = filtfilt(b2, a2, filtered_data(:,i));
    
    plot(time, 1e6*filtered_data(:,i), 'LineWidth', 1.5);
    %axis([-inf inf -100 100])
    %axis([2000 4000 -inf inf])
    ylabel('EEG Amplitude (uV)')
    xlabel('Time (ms)')
    set(gca,'FontSize', 14, 'LineWidth', 1)
end
%plot(time,20*data(:,58),'r','LineWidth', 2)
legend('C3', 'CP5', 'P3', 'CP1', 'FUS')
hold off

%% Power Spectrum Density
channel_names = {'C3', 'CP5', 'P3', 'CP1', 'tFUS'};
figure
for i = 1:4
    subplot(2,2,i)
    [freq(:,i), psdx(:,i)] = plot_psd(filtered_data(:,i+1), fs, channel_names(i));
end

%% Extract Epochs

[C3, CP5, P3, CP1] = extract_epochs(filtered_data, fs, data);

figure
subplot(2,2,1)
plot_epochs(C3,fs)
title('C3')
subplot(2,2,2)
plot_epochs(CP5,fs)
title('CP5')
subplot(2,2,3)
plot_epochs(P3,fs)
title('P3')
subplot(2,2,4)
plot_epochs(CP1,fs)
title('CP1')
%% Functions
function plot_epochs(ep,fs)
    y = 1e6*(mean(ep') - mean(mean(ep')));
    x = [-200:1000/fs:500];
    std_dev = std(ep');
    curve1 = y + 1e6*std_dev;
    curve2 = y - 1e6*std_dev;
    x2 = [x, fliplr(x)];
    inBetween = [curve1, fliplr(curve2)];
    %fill(x2, inBetween, 'k', 'FaceAlpha', 0.1);
    hold on;
    plot(x, y, 'r', 'LineWidth', 1.5);
    %axis([-inf inf -max(abs(curve2))-1 max(abs(curve1)) + 1])
    %rectangle('Position',[-100 min(curve2)-1 500 1], 'FaceColor',[0.3010 0.7450 0.9330])
    %axis([-inf inf -5 5])
    %rectangle('Position',[-100 -5 500 1], 'FaceColor',[0.3010 0.7450 0.9330])
    axis([-inf inf min(y)-0.01*min(y) abs(min(y)+0.01*abs(min(y)))])
    rectangle('Position',[-100 min(y)-0.01*min(y) 500 0.1*abs(min(y))], 'FaceColor',[0.3010 0.7450 0.9330])
    xline(0, '--','LineWidth', 2)
    ylabel('EEG Amplitude (uV)')
    xlabel('Time (ms)')
    set(gca,'FontSize', 14, 'LineWidth', 1)
end

function [C3, CP5, P3, CP1] = extract_epochs(filtered_data, fs, epoch_triggers)
    [pks, locs] = findpeaks(epoch_triggers(:,58));
    for i = 1:length(locs) - 1
        C3(:,i) = filtered_data(locs(i)-(100/(1/fs)/1000):locs(i)+(600/(1/fs)/1000),2);
        CP5(:,i) = filtered_data(locs(i)-(100/(1/fs)/1000):locs(i)+(600/(1/fs)/1000),3);
        P3(:,i) = filtered_data(locs(i)-(100/(1/fs)/1000):locs(i)+(600/(1/fs)/1000),4);
        CP1(:,i) = filtered_data(locs(i)-(100/(1/fs)/1000):locs(i)+(600/(1/fs)/1000),5);
    end
end

function [freq, psdx] = plot_psd(data, fs, channel)
    T = 1/fs;             % Sampling period       
    L = length(data);             % Length of signal
    t = (0:L-1)*T;        % Time vector
    X = 1e6*data;

    % Convert FFT to PSD
    xdft = fft(X);
    xdft = xdft(1:floor(L/2+1));
    psdx = (1/(fs*L)) * abs(xdft).^2;
    psdx(2:end-1) = 2*psdx(2:end-1);
    freq = 0:fs/L:fs/2;
    
    loglog(freq,psdx, 'LineWidth', 1.5) 
    %semilogy(freq,psdx, 'LineWidth', 1.5) 
    title(channel)
    xlabel("f (Hz)")
    ylabel("PSD (\muV^2 Hz^{-1})")
    axis([1 100 -inf inf])
    set(gca,'FontSize', 14, 'LineWidth', 1)
end

function data = importfile(filename, dataLines)
    %IMPORTFILE Import data from a text file
    %  data = IMPORTFILE(FILENAME) reads data from text file FILENAME
    %  for the default selection.  Returns the data as a table.
    %
    %  data = IMPORTFILE(FILE, DATALINES) reads data for the specified
    %  row interval(s) of text file FILENAME. Specify DATALINES as a
    %  positive scalar integer or a N-by-2 array of positive scalar integers
    %  for dis-contiguous row intervals.
    %
    %  Example:
    %  data = importfile("/Users/KevinTang/Desktop/UTAustin/Code/GitHub/labstreaminglayer/Code/Rehamove3/Data Analysis/Data/JJ_tFUS_80.csv", [2, Inf]);
    %
    %  See also READTABLE.
    %
    % Auto-generated by MATLAB on 07-Aug-2023 14:04:26

    % Input handling

    % If dataLines is not specified, define defaults
    if nargin < 2
        dataLines = [2, Inf];
    end

    % Set up the Import Options and import the data
    opts = delimitedTextImportOptions("NumVariables", 59);

    % Specify range and delimiter
    opts.DataLines = dataLines;
    opts.Delimiter = [" ", "["];

    % Specify column names and types
    opts.VariableNames = ["VarName1", "VarName2", "VarName3", "VarName4", "VarName5", "VarName6", "VarName7", "VarName8", "VarName9", "VarName10", "VarName11", "VarName12", "VarName13", "VarName14", "VarName15", "VarName16", "VarName17", "VarName18", "VarName19", "VarName20", "VarName21", "VarName22", "VarName23", "VarName24", "VarName25", "VarName26", "VarName27", "VarName28", "VarName29", "VarName30", "VarName31", "VarName32", "VarName33", "VarName34", "VarName35", "VarName36", "VarName37", "VarName38", "VarName39", "VarName40", "VarName41", "VarName42", "VarName43", "VarName44", "VarName45", "VarName46", "VarName47", "VarName48", "VarName49", "VarName50", "VarName51", "VarName52", "VarName53", "VarName54", "VarName55", "VarName56", "VarName57", "VarName58", "VarName59"];
    opts.VariableTypes = ["double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double"];

    % Specify file level properties
    opts.ExtraColumnsRule = "ignore";
    opts.EmptyLineRule = "read";
    opts.ConsecutiveDelimitersRule = "join";

    % Specify variable properties
    opts = setvaropts(opts, ["VarName1", "VarName2", "VarName3", "VarName4", "VarName5", "VarName6", "VarName7", "VarName8", "VarName9", "VarName10", "VarName11", "VarName12", "VarName13", "VarName14", "VarName15", "VarName16", "VarName17", "VarName18", "VarName19", "VarName20", "VarName21", "VarName22", "VarName23", "VarName24", "VarName25", "VarName26", "VarName27", "VarName28", "VarName29", "VarName30", "VarName31", "VarName32", "VarName33", "VarName34", "VarName35", "VarName36", "VarName37", "VarName38", "VarName39", "VarName40", "VarName41", "VarName42", "VarName43", "VarName44", "VarName45", "VarName46", "VarName47", "VarName48", "VarName49", "VarName50", "VarName51", "VarName52", "VarName53", "VarName54", "VarName55", "VarName56", "VarName57", "VarName58", "VarName59"], "TrimNonNumeric", true);
    opts = setvaropts(opts, ["VarName1", "VarName2", "VarName3", "VarName4", "VarName5", "VarName6", "VarName7", "VarName8", "VarName9", "VarName10", "VarName11", "VarName12", "VarName13", "VarName14", "VarName15", "VarName16", "VarName17", "VarName18", "VarName19", "VarName20", "VarName21", "VarName22", "VarName23", "VarName24", "VarName25", "VarName26", "VarName27", "VarName28", "VarName29", "VarName30", "VarName31", "VarName32", "VarName33", "VarName34", "VarName35", "VarName36", "VarName37", "VarName38", "VarName39", "VarName40", "VarName41", "VarName42", "VarName43", "VarName44", "VarName45", "VarName46", "VarName47", "VarName48", "VarName49", "VarName50", "VarName51", "VarName52", "VarName53", "VarName54", "VarName55", "VarName56", "VarName57", "VarName58", "VarName59"], "ThousandsSeparator", ",");

    % Import the data
    data = readtable(filename, opts);

end