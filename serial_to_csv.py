import serial
from serial.tools import list_ports_windows
from time import sleep, perf_counter, strftime
import pandas as pd

print(list_ports_windows.iterate_comports().__next__())

port = serial.Serial('COM4')

df = pd.DataFrame()
df['time'] = 0
df['force_mV'] = 0
df['displacement_mV'] = 0
initial_reading = False
start_time = 0
elapsed_time = 0

while not initial_reading or (initial_reading and elapsed_time < 20):

    elapsed_time = float(perf_counter() - start_time)

    if port.inWaiting() != 0:
        try:
            data = str(port.readline())

            s = data.split('\\t')
            force = s[0][2:]
            position = s[1][:3]

            if not initial_reading:
                initial_reading = True
                start_time = perf_counter()

        except ValueError:
            continue

        print(force, position, elapsed_time)
        new_row = pd.Series(data={'time': elapsed_time, 'force_mV': force, 'displacement_mV': position})

        df = df.append(new_row, ignore_index=True)

    sleep(0.01)

df.drop_duplicates(subset='time', inplace=True)

time = strftime('%Y%m%d_%H%M%S')
df.to_csv(f'./logs/{time}.csv')

