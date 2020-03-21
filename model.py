# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

#installed all packages with anaconda promt, e.g.:
#conda install -c conda-forge fbprophet

import pandas as pd
import datetime
import fbprophet

raw = pd.read_csv("/Users/maxehrlich/Downloads/RKI_COVID19.csv",  sep=',')

#filter only needed columns
filtered_columns = raw.filter(["Meldedatum", "AnzahlFall"])
#char field to date field
filtered_columns['Meldedatum'] = filtered_columns.apply(lambda x: datetime.datetime.strptime(str(x.Meldedatum),'%Y-%m-%dT%H:%M:%S.000Z').strftime('%Y-%m-%d'), axis=1)
filtered_columns['Meldedatum'] = pd.to_datetime(filtered_columns['Meldedatum'])
#delete current date (as day is not over yet - still to find out: when does data get loaded?)
#filtered_timeframe = filtered_columns[filtered_columns['Meldedatum'] < datetime.datetime.today()]
filtered_timeframe = filtered_columns[filtered_columns['Meldedatum'] < datetime.datetime.strptime(str('2020-03-19'),'%Y-%m-%d')]

"""
Here we need to add a loop per Bundesland or Landkreis to save regional files for "forecast_merged" and "prophet_df"
"""
#aggregate per date
cumsum_df = filtered_timeframe.groupby(by='Meldedatum').sum()
cumsum_df['Meldedatum'] = cumsum_df.index
cumsum_df['Meldedatum'] = pd.to_datetime(cumsum_df['Meldedatum'])


"""
IDEA:
set a dynamic cap, dependend on population or even better on proportion infected/not yet infected (2 weeks you can infect others)
STUPID APPROACH: 
    Data analysis and recent reports (here) lead to the estimate of “doubling times” for infected populations of somewhere between 3 to 6 days. (For Italy, the rate is 5 days, while in the US, France, and Germany, it has been 3 days).
    https://www.diamandis.com/blog/coronavirus-exponential-implications
CLEVER APPROACH:
    make it dependend from past growth (as this can change by different behaviour - assume whole DE as same growth rate)
FIRST TRY:
   (runsum #infected 2 days ago + runsum #infected 1 day ago) * 0.64
"""

#prediction
prophet_df = cumsum_df.rename(columns={'Meldedatum': 'ds', 'AnzahlFall': 'y'})
prophet_df['cap'] = 10000
plotdata_prophet = fbprophet.Prophet(changepoint_prior_scale=50, daily_seasonality=False, weekly_seasonality=False, growth='logistic')
plotdata_prophet.fit(prophet_df)
# Make a future dataframe for 2 years (periods = [months])
forecast_merged = plotdata_prophet.make_future_dataframe(periods=30, freq='d')
forecast_merged['cap'] = 10000
# Make predictions
forecast_merged = plotdata_prophet.predict(forecast_merged)

"""
later to be replaced by Tableau with slider, database for that is: 
    - forecast_merged: ds, yhat, yhat_upper, yhat_lower
    - prophet_df: y
"""

#vizualisation
import matplotlib.pyplot as plt
figsize=(15, 10)
xlabel='ds'
ylabel='y'
fig = plt.figure(facecolor='w', figsize=figsize)

ax = fig.add_subplot(111)
fcst_t = prophet_df['ds'].dt.to_pydatetime()
ax.plot(prophet_df['ds'].dt.to_pydatetime(), prophet_df['y'], 'k.')
ax.plot(forecast_merged['ds'], forecast_merged['yhat'], ls='-', c='#0072B2')
ax.fill_between(forecast_merged['ds'], forecast_merged['yhat_lower'], forecast_merged['yhat_upper'], color='#0072B2', alpha=0.2)
ax.grid(True, which='major', c='gray', ls='-', lw=1, alpha=0.2)
ax.set_xlabel(xlabel)
ax.set_ylabel(ylabel)
ax.legend(('actual','forecast', 'forecastrange'))
fig.tight_layout()
fig

