def departure_arrival_params(passenger_df):
    """
    Input: passenger dataframe, whole or sample
       should have the following columns: ['origin_city_name','origin','departures_performed','passengers','dest_city_name','dest']
      
    Output: 2 csv files with info for departure and arrival airport passengers
    """
    #Departures DF
    departures = passenger_df[['origin_city_name','origin','departures_performed','passengers']].groupby(['origin','origin_city_name']).sum()

    #dividing by 5 to make it a yearly sum
    departures['departures_performed'] = departures['departures_performed']/5
    departures['passengers'] = departures['passengers']/5
    
    #sort and rename
    departures.sort_values('departures_performed',ascending=False)
    departures = departures.rename(columns={'departures_performed':'yearly_departures_per_ap','passengers':'yearly_passengers_per_ap'})

    departures.to_csv('data/departures_by_airport.csv')
    
    #Arrivals DF
    arrivals = passenger_df[['dest_city_name','dest','departures_performed','passengers']].groupby(['dest','dest_city_name']).sum()

    #dividing by 5 to make it a yearly sum
    arrivals['departures_performed'] = arrivals['departures_performed']/5
    arrivals['passengers'] = arrivals['passengers']/5
    
    #sort and rename
    arrivals.sort_values('departures_performed',ascending=False)
    arrivals = arrivals.rename(columns={'departures_performed':'yearly_arrivals_per_ap','passengers':'yearly_arriving_passengers_per_ap'})

    arrivals.to_csv('data/arrivals_by_airport.csv')