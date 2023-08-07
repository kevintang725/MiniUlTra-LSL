%% EEG Analysis

%% Set up Filter
fs = 512;

[b1,a1] = butter(3,[2 90]/(fs/2), 'bandpass');
[b2,a2] = butter(3,[59 61]/(fs/2), 'stop');


%%
bsFilt = designfilt('bandstopfir','FilterOrder',40, ...
         'CutoffFrequency1',59,'CutoffFrequency2',61, ...
         'SampleRate',fs);
     
bpFilt = designfilt('bandpassiir','FilterOrder',40, ...
         'HalfPowerFrequency1',8,'HalfPowerFrequency2',50, ...
         'SampleRate',fs);
%fvtool(d)
%%
data = table2array(JJtFUSSham);
%time = 1000*(data(:,2) - data(1,2));
%%
figure
hold on
for i = 1:4
    %filtered_data(:,i) = filtfilt(b1,a1, data(:,i));
    %filtered_data(:,i) = filtfilt(b2,2, filtered_data(:,i));
    filtered_data(:,i) = filtfilt(bsFilt, data(:,i));
    filtered_data(:,i) = filtfilt(bpFilt, filtered_data(:,i));
    plot(time,1e6*filtered_data(:,i), 'LineWidth', 1.5);
    %axis([5000 5500 -inf inf])
    ylabel('EEG Amplitude (uV)')
    xlabel('Time (ms)')
    set(gca,'FontSize', 14, 'LineWidth', 1)
end
plot(50*data(:,57),'r','LineWidth', 2)
legend('C3', 'CP5', 'P3', 'CP1', 'tFUS/Sham')

%%
