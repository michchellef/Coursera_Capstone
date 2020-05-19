#!/usr/bin/env python
# coding: utf-8

# # Segmenting and Clustering Neighborhoods in Toronto

# ## Part 1: Importing Neighbourhood Data from Wikipedia
# 
# In this section, I scrape the wikipedia page 'List of postal codes of Canada: M' (https://en.wikipedia.org/wiki/List_of_postal_codes_of_Canada:_M) to get Toronto postal code, borough, and neighbourhood data into a Pandas dataframe.

# First, need to import pandas:

# In[1]:


import pandas as pd
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)


# The wikipedia page contains several tables. We are only interested in the first one, which I assign to a pandas dataframe and preview the dataframe:

# In[2]:


wiki = 'https://en.wikipedia.org/wiki/List_of_postal_codes_of_Canada:_M'
df = pd.read_html(wiki, header=0)[0]
df.head(10)


# We are only interested in processing cells that have an assigned borough. Removing rows with unassigned boroughs:

# In[3]:


df = df[df.Borough != 'Not assigned']
df.head(10)


# Number of rows in the dataframe: 

# In[4]:


print('The number of rows in the dataframe is', df.shape[0])


# Therefore we are dealing with 103 neighbourhoods in Toronto.

# ## Part 2: Importing Latitude and Longitude Data

# Importing the latitude and longitude data for each neighbourhood into a pandas dataframe from csv file: http://cocl.us/Geospatial_data:

# In[5]:


geo_url = 'http://cocl.us/Geospatial_data'
geo_df = pd.read_csv(geo_url)
geo_df.head(10)


# Set indices to 'Postal Code' for both dataframes to allow for merging:

# In[6]:


geo_df = geo_df.set_index('Postal Code')
df = df.set_index('Postal Code')


# Concatenate the two dataframes into a new dataframe:

# In[7]:


all_df = pd.concat([df, geo_df], axis=1, join='outer', sort=False)
all_df.head(10)


# Reset index of the new dataframe and recover 'Postal Code' column title:

# In[8]:


all_df.reset_index(inplace=True)
all_df.rename(columns={'index': 'Postal Code'},inplace=True)
all_df.head(10)


# ## Part 3: Clustering Toronto Neighbourhoods

# For the purpose of clutering, I will focus only on boroughs that contain the word 'Toronto'. Therefore I will create a new dataframe containing  neighbourhoods corresponding only to these boroughs:

# In[24]:


neighborhoods = all_df[all_df['Borough'].astype(str).str.contains('Toronto')]
neighborhoods


# Importing relevant dependencies:

# In[17]:


import numpy as np # library to handle data in a vectorized manner

#!pip install geopy
from geopy.geocoders import Nominatim # convert an address into latitude and longitude values

# Matplotlib and associated plotting modules
import matplotlib.cm as cm
import matplotlib.colors as colors

# import k-means from clustering stage
from sklearn.cluster import KMeans

#!pip install folium==0.5.0
import folium # map rendering library

print('Libraries imported.')


# Obtaining latitude and longitude coordinates of Toronto for mapping:

# In[18]:


address = 'Toronto, Ontario'

geolocator = Nominatim(user_agent="to_explorer")
location = geolocator.geocode(address)
latitude = location.latitude
longitude = location.longitude
print('The geograpical coordinate of Toronto are {}, {}.'.format(latitude, longitude))


# #### Creating a map of Toronto with neighborhoods superimposed:

# In[25]:


# create map of Toronto using latitude and longitude values
map_toronto = folium.Map(location=[latitude, longitude], zoom_start=10)

# add markers to map
for lat, lng, borough, neighborhood in zip(neighborhoods['Latitude'], neighborhoods['Longitude'], neighborhoods['Borough'], neighborhoods['Neighborhood']):
    label = '{}, {}'.format(neighborhood, borough)
    label = folium.Popup(label, parse_html=True)
    folium.CircleMarker(
        [lat, lng],
        radius=5,
        popup=label,
        color='blue',
        fill=True,
        fill_color='#3186cc',
        fill_opacity=0.7,
        parse_html=False).add_to(map_toronto)  
    
map_toronto


# ### Clustering Neighborhoods by Borough

# Cluster the neighbourhoods into boroughs, creating separate dataframes for each borough:

# In[53]:


downtown_toronto = neighborhoods[neighborhoods['Borough']=='Downtown Toronto']
central_toronto = neighborhoods[neighborhoods['Borough']=='Central Toronto']
west_toronto = neighborhoods[neighborhoods['Borough']=='West Toronto']
east_toronto = neighborhoods[neighborhoods['Borough']=='East Toronto']


# #### Creating a map of Toronto with neighborhoods superimposed, coloured by borough:

# In[58]:


# create map of Toronto using latitude and longitude values
map_toronto = folium.Map(location=[latitude, longitude], zoom_start=12)

# add dt Toronto markers to map
for lat, lng, borough, neighborhood in zip(downtown_toronto['Latitude'], downtown_toronto['Longitude'], downtown_toronto['Borough'], downtown_toronto['Neighborhood']):
    label = '{}, {}'.format(neighborhood, borough)
    label = folium.Popup(label, parse_html=True)
    folium.CircleMarker(
        [lat, lng],
        radius=5,
        popup=label,
        color='blue',
        fill=True,
        fill_color='#3186cc',
        fill_opacity=0.7,
        parse_html=False).add_to(map_toronto)  
    
for lat, lng, borough, neighborhood in zip(central_toronto['Latitude'], central_toronto['Longitude'], central_toronto['Borough'], central_toronto['Neighborhood']):
    label = '{}, {}'.format(neighborhood, borough)
    label = folium.Popup(label, parse_html=True)
    folium.CircleMarker(
        [lat, lng],
        radius=5,
        popup=label,
        color='red',
        fill=True,
        fill_color='red',
        fill_opacity=0.7,
        parse_html=False).add_to(map_toronto)  

for lat, lng, borough, neighborhood in zip(west_toronto['Latitude'], west_toronto['Longitude'], west_toronto['Borough'], west_toronto['Neighborhood']):
    label = '{}, {}'.format(neighborhood, borough)
    label = folium.Popup(label, parse_html=True)
    folium.CircleMarker(
        [lat, lng],
        radius=5,
        popup=label,
        color='green',
        fill=True,
        fill_color='green',
        fill_opacity=0.7,
        parse_html=False).add_to(map_toronto)  
    
for lat, lng, borough, neighborhood in zip(east_toronto['Latitude'], east_toronto['Longitude'], east_toronto['Borough'], east_toronto['Neighborhood']):
    label = '{}, {}'.format(neighborhood, borough)
    label = folium.Popup(label, parse_html=True)
    folium.CircleMarker(
        [lat, lng],
        radius=5,
        popup=label,
        color='purple',
        fill=True,
        fill_color='purple',
        fill_opacity=0.7,
        parse_html=False).add_to(map_toronto)
    
map_toronto


# In[ ]:


#kclusters = 5
#k_means = KMeans(init="k-means++", n_clusters=kclusters, n_init=12)
#X = neighborhoods.values[:,4:6]
#boroughs = pd.get_dummies(neighborhoods[['Borough']], prefix="", prefix_sep="")

