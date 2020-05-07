import pandas as pd
import geopandas as gpd
import numpy as np
import folium

geo_df = gpd.read_file('spatial_data/chicago zips.geojson')

df = pd.read_csv('analysis_data/analysis_data 2020-05-06.csv', dtype={'zip': str})

geo_df = geo_df.merge(df, on='zip')

geo_df = geo_df[(geo_df['fpc'] <= 1) & (geo_df['fpc'] > 0)]

# Boiler plate code for mapping

mymap = folium.Map(location=[41.8781, -87.623177], zoom_start=11,tiles=None)

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
        fields=['zip','interval_width'],
        aliases=['Zip Code: ','interval_width: '],
        style=("background-color: white; color: #333333; font-family: arial; font-size: 12px; padding: 10px;")
    )
)

mymap.add_child(zip_highlighter)

mymap.keep_in_front(zip_highlighter)

folium.LayerControl().add_to(mymap)

mymap.save('/Users/liam/covid_maps/index.html')
