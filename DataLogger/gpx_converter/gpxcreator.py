# used for manipulating directory paths
import os

# Scientific and vector computation for python
import numpy as np
np.set_printoptions(suppress=True)

from gpx_converter import Converter

import csv
import sys

# we use pandas to import a comma-seperated values dataset
import pandas as pd

data = pd.read_csv('datain.csv', low_memory = False)
data = pd.DataFrame(data)

data['latitude'].replace('', np.nan, inplace=True)
data['longitude'].replace('', np.nan, inplace=True)
data['time'].replace('', np.nan, inplace=True)
data = data.drop('x', axis=1)
data = data.drop('y', axis=1)
data = data.drop('z', axis=1)
data = data.drop('roll', axis=1)
data = data.drop('pitch', axis=1)
data = data.drop('yaw', axis=1)
data.dropna(subset=['latitude'], inplace=True)
data['time']=data['time']+1681038660
NaN = pd.DataFrame(np.nan, index=np.arange(9), columns=data.columns)
result = pd.DataFrame()

for i in range(data.shape[0]):
    adding = pd.concat([NaN, pd.DataFrame(data.iloc[i]).T])
    result = pd.concat([result, adding])
result = result.reset_index(drop=True)
result = result.interpolate()
result['time'] = pd.to_datetime(result['time'], unit='s')
result.dropna(subset=['latitude'], inplace=True)
result = result.reset_index(drop=True)

#result.to_csv('dataout.csv')

Converter.dataframe_to_gpx( input_df=result,
                            lats_colname='latitude',
                            longs_colname='longitude',
                            times_colname='time',
                            output_file='output.gpx')
