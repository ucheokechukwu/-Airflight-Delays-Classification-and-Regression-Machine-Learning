def preparing_training_df(train_df):
        """Input: dataset after preprocessing
        check extras for  holidays csv
        Output: 3 datasets: X and y
        """
    
        ######################################################
        # getting the list of US national holidays
        # run this if 'holidays' is not available. check the file location first
        us_holidays_df = pd.read_csv('extra/us_holidays.csv')

        from datetime import timedelta
        holidays = []
        for hol in us_holidays_df['date'].values:
            holstart = pd.to_datetime(hol) - timedelta(days=5)
            holend = pd.to_datetime(hol) + timedelta(days=3)
            holidayweek = pd.date_range(holstart, holend)
            holidays.extend(holidayweek)
        #######################################################          
    
    
        # EDA: column transformations to integrate with the preprocessed feature tables:
        # binarize branded share
        train_df['branded_share'] = train_df['branded_code_share'].apply(lambda x: 1 if len(x)>2 else 0)
        # extract month and day of week and holidate
        train_df['fl_date'] = pd.to_datetime(train_df['fl_date'])
        train_df['fl_month'] = train_df['fl_date'].dt.month
        train_df['fl_dayofweek'] = train_df['fl_date'].dt.dayofweek
        train_df['fl_date'] = pd.to_datetime(train_df['fl_date'])
        train_df['holidate'] = train_df['fl_date'].apply(lambda x: 1 if x in holidays else 0)
    
        # extract flight hour
        train_df['dep_hour'] = (np.round(train_df['crs_dep_time'],-2)/100).astype(int)
        train_df['arr_hour'] = (np.round(train_df['crs_arr_time'],-2)/100).astype(int)

        # drop irrelevant columns  
        train_df.drop(columns = ['mkt_unique_carrier', 'mkt_carrier',
                             'mkt_carrier_fl_num',
                             'op_carrier_fl_num',
                             'origin', 'origin_city_name'],
                             inplace=True)
                             
        train_df.drop(columns = ['dest', 'dest_city_name',
                             'crs_elapsed_time',
                             'flights',
                             'fl_date',
                             'crs_dep_time', 'crs_arr_time',
                             'branded_code_share'],
                              inplace=True)
    
        delay_cols = ['carrier_delay', 'weather_delay',
                       'nas_delay', 'security_delay', 'late_aircraft_delay'] 
        
    #     # defining the target (y) labels
    #     df['target'] = df[delay_cols].idxmax(axis=1) # returns maximum delay
    
        # remove delays from dataset
        train_df.drop(columns=delay_cols, inplace=True)
    
        train_df.drop(columns = ['dep_time',
                           'dep_delay', 'taxi_out', 'taxi_in', 'arr_time',
                           'arr_delay', 'cancelled','actual_elapsed_time',
                           'air_time', 'isDelay'],
                                  inplace=True)
 
    ################# calling features tables
    
    # merging the testing dataset with the features tables of aggregate values
    # thereby converting categorical and ordinal columns to continuous values
    tmp = train_df
    train_df = tmp.merge(tmp2, 
                  left_on=['tail_num'], 
                  right_on=['tail_num'], how='left').merge(tmp3,
                  left_on=['tail_num','dep_hour'],
                  right_on=['tail_num','dep_hour']).merge(tmp4,
                  left_on=['tail_num','arr_hour'],
                  right_on=['tail_num','arr_hour']).merge(tmp5,
                  left_on=['op_unique_carrier', 'branded_share', 'fl_dayofweek'], 
                  right_on=['op_unique_carrier', 'branded_share', 'fl_dayofweek'],
                  suffixes=('_', '_carrier')).merge(tmp6,
                  left_on=['dest_airport_id', 'fl_month'], 
                  right_on=['dest_airport_id', 'fl_month'],
                  suffixes=('_', '_dest')).merge(tmp7,
                  left_on=['origin_airport_id', 'fl_month'], 
                  right_on=['origin_airport_id', 'fl_month'],
                  suffixes=('_', '_origin')).merge(tmp8,                                
                  left_on=['holidate', 'origin_airport_id', 'dest_airport_id'], 
                  right_on=['holidate', 'origin_airport_id', 'dest_airport_id'],
                  suffixes=('_', '_holidate')).merge(tmp9,                               
                  left_on=['origin_airport_id', 'dest_airport_id', 'fl_dayofweek'], 
                  right_on=['origin_airport_id', 'dest_airport_id', 'fl_dayofweek'],
                  suffixes=('_', '_route'))
    
    # dropping irrelevant columns
    train_y = train_df['target_delay']
    
    train_X = train_df.drop(columns = ['op_unique_carrier',
                       'tail_num',
                       'origin_airport_id',
                       'dest_airport_id', 'target_delay',
                                       'fl_month',
                                      'fl_dayofweek'])
    
    return train_y, train_X
        





