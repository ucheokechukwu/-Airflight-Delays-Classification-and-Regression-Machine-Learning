def dest_monthly_params(df_sample):
    """
    Input: flights df_sample, whole or sample
        should have the following columns: ['dest',
           'arr_delay',
           'crs_arr_time',
           'arr_time',
           'weather_delay',
           'security_delay',
           'cancelled',
          'fl_date']
          
    Output: A dataframe displaying dest (airport) and monthtly (1-12) averages for
        arr_delay, cancelled, weather_delay, security_detail
    """
    
    # cleaning data
    filter1 = df_sample['arr_delay'].isna()
    filter2 = (df_sample['crs_arr_time'] == df_sample['arr_time'])

    indices = df_sample[(filter1) & (filter2)].index
    for idx in indices:
        df_sample.loc[idx,'arr_delay'] = 0


    df_sample.drop(columns=['crs_arr_time',
                           'arr_time'],
                  inplace=True)
    
    # extract hour and minute from crs_time
    df_sample['fl_date'] = pd.to_datetime(df_sample['fl_date'])
    df_sample['fl_month'] = df_sample['fl_date'].dt.month
    
    df_sample[['weather_delay', 'security_delay']] = df_sample[['weather_delay', 'security_delay']].fillna(0)
    
    dest_monthly_params = df_sample.groupby(['dest', 'fl_month']).agg({'arr_delay': 'mean',
                                  'cancelled' : 'mean',
                                  'weather_delay' : 'mean',
                                  'security_delay' : 'mean'
                                  })
    
    
    return dest_monthly_params
    
    