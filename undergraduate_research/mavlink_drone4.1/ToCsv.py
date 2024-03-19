import pandas as pd
import numpy as np

def tocsv(data ,filename):
    csv_file = np.array(data)
    df = pd.DataFrame(csv_file)
    df.to_csv(filename, index=False, header=["time", "Lat","Lon", "Alt", "LPG", "CH4", "CO", "CO2", "NO2", 'PM1_0', 'PM2_5', "PM10_0", "TimeMeasured"])