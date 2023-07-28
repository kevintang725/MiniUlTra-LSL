import pandas as pd
import time
 

"""Example program to show how to read a multi-channel time series from LSL."""

from pylsl import StreamInlet, resolve_stream


def main():
    
    # first resolve an EEG stream on the lab network
    print("looking for an EEG stream...")
    streams = resolve_stream('type', 'EEG')

    # create a new inlet to read from the stream
    inlet = StreamInlet(streams[0])
    
    start = time.time()

    # create dataframe to store 
    df = pd.DataFrame()
    
    # request file name input from user
    file_name = input('Please enter the filename to save as: ')

    # request total recording time to stream
    trial_duration = input('Please enter trial duration to record in seconds: ')
    
    while True:
        # read data from streaming layer
        sample, timestamp = inlet.pull_sample()
        # compute elapsed time
        elapsed_time = time.time() - start
        print(elapsed_time)
        # append data to the dataframe
        df = df.append({'time':timestamp, 'data':sample}, ignore_index=True)
        #df = pd.concat([df, pd.DataFrame({'time':timestamp, 'data':sample})],ignore_index=False)
        if elapsed_time > int(trial_duration):
            break
    
    # display dataframe stored
    print(df)   

    # save to csv
    df.to_csv(file_name + '.csv')


if __name__ == '__main__':
    main()
