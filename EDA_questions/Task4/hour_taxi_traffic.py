def hour_taxi_traffic(df):
    """
    Input: flights df, whole or sample
    Output: A dataframe displaying the average total taxi time and traffic in each hour
    """
    
    # extract hour and minute from crs_time
    df['dep_hour'] = (np.round(df['crs_dep_time'],-2)/100).astype(int)
    df['arr_hour'] = (np.round(df['crs_arr_time'],-2)/100).astype(int)


    # group to get the taxi times at arrival and departure
    arr_hour_taxi_in = df.groupby('arr_hour').mean(['taxi_in'])['taxi_in']
    dep_hour_taxi_out = df.groupby('dep_hour').mean(['taxi_out'])['taxi_out']
    total_taxi_time = dep_hour_taxi_out + arr_hour_taxi_in # sum the total taxi time
    
    
    # group to get the average flights per hour, divide by all days in the dataframe
    dep_hour_flights = df.groupby('dep_hour').count()['fl_date'] / len(df['fl_date'].unique())
    arr_hour_flights = df.groupby('arr_hour').count()['fl_date'] / len(df['fl_date'].unique())
    
    hourly_flights = (dep_hour_flights + arr_hour_flights)  # add up the total flights

    # join and merge the series together to get one dataframe
    total_taxi_time['traffic'] = hourly_flights.values # join the series     
    hour_taxi_traffic = total_taxi_time.to_frame().merge(hourly_flights, left_index=True, right_index=True)

    # give proper column and index names
    hour_taxi_traffic.rename(columns={0: 'taxi_time', 'fl_date':'average traffic'}, inplace=True)
    hour_taxi_traffic.rename_axis('hour', inplace=True)
    
    # Visualize
    plt.scatter(x = hour_taxi_traffic['average traffic'], y = hour_taxi_traffic['taxi_time'])
    plt.xlabel('Flight traffic')
    plt.ylabel('Total taxi time')
    plt.show()
    
    return hour_taxi_traffic