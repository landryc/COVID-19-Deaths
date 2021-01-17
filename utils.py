# Content the utilitaries functions

import numpy as np 
import pandas as pd

def parse_dates(dates, country):
    #print('parsing')
    ids = list()
    for date in dates:
        m = date.strftime('%m')
        d = date.strftime('%d')
        y = date.strftime('%y')

        if m.startswith('0'):
            m = m[1]
        if d.startswith('0'):
            d = d[1]

        ids.append(country + ' X ' + f'{m}/{d}/{y}')
    return ids

def save_forecasts(submission, country, forecasts):
    #print('save forecasts')
    dates = forecasts.index
    values = forecasts.values
    ids = parse_dates(dates, country)
    for id_, value in zip(ids, values):
        temp = pd.DataFrame({'Territory X Date' : [id_], 'target' : [value]})
        submission = submission.append(temp)
    return submission
        
def serialize(submission, nb_pred):
    if nb_pred == 7:
        file = 'SampleSubLocal.csv'
    else:
        file = 'SampleSubmission.csv'
    submission.to_csv(file, index=False)
    print('Forecasts saved in file :', file)
    
def evaluation(submission, ref):
    fusion = pd.merge(submission, ref, how='inner', on='Territory X Date')
    print('la fusion :',len(fusion))
    print('correlation & regression line')
    print('corr : ',fusion['target_x'].corr(fusion['target_y']))
    plt.plot(fusion['target_x'], fusion['target_y'])
    return mean_absolute_error(fusion['target_x'], fusion['target_y'])