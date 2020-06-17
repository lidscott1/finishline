import pandas as pd
import geopandas as gpd
import numpy as np
import folium
from stats.statbook import StatBook, pull_loc
import datetime

geo_df = gpd.read_file('spatial_data/chicago_zips_testingcounts.geojson')

# zip code 60707 has a duplicate, objectid 35 and 51, 51 is the smaller area so drop that one
geo_df = geo_df.drop(index = 50)

# Transformations to raw data
date = datetime.date.today()

df = pd.read_csv('analysis_data/analysis_data {date}.csv'.format(date=date), dtype={'ZIP Code': str})

df = df.rename(columns={'ZIP Code': 'zip'})

geo_df = geo_df.merge(df, on='zip')

geo_df = geo_df[(geo_df['fpc'] <= 1) & (geo_df['fpc'] > 0)]

# Boiler plate code for mapping

mymap = folium.Map(location=[41.8781, -87.623177], zoom_start=11, tiles = None)

folium.TileLayer('CartoDB positron',name="Light Map",control=False).add_to(mymap)

geo_df['interval_width'] = np.round(geo_df['interval_width'], 5)

myscale = (geo_df['interval_width'].quantile((0,0.2,0.4,0.6,0.8,1))).tolist()

folium.Choropleth(
    geo_data=geo_df,
    name='Choropleth',
    data=geo_df,
    columns=['zip','interval_width'],
    key_on='feature.properties.zip',
    fill_color='YlGnBu',
    threshold_scale=myscale,
    fill_opacity=0.4,
    line_opacity=0.2,
    legend_name='Interval Width',
    smooth_factor=0
).add_to(mymap)

style_function = lambda x: {'fillColor': '#ffffff',
                            'color':'#000000',
                            'fillOpacity': 0.1,
                            'weight': 0.1}
highlight_function = lambda x: {'fillColor': '#000000',
                                'color':'#000000',
                                'fillOpacity': 0.50,
                                'weight': 0.1}
zip_highlighter = folium.features.GeoJson(
    geo_df,
    style_function=style_function,
    control=False,
    highlight_function=highlight_function,
    tooltip=folium.features.GeoJsonTooltip(
        fields=['zip','interval_width','num_of_test_centers','score'],
        aliases=['Zip Code: ','interval_width: ','Test Centers: ', 'Score: '],
        style=("background-color: white; color: #333333; font-family: arial; font-size: 12px; padding: 10px;")
    )
)

mymap.add_child(zip_highlighter)

mymap.keep_in_front(zip_highlighter)

folium.LayerControl().add_to(mymap)

# Read in testing sites and transform location data from string to (float, float)
testing_sites = pd.read_csv("spatial_data/COVID-19_Testing_Sites.csv")

testing_sites['Location_int'] = testing_sites.loc[:, 'Location'].apply(pull_loc)

testing_sites = testing_sites.loc[testing_sites['Location_int'] != (None, None),:].reset_index(drop=True)

# Paste on Testing site locations
for i in range(len(testing_sites)):
    
    fac = testing_sites.loc[i, 'Facility']
    
    phone = testing_sites.loc[i, 'Phone']
    
    folium.Marker(location=testing_sites.loc[i, 'Location_int'],
                  tooltip = f"Facility: {fac} Phone: {phone}"
                 ).add_to(mymap)

mymap.save('covid_maps/index.html')