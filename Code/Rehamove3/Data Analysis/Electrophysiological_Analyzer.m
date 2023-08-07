%% EEG Analysis

%% Set up Filter
fs = 512;

[b1,a1] = butter(3,[2]/(fs/2), 'high');
[b2,a2] = butter(3,[59 61]/(fs/2), 'stop');


%% Filters

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
%%
data = table2array(JJtFUS80);

%%

figure
hold on
for i = 1:4
    %filtered_data(:,i) = data(:,i);
    filtered_data(:,i) = filtfilt(hpFilt, data(:,i));
    filtered_data(:,i) = filtfilt(bsFilt, filtered_data(:,i));
    
    S = filtered_data(:,i);
    
    [pks{i}, locs{i}] = findpeaks(S,'Threshold',75e-6);
    S(locs{i}) = 0;
    SS{i} = S;
    
    plot(1e6*SS{i}, 'LineWidth', 1.5);
    %axis([5000 5500 -inf inf])
    ylabel('EEG Amplitude (uV)')
    xlabel('Samples')
    set(gca,'FontSize', 14, 'LineWidth', 1)
end
plot(1*data(:,57),'r','LineWidth', 2)
legend('C3', 'CP5', 'P3', 'CP1', 'tFUS/Sham')
hold off

%%
channel_names = {'C3', 'CP5', 'P3', 'CP1', 'tFUS/Sham'};
figure
for i = 1:4
    subplot(2,2,i)
    plot_psd(filtered_data(:,i), fs, channel_names(i))
end

%%
% figure
% for i = 1:4
%     subplot(2,2,i)
%     cwt(filtered_data(:,i),seconds(1/fs));
% end

%%    

function plot_psd(data, fs, channel)
    T = 1/fs;             % Sampling period       
    L = length(data);             % Length of signal
    t = (0:L-1)*T;        % Time vector
    X = data;

    Y = fft(X);
    P2 = abs(Y/L);
    P1 = P2(1:L/2+1);
    P1(2:end-1) = 2*P1(2:end-1);

    f = fs*(0:(L/2))/L;
    plot(f,P1) 
    title(channel)
    xlabel("f (Hz)")
    ylabel("|P1(f)|")
    axis([0 50 -inf inf])
end