def preparing_test_dataset(df):
    """Input: 'raw' testing dataframe from csv file
    This function takes the raw pd.read_csv('flights_test.csv') 
        applies the engineered feature aggregations
        and restructures it to the form it needs to be 
        for Scaling and Model Predicting
    Output: X_test. 
    """
    
    ######################################################
    # getting the list of US national holidays
    # run this if 'holidays' is not available. check the file location first
    us_holidays_df = pd.read_csv('extra/us_holidays.csv')

    from datetime import timedelta
    holidays = []
    for hol in us_holidays_df['date'].values:
        holstart = pd.to_datetime(hol) - timedelta(days=5)
        holend = pd.to_datetime(hol) + timedelta(days=3)
        holidayweek = pd.date_range(holstart, holend)
        holidays.extend(holidayweek)
    #######################################################   
    
    # column transformations to integrate with the preprocessed feature tables:  

    # binarize branded share
    df['branded_share'] = df['branded_code_share'].apply(lambda x: 1 if len(x)>2 else 0)
    # extract month and day of week and holidate
    df['fl_date'] = pd.to_datetime(df['fl_date'])
    df['fl_month'] = df['fl_date'].dt.month
    df['fl_dayofweek'] = df['fl_date'].dt.dayofweek
    df['fl_date'] = pd.to_datetime(df['fl_date'])
    df['holidate'] = df['fl_date'].apply(lambda x: 1 if x in holidays else 0)
     # extract flight hour
    df['dep_hour'] = (np.round(df['crs_dep_time'],-2)/100).astype(int)
    df['arr_hour'] = (np.round(df['crs_arr_time'],-2)/100).astype(int)   
    # drop irrelevant columns   
    df.drop(columns = ['dup', 'mkt_unique_carrier', 'mkt_carrier',
                         'mkt_carrier_fl_num',
                         'op_carrier_fl_num',
                         'origin', 'origin_city_name',
                         'dest', 'dest_city_name',
                         'crs_elapsed_time',
                         'flights',
                            'fl_date',
                            'crs_dep_time', 'crs_arr_time',
                         'branded_code_share'],
              inplace=True) 
    
    ################# calling features tables
    
    # merging the testing dataset with the features tables of aggregate values
    # thereby converting categorical and ordinal columns to continuous values
    tmp = df
    df = tmp.merge(tmp2, 
                  left_on=['tail_num'], 
                  right_on=['tail_num'], how='left').merge(tmp3,
                  left_on=['tail_num','dep_hour'],
                  right_on=['tail_num','dep_hour']).merge(tmp4,
                  left_on=['tail_num','arr_hour'],
                  right_on=['tail_num','arr_hour']).merge(tmp5,
                  left_on=['op_unique_carrier', 'branded_share', 'fl_dayofweek'], 
                  right_on=['op_unique_carrier', 'branded_share', 'fl_dayofweek'],
                  suffixes=('_', '_carrier')).merge(tmp6,
                  left_on=['dest_airport_id', 'fl_month'], 
                  right_on=['dest_airport_id', 'fl_month'],
                  suffixes=('_', '_dest')).merge(tmp7,
                  left_on=['origin_airport_id', 'fl_month'], 
                  right_on=['origin_airport_id', 'fl_month'],
                  suffixes=('_', '_origin')).merge(tmp8,                                
                  left_on=['holidate', 'origin_airport_id', 'dest_airport_id'], 
                  right_on=['holidate', 'origin_airport_id', 'dest_airport_id'],
                  suffixes=('_', '_holidate')).merge(tmp9,                               
                  left_on=['origin_airport_id', 'dest_airport_id', 'fl_dayofweek'], 
                  right_on=['origin_airport_id', 'dest_airport_id', 'fl_dayofweek'],
                  suffixes=('_', '_route'))
    
    df.drop(columns = ['op_unique_carrier',
                       'tail_num',
                       'origin_airport_id',
                       'dest_airport_id',
                                       'fl_month',
                                      'fl_dayofweek'],
              inplace=True)


    return df
