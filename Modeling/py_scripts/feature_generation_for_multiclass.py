### All scripts should be run on flights dataset (full or sample) after preprocessing_dataset function.

def tailnum_delay_taxi_multiclass_params(df_sample):
    """
    Input: flights csv sample or full dataset AFTER preprocessing_dataset
    Aggregates on tail_num
    Output: 
        index / join key: 'tail_num'
        columns: aggregated isCraft and isCarrier delays 
    """  
    
    df_sample['isCraft'] = df_sample['target_delay'].\
                            apply (lambda x: 1 if x == 'late_aircraft_delay' else 0)
    df_sample['isCarrier'] = df_sample['target_delay'].\
                            apply (lambda x: 1 if x == 'carrier_delay' else 0)

    tailnum_delay_taxi_df = df_sample.groupby('tail_num').agg({'dep_delay': 'median',
                                  'arr_delay' : 'median',
                                  'isCraft' : 'mean',
                                  'isCarrier' : 'mean'      
                                  })
    return tailnum_delay_taxi_df
    
    
    

def tailnum_hourly_delays_multiclass_params(df_sample):
    """
    Input: flights csv sample or full dataset AFTER preprocessing_dataset
    Aggregates on tail_num and arr_hour and tail_num and dep_hour
    Output: 2 dataframes 
        index / join key: 'tail_num' and arr_hour / dep_hour
        columns: median delays
    """  
    df_sample['isCraft'] = df_sample['target_delay'].\
                            apply (lambda x: 1 if x == 'late_aircraft_delay' else 0)
    df_sample['isCarrier'] = df_sample['target_delay'].\
                            apply (lambda x: 1 if x == 'carrier_delay' else 0)
    
    # extract hour and minute from crs_time
    df_sample['dep_hour'] = (np.round(df_sample['crs_dep_time'],-2)/100).astype(int)
    df_sample['arr_hour'] = (np.round(df_sample['crs_arr_time'],-2)/100).astype(int)
    
    tailnum_dep_hourly_delays_df = df_sample.groupby(['tail_num', 'dep_hour']).agg({'dep_delay': 'median',
                                          'carrier_delay' :  'median',
                                          'late_aircraft_delay' :  'median',
                                          'isCraft' : 'mean', 
                                          'isCarrier' : 'mean' })
    tailnum_arr_hourly_delays_df = df_sample.groupby(['tail_num', 'arr_hour']).agg({'arr_delay': 'median',
                                          'carrier_delay' :  'median',
                                          'late_aircraft_delay' :  'median',
                                          'isCraft' : 'mean', 
                                          'isCarrier' : 'mean' })
    
    return tailnum_dep_hourly_delays_df, tailnum_arr_hourly_delays_df
    
    
def carrier_branded_dayofweek_delay_multiclass_params(df_sample):
    """
    Input: flights csv sample or full dataset AFTER preprocessing_dataset
    Aggregates on op_unique_carrier, branded_share, f1_dayofweek
    
    Output: 
        index /join key: op_unique_carrier, branded_share, f1_dayofweek
        columns: median delays and isCarrier
    """      
    

    df_sample['branded_share'] = df_sample['branded_code_share'].apply(lambda x: 1 if len(x)>2 else 0)
    df_sample = df_sample.drop(columns = ['branded_code_share'])
    
    
    df_sample['isCarrier'] = df_sample['target_delay'].\
                            apply (lambda x: 1 if x == 'carrier_delay' else 0)


    df_sample['fl_date'] = pd.to_datetime(df_sample['fl_date'])
    df_sample['fl_dayofweek'] = df_sample['fl_date'].dt.dayofweek
    df_sample.drop(columns=['fl_date'], inplace=True)


    carrier_df = df_sample.groupby(['op_unique_carrier', 'branded_share', 'fl_dayofweek'])\
                                    .agg({'dep_delay': 'median',
                                          'arr_delay' : 'median',
                                          'carrier_delay' :  'median',
                                          'late_aircraft_delay' :  'median', 
                                          'isCarrier' : 'mean' })
    return carrier_df

def dest_monthly_multiclass_params(df_sample):
    """
    Input: flights csv sample or full dataset AFTER preprocessing_dataset
    Aggregates on dest_airport_id, fl_month
    
    Output: 2 dataframes 
        index / join key: dest_airport_id, fl_month
        columns: median delays and isWeather, isSecurity
    """   

    # extract hour and minute from crs_time
    df_sample['fl_date'] = pd.to_datetime(df_sample['fl_date'])
    df_sample['fl_month'] = df_sample['fl_date'].dt.month
    
    df_sample['isWeather'] = df_sample['target_delay'].\
                            apply (lambda x: 1 if x == 'weather_delay' else 0)
    df_sample['isSecurity'] = df_sample['target_delay'].\
                            apply (lambda x: 1 if x == 'security_delay' else 0)

    
    dest_monthly_params = df_sample.groupby(['dest_airport_id', 'fl_month']).agg({'arr_delay': 'median',
                                  'arr_delay' : 'median',
                                  'carrier_delay': 'median',  
                                  'nas_delay': 'median', 
                                  'late_aircraft_delay': 'median',                                    
                                  'weather_delay' : 'median',
                                  'security_delay' : 'median', 
                                  'isWeather' : 'mean' , 
                                  'isSecurity' : 'mean' ,
                                                                                  
                                  })
    
    dest_monthly_params.index.to_flat_index()
    return dest_monthly_params
    
