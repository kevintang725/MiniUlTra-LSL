%% EEG Analysis

%% Set up Filter
fs = 512;

fc1 = 0.5;
fc2 = 50;
[b,a] = butter(5,[fc1 fc2]/(fs/2), 'bandpass');

d = designfilt("lowpassfir", ...
    PassbandFrequency=0.15,StopbandFrequency=0.2, ...
    PassbandRipple=1,StopbandAttenuation=60, ...
    DesignMethod="equiripple");

%fvtool(d)
%%
A = EMGBicep.VarName4(2:end);
%B = filtfilt(d, A);
B = filtfilt(b,a, A)

plot(B)