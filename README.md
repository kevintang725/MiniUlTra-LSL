# Bioadhesive Hydrogel-Coupled and Miniaturized Ultrasound Transducer System for Long-Term, Wearable Neuromodulation
## Author Information
Kai Wing Kevin Tang1,†, Jinmo Jeong1,†, Ju-Chun Hsieh1,†, Mengmeng Yao1, Hong Ding1, Wenliang Wang1, Xiangping Liu1, Ilya Pyatnitskiy1, Weilong He1, William D. Moscoso-Barrera1, Anakaren Romero Lozano1, Brinkley Artman1, Heeyong Huh2, Preston S. Wilson3, Huiliang Wang1* 

BioRxiv Preprint: doi: https://doi.org/10.1101/2024.07.17.603650

## Affiliation
1:Department of Biomedical Engineering, Cockrell School of Engineering, The University of Texas at Austin, Austin, Texas 78712, United States.

2:Department of Aerospace Engineering and Engineering Mechanics, Cockrell School of Engineering, The University of Texas at Austin, Austin, Texas 78712, United States.

3:Walker Department of Mechanical Engineering, Cockrell School of Engineering, The University of Texas at Austin, Austin, Texas 78712, United States.

## Repository Description
Python code integrated with Lab Streaming Layer and Rehamove 3 libraries to allow time-locked EEG recording from external electrophysiological amplifier (eego mylab, OpenBCI, BrainVision) with functional electrical stimulation and ultrasound stimulation controlled and triggered by an external microprocessing unit (Arduino Uno)

## Experimental Setup. 
Participants were positioned and seated in an adjustable height chair, where their right forearm is fully extended and supported in supination. Four 10-20 EEG electrode sites (C3, CP1, P3, CP5) were connected for recording somatosensory evoked potentials. During testing, subjects were initially stimulated by FES with varying currents (8-25 mA, 200 µs) to obtain the minimum threshold necessary to elicit muscle contraction of the right contralateral side. The SFAT-ACFAL was applied topically to CP3 manually with administration of ultrasound gel (Aquasonic 100, Parker) as interface to the scalp, which was then held in place using medical tape. Additionally, three electrical stimulation electrodes (2” Round, Reserv) were placed on the right contralateral arm (ground electrode on elbow, bipolar electrodes axially paired on the wrist via palpation of median nerve). The electrodes were connected to a functional electrical stimulation (FES) system (RehaMove3, Hasomed) for median nerve stimulation (MN), which was controlled externally by custom Python software. tFUS treatment condition stimulation occurring 100 ms before MN stimuli (360µs ON and 640µs OFF, PRF 1kHz, Pulse Duration 500ms ON 500ms OFF) was controlled by programming of microcontroller (Uno, Arduino), which was connected to trigger the ultrasound generator (BBBoq, Image Guided Therapy System), FES system (MN stimuli), and EEG amplifier for time-locked epoch events during somatosensory evoked potentials (SEP) (Supplementary Fig. 12). Custom Python code was developed to integrate all systems together in addition to use of LabStreamingLayer (LSL) to stream and log EEG data into dataframe with external data including trigger and metadata. Subjects were then subjected to three blocks of trials, where each block consisted of four trials (FUS-/FES-, FUS-/FES+, FUS+/FES-, FUS+/FES+) and each trial lasted 3 mins. Within each trial, 30 s of baseline recording occurs before 120 s of sham/FUS followed by 30s of rest recording to ensure sufficient buffered data for post-recording cleaning. Total recording session time was approximately 1 h.

## How to use (Recommended to use Anaconda and create a new environment)
1.) Download repository to your local directory.   

2.) Navigate to _Code/Rehamove3_ directory

3.) Depending on your Operating System (OS), navigate to _Code/Rehamove3/builds/python_ and copy the corresponding three files in the OS system you are using and paste them         back into the _Code/Rehamove3_ directory
    - _rehamovelib.so
    - rehamove.py
    - rehamovelib.py
    
4.) Open terminal from _Code/Rehamove3_ directory and run _ReceiveData.py_ to run Lab Streaming Layer to collect data from your recording system (it may prompt you to install      pylsl, to do so use _pip install pylsl_)

5.) To change or view experimental protocol and paradigm via triggering (TTL) from Arduino Uno. Navigate to _Arduino/Legon_et_al_2014_v3/Legon_et_al_2014_v3.ino_
    
## Experimental and Software/Hardware Setup
<img width="832" alt="image" src="https://github.com/user-attachments/assets/c9ffa133-0699-4cfc-8b81-768f76bac352">


