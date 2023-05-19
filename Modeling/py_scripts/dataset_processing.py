def feature_generation (df_full, save_features=0):
    
    """
    input: none but df_full = flights_csv full dataset after initial cleaning
    and test/train split should already be declared in the notebook.
    
    generates the aggregate features used for model training
    
    returns: either returns the dataframes or it saves them to csv
    """
    tmp = preprocessing_dataset(df_full)
    

    tmp2 = tailnum_delay_taxi_multiclass_params(tmp)
    tmp3, tmp4 = tailnum_hourly_delays_multiclass_params(tmp)
    tmp5 = carrier_branded_dayofweek_delay_multiclass_params(tmp)
    tmp6 = dest_monthly_multiclass_params(tmp)
    tmp7 = origin_monthly_multiclass_params(tmp)
    tmp8 = holiday_multiclass_params(tmp)
    tmp9 = origin_dest_route_dayofweek_multiclass_params(tmp)
    
    # save to file
    if save_features:
        tmp2.to_csv('../data/features_tailnum_delay_taxi_multiclass_params.csv')
        tmp3.to_csv('../data/tailnum_hourly_delays_multiclass_params_dep.csv')
        tmp4.to_csv('../data/tailnum_hourly_delays_multiclass_params_arr.csv')
        tmp5.to_csv('../data/carrier_branded_dayofweek_delay_multiclass_params.csv')
        tmp6.to_csv('../data/dest_monthly_multiclass_params.csv')
        tmp7.to_csv('../data/origin_monthly_multiclass_params.csv')
        tmp8.to_csv('../data/holiday_multiclass_params.csv')
        tmp9.to_csv('../data/origin_dest_route_dayofweek_multiclass_params.csv')
        return tmp
    else:       
        return tmp, tmp2, tmp3, tmp4, tmp5, tmp6, tmp7, tmp8, tmp9
        
        
def preprocessing_dataset(df):
    """
    Input: full dataset or a sample dataset of flights_csv after initial cleaning (check duplicates etc)
    returns: clean dataset (no null values) and only records of delayed flights for analysis
    """
    
    # cleaning 'arr_delay' and 'dep_delay'
    # remove any null values that are left after calling the cleaning function
    df = cleaning_delays(df)
    df.dropna(subset=['arr_delay', 'dep_delay'], inplace=True) 
    unused_cols = ['wheels_off', 
                    'wheels_on',
                    'diverted',
                    'cancellation_code',
                    'dup',
                    'first_dep_time',
                    'total_add_gtime',
                    'longest_add_gtime',
                    'no_name']
    df = df.drop(columns=unused_cols) # delete unnecessary cols
    # column for the target labels
    # clean the delay variables, fill with 0, assuming nan delays were 0
    delay_cols = ['carrier_delay', 'weather_delay',
       'nas_delay', 'security_delay', 'late_aircraft_delay'] 
    for col in delay_cols:
        df[col].fillna(0, inplace=True) 
    
    
    # filter out records where there were no delays
    df['isDelay'] = df['arr_delay'].apply(lambda x: 1 if x>0 else None)
    df['isDepDelay'] = df['dep_delay'].apply(lambda x: 1 if x>0 else None)
    df['isDelay'].fillna(df['isDepDelay'], inplace=True)
    df.drop(columns=['isDepDelay'], inplace=True)
    df.dropna(subset='isDelay', inplace=True)
    
    # defining the target (y) labels
    df['target_delay'] = df[delay_cols].idxmax(axis=1) # returns maximum delay
    

    
    return df
    
    
    
def cleaning_delays (df_sample):
    """input flights csv full dataset or sample data
    checks null values for dep_delay and arr_delay 
    against crs_times and actual times to confirm they are null and not 0s
    usually CALLED by preprocessing_dataset
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
        
        
    return df_sample
    
    
