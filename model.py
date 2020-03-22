# -*- coding: utf-8 -*-
"""
code reads datasource from local path and transforms it so that you can use it to build a prediction model from that (predict # new infections in DE)
"""

#installed all packages with anaconda promt, e.g.:
#conda install -c conda-forge fbprophet

import pandas as pd
import datetime
import fbprophet

"""
read datasource:
in this implementation you need to first to download daily updated file from
https://npgeo-corona-npgeo-de.hub.arcgis.com/datasets/dd4580c810204019a7b8eb3e0b329dd6_0
and then fit the pathname to your path

code to download this file automatically and save it on S3 can be found in data_importer.zip in this github repository
"""

#fit to your file-path
raw = pd.read_csv("/Users/maxehrlich/Downloads/RKI_COVID19.csv",  sep=',')

"""
transform data:
date filter needs to be done dynamically for daily runs of the script
"""
#filter only needed columns
filtered_columns = raw.filter(["Meldedatum", "AnzahlFall"])
#char field to date field
filtered_columns['Meldedatum'] = filtered_columns.apply(lambda x: datetime.datetime.strptime(str(x.Meldedatum),'%Y-%m-%dT%H:%M:%S.000Z').strftime('%Y-%m-%d'), axis=1)
filtered_columns['Meldedatum'] = pd.to_datetime(filtered_columns['Meldedatum'])
#filtered_timeframe = filtered_columns[filtered_columns['Meldedatum'] < datetime.datetime.today()]
filtered_timeframe = filtered_columns[filtered_columns['Meldedatum'] < datetime.datetime.strptime(str('2020-03-19'),'%Y-%m-%d')]

#aggregate per date
cumsum_df = filtered_timeframe.groupby(by='Meldedatum').sum()
cumsum_df['Meldedatum'] = cumsum_df.index
cumsum_df['Meldedatum'] = pd.to_datetime(cumsum_df['Meldedatum'])


#final data source
prophet_df = cumsum_df.rename(columns={'Meldedatum': 'ds', 'AnzahlFall': 'y'})

"""
current status: this dataframe needs to be copied into Calculations.xlsx in sheet "model training"
"""
