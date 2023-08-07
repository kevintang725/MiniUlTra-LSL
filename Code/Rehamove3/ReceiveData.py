# Read, Record, and Save Data from AntNeuro Amplifier
# Author: Kai Wing Kevin Tang, 2023

import pandas as pd
import time


from pylsl import StreamInlet, resolve_stream
import BCI_Functions

def main():

    # first resolve an EEG stream on the lab network
    print("looking for an EEG stream...")
    streams = resolve_stream('type', 'EEG')

    # create a new inlet to read from the stream
    inlet = StreamInlet(streams[0])
    

    # create dataframe to store streamed raw EEG data 
    df = pd.DataFrame()

    # create dataframe to store moving average data
    df_moving_average = pd.DataFrame()
    
    # request file name input from user
    file_name = input('Please enter the filename to save as: ')

    # request total recording time to stream
    trial_duration = input('Please enter trial duration to record in seconds: ')
    
    # Begin timer
    start = time.time()
    while True:
        # read data from streaming layer
        sample, timestamp = inlet.pull_sample()
        # compute elapsed time
        elapsed_time = time.time() - start
        print(elapsed_time)
        # append data to the dataframe
        df = df.append({'time':timestamp, 'data':sample}, ignore_index=True)
        #df = pd.concat([df, pd.DataFrame({'time':timestamp, 'data':sample})],ignore_index=False)
        
        # calculate  moving average to the dataframe
        #moving_average = BCI_Functions.simple_moving_average(df_moving_average)
        # append moving average to the dataframe
        #df_moving_average = df_moving_average.append({'Moving Average', moving_average},ignore_index=True)

        # Check if recorded time has reached user input's total time desired
        if elapsed_time > int(trial_duration):
            # terminate and exit loop
            break
    
    # display dataframe stored
    print(df)   

    # save to csv
    df.to_csv(file_name + '.csv')


if __name__ == '__main__':
    main()
