import serial
from serial.tools import list_ports_windows
from time import sleep, perf_counter, strftime
import pandas as pd

print(list_ports_windows.iterate_comports().__next__())

port = serial.Serial('COM4')

df = pd.DataFrame()
df['time'] = 0
df['mV'] = 0
initial_reading = False
start_time = 0
elapsed_time = 0

while not initial_reading or (initial_reading and elapsed_time < 10):

    elapsed_time = float(perf_counter() - start_time)

    if port.inWaiting() != 0:
        try:
            data = float(port.readline())

            if not initial_reading:
                initial_reading = True
                start_time = perf_counter()

        except ValueError:
            continue

        print(data, elapsed_time)
        new_row = pd.Series(data={'time': elapsed_time, 'mV': data})

        df = df.append(new_row, ignore_index=True)

    sleep(0.01)

df.drop_duplicates(subset='time', inplace=True)

time = strftime('%Y%m%d_%H%M%S')
df.to_csv(f'./logs/{time}.csv')

