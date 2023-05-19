def passenger_fuel_df(fuel_df,passenger_df,flight_df):
    """
    Input: fuel dataframe, whole or sample
        should have the following columns: ['year','carrier','total_gallons']
       
       passenger dataframe, whole or sample
       should have the following columns: ['year','passengers']
       
       flight dataframe
       should have the following columns: ['fl_date','mkt_unique_carrier','distance','dep_delay']
    Output: csv file of average distance, passenger and fuel info by air carrier
    """
    #passengers by air carrier
    passengers_bycarrier = passenger_df[passenger_df['year']>2017][['carrier','passengers']].groupby('carrier').sum().sort_values('passengers',ascending=False)
    
    #total fuel consumption per air carrier for years present in flights
    fuel_con_bycarrier = fuel_df[fuel_df['year']>2017][['carrier','total_gallons']].groupby('carrier').sum().sort_values('total_gallons',ascending=False)
    
    #add time variables
    flight_df['month'] = pd.DatetimeIndex(df['fl_date']).month
    flight_df['year'] = pd.DatetimeIndex(df['fl_date']).year
    
    #calculate df with flight info by month and year
    flights_by_carriermonth = flight_df[['mkt_unique_carrier','month','year','distance','dep_delay']].groupby(['mkt_unique_carrier','month','year']).sum()
    
    #calculate average amounts per carrier per month
    average_by_carrier = flights_by_carriermonth[['distance','dep_delay']].groupby('mkt_unique_carrier').mean()
    
    #merge dataframes together
    qtendf = average_by_carrier.merge(fuel_con_bycarrier,how = 'left', left_index = True, right_index=True)
    qtendf = qtendf.merge(passengers_bycarrier,how = 'left', left_index = True, right_index=True)
    
    #calculate median gallons for non-null
    median_gallon = qtendf[qtendf['total_gallons']>0]['total_gallons'].median()
    
    #divide passengers and gallons by 24 months to bring to an average monthly total
    qtendf['passengers'] = qtendf['passengers']/24
    qtendf['total_gallons'] = qtendf['passengers']/24
    
    #replace null gallons with median
    qtendf['total_gallons'] = qtendf['total_gallons'].where(qtendf['total_gallons']>0,median_gallon)
    
    #calculate average distance per passenger
    qtendf['monthly_distance_per_passenger'] = (qtendf['passengers']/qtendf['distance'])
    
    #calculate average gallons per distance per passenger
    qtendf['avgfuel_percustomer_perdistance'] = qtendf['total_gallons']/qtendf['monthly_distance_per_passenger']
    
    #rename columns for clarity
    qtendf = qtendf.rename(columns={'distance':'avg_distance_per_month_by_carrier','dep_delay':'avg_dep_delay_by_carrier','passengers':'passengers_by_carrier_per_month'})
    
    #post to csv
    qtendf.to_csv('data/passenger_fuel_df.csv')