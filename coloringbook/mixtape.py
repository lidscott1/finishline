import pandas as pd
import glob
import os
import datetime
from stats.statbook import StatBook

date = datetime.date.today()

list_of_files = glob.glob('raw_data/*.csv') # * means all if need specific format then *.csv

latest_file = max(list_of_files, key=os.path.getctime)

df = pd.read_csv(latest_file)

df = df.loc[df.groupby('zip_code').week_number.idxmax()].reset_index(drop=True)

tests, cases, population = df.tests_cumulative, df.cases_cumulative, df.population

df['zip'] = df['zip_code']

stats = StatBook(tests, cases, population)

df['lower_confint_fpc'], df['upper_confint_fpc'] = stats.get_conf_interval()

df['fpc'] = stats.get_fpc()

df['interval_width'] = df['upper_confint_fpc'] - df['lower_confint_fpc']

df.to_csv('analysis_data/analysis_data {date}.csv'.format(date=date))