def origin_monthly_multiclass_params(df_sample):
    """
    Input: flights csv sample or full dataset AFTER preprocessing_dataset
    Aggregates on origin_airport_id, fl_month
          
    Output: A dataframe
        index / join key: 'origin_airport_id', 'fl_month'
        columns: median delays and isWeather, isSecurity
    """
    

    # extract hour and minute from crs_time
    df_sample['fl_date'] = pd.to_datetime(df_sample['fl_date'])
    df_sample['fl_month'] = df_sample['fl_date'].dt.month

    df_sample['isWeather'] = df_sample['target_delay'].\
                            apply (lambda x: 1 if x == 'weather_delay' else 0)
    df_sample['isSecurity'] = df_sample['target_delay'].\
                            apply (lambda x: 1 if x == 'security_delay' else 0)
    
    origin_monthly_params = df_sample.groupby(['origin_airport_id', 'fl_month']).agg({'dep_delay': 'median',
                                  'arr_delay' : 'median',
                                  'carrier_delay': 'median',  
                                  'nas_delay': 'median', 
                                  'late_aircraft_delay': 'median',                                    
                                  'weather_delay' : 'median',
                                  'security_delay' : 'median', 
                                  'isWeather' : 'mean', 
                                  'isSecurity' : 'mean',
                                  })
    
    origin_monthly_params.index.to_flat_index()
    return origin_monthly_params
    
def holiday_multiclass_params(df_sample):
    """
    Input: flights csv sample or full dataset AFTER preprocessing_dataset
    Aggregates on 'holidate', 'origin_airport_id', 'dest_airport_id'
    Output: 
        Index / join key: 'holidate', 'origin_airport_id', 'dest_airport_id'
        columns: median delays,  isWeather isSecurity

    """
       
        
########################################
##  run this if holidays is not available. check the file location first
    us_holidays_df = pd.read_csv('extra/us_holidays.csv')

    from datetime import timedelta
    holidays = []
    for hol in us_holidays_df['date'].values:
        holstart = pd.to_datetime(hol) - timedelta(days=3)
        holend = pd.to_datetime(hol) + timedelta(days=3)
        holidayweek = pd.date_range(holstart, holend)
        holidays.extend(holidayweek)
#######################
    
    df_sample['isWeather'] = df_sample['target_delay'].\
                            apply (lambda x: 1 if x == 'weather_delay' else 0)
    df_sample['isSecurity'] = df_sample['target_delay'].\
                            apply (lambda x: 1 if x == 'security_delay' else 0)

    
    # get holidate 
    df_sample['fl_date'] = pd.to_datetime(df_sample['fl_date'])
    df_sample['holidate'] = df_sample['fl_date'].apply(lambda x: 1 if x in holidays else 0)


    holiday_params = df_sample.groupby(['holidate', 'origin_airport_id', 'dest_airport_id']).agg({'dep_delay': 'median',
                              'arr_delay' : 'median',
                              'carrier_delay': 'median',  
                              'nas_delay': 'median', 
                              'late_aircraft_delay': 'median',                                    
                              'weather_delay' : 'median',
                              'security_delay' : 'median',
                              'isWeather' : 'mean', 
                              'isSecurity' : 'mean',
                              })
    
    return holiday_params
        
        
def origin_dest_route_dayofweek_multiclass_params(df_sample):
    """
    Input: flights csv sample or full dataset AFTER preprocessing_dataset
    Aggregates on 'origin_airport_id', 'dest_airport_id', 'fl_dayofweek'
    
    Output: A dataframe
        Index: 'origin_airport_id', 'dest_airport_id', 'fl_dayofweek'
        columns: median delays, isCarrier
    """
    
    df_sample['isCarrier'] = df_sample['target_delay'].\
                            apply (lambda x: 1 if x == 'carrier_delay' else 0)
    
    # get dayofweek
    df_sample['fl_date'] = pd.to_datetime(df_sample['fl_date'])
    df_sample['fl_dayofweek'] = df_sample['fl_date'].dt.dayofweek
    # traffic
    
    params_df = df_sample.groupby(['origin_airport_id', 'dest_airport_id', 
                                   'fl_dayofweek']).agg({'dep_delay': 'median',
                              'arr_delay' : 'median',
                              'carrier_delay': 'median',  
                              'nas_delay': 'median', 
                              'late_aircraft_delay': 'median',                                    
                              'weather_delay' : 'median',
                              'security_delay' : 'median',
                              'isCarrier' : 'mean'
                              })

    params_df['traffic'] = df_sample.groupby(['origin_airport_id', 'dest_airport_id', 'fl_dayofweek']).size()
    
    
    return params_df
