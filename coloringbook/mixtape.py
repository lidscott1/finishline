import pandas as pd
import geopandas as gpd
import numpy as np
import glob
import os
import datetime
from stats.statbook import StatBook, pull_loc

# Get number of testing sites in each zip code
testing_sites = pd.read_csv("spatial_data/COVID-19_Testing_Sites.csv")

testing_sites['zip'] = [s[-5:] for s in testing_sites['Address']]

zip_test_data = np.array(np.unique(testing_sites['zip'], return_counts=True))

test_site_counts = pd.DataFrame(data = zip_test_data.T, columns = ['zip', 'num_of_test_centers'])

# Transformations to raw data
date = datetime.date.today()

list_of_files = glob.glob('raw_data/*.csv') # * means all if need specific format then *.csv

latest_file = max(list_of_files, key=os.path.getctime)

df = pd.read_csv(latest_file)

df = df.loc[df.groupby('ZIP Code')['Week Number'].idxmax()].reset_index(drop=True)

df['zip'] = df['ZIP Code']

df = df.drop('ZIP Code', axis = 1)

df = df.merge(test_site_counts, how='left', on='zip')

df.loc[df['num_of_test_centers'].isna(), 'num_of_test_centers'] = 0

# Processing data with the StatBook class
tests, cases, population, testing_sites = df['Tests - Cumulative'], df['Cases - Cumulative'], df['Population'], df['num_of_test_centers']

stats = StatBook(tests, cases, population, testing_sites)

df['lower_confint_fpc'], df['upper_confint_fpc'] = stats.get_conf_interval()

df['fpc'] = stats.get_fpc()

df['interval_width'] = df['upper_confint_fpc'] - df['lower_confint_fpc']

df['score'] = stats.get_score()

df.to_csv('analysis_data/analysis_data {date}.csv'.format(date=date))

# Add testing site numbers to spatial data
geo_df = gpd.read_file('spatial_data/chicago zips.geojson')

geo_df.merge(test_site_counts, how='left', on='zip')

geo_df.to_file('spatial_data/chicago_zips_testingcounts.geojson', driver='GeoJSON')