def tailnum_delay_taxi(df_sample):
        """
    Input: flights df_sample, whole or sample
        should have the following columns: ['tail_num',
           'arr_delay',
           'crs_arr_time',
           'arr_time',
           'dep_delay',
           'crs_dep_time',
           'dep_time',
           'taxi_in',
           'taxi_out']
          
    Output: A dataframe displaying tail number 
        and averages for taxi_out, taxi_in, dep_delay and arr_delay
    """
    
    
    
    
    
    # checking for Null values 
    filter1 = df_sample['dep_delay'].isna()
    filter2 = (df_sample['crs_dep_time'] == df_sample['dep_time'])

    indices = df_sample[(filter1) & (filter2)].index

    for idx in indices:
        df_sample.loc[idx,'dep_delay'] = 0
    
    filter1 = df_sample['arr_delay'].isna()
    filter2 = (df_sample['crs_arr_time'] == df_sample['arr_time'])

    indices = df_sample[(filter1) & (filter2)].index

    for idx in indices:
        df_sample.loc[idx,'arr_delay'] = 0
    
    # cleaning up null values and dropping unnecessary columns
    df_sample.dropna(inplace=True)
    df_sample.drop(columns=['crs_arr_time',
                       'arr_time',
                       'crs_dep_time',
                       'dep_time'],
              inplace=True)
    tailnum_delay_taxi_df = df_sample.groupby('tail_num').agg({'dep_delay': 'mean',
                                  'taxi_out' : 'mean',
                                  'arr_delay' : 'mean',
                                  'taxi_in' : 'mean'
                                  })
    return tailnum_delay_taxi_df
    
    