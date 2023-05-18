def daily_arrival_and_departure(flightsdf):
    """
    Input: flight dataframe
       should have the following columns: ['fl_date','origin','dest']
    Output: 2 csv files; one containing daily arrivals and one containing daily departures for each airport
    """
    
    import pandas as pd
    import numpy as np
    
    num_departures = flightsdf.groupby(by=['fl_date','origin']).count().rename(columns={'dest':'num_flights_leaving'})
    num_arrivals = flightsdf.groupby(by=['fl_date','dest']).count().rename(columns={'origin':'num_flights_arriving'})
    
    num_departures.to_csv('data/num_departures_daily.csv')
    num_arrivals.to_cwv('data/num_arrivals_daily.csv')