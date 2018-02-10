
# coding: utf-8

# # Visualizing Map Data with Geopandas
# 
# There are several python packages that plot geographical data. In this example, we will be using [geopandas](http://geopandas.org/), because of its simplicity and its relation to `pandas`.
# 
# The data used in this example is provided by the US 2010 Census, and is hosted on the [US Census Bureau](https://www2.census.gov/) website.

# ### Importing Python Packages
# 
# These packages are required for the following program to run. If unavailable, you can install them via `pip install <package-name>`.

# In[1]:


import requests
import matplotlib.pyplot as plt
import geopandas as gpd


# ### Downloading Data
# 
# This script downloads the file from `url`, saves it in the current directory, and loads the shapefile with `geopandas`.

# In[2]:


url = 'http://www2.census.gov/geo/tiger/TIGER2010DP1/State_2010Census_DP1.zip'
file_name = 'State_2010Census_DP1.zip'


# In[3]:


r = requests.get(url)
with open(f'{file_name}', 'wb') as f:
    f.write(r.content)

data = gpd.read_file(f"zip://{file_name}")


# ### Viewing Data
# 
# `data.head()` displays the first five rows of the attribute table. The column names can be a bit criptic, but a good description can be found [here](http://magic.lib.uconn.edu/magic_2/vector/37800/demogprofilehousect_37800_0000_2010_s100_census_1_t.htm).
# 
# In this program we only care about:
#     * ALAND10: number of square meters of land per state
#     * DP0010001: population in the state

# In[4]:


data.head()


# ### Plotting the Default Map
# 
# First, lets clean up the data a bit to make the visualization cleaner.

# In[5]:


data = data.drop([17]) # delete alaska
data = data.drop([34]) # delete hawaii
data = data.drop([7])  # delete puerto rico


# This plots the raw map without the previous changes.

# In[18]:


plot_size = (25,10)
data.plot(figsize=plot_size)


# ### Manipulating Data
# 
# Here we create a new row of the attribute table called `color` that is populated with the habitants per square kilometer. This value is then normalized to be plotted.

# In[7]:


pop_dens_list = list()

for idx, row in data.iterrows():
    people_per_square_mile = row['DP0010001'] / (row['ALAND10'] / 1000)
    pop_dens_list.append(people_per_square_mile)


# In[8]:


data['POPSQKM'] = pop_dens_list


# Matplotlib supports different colormaps, which can be found [here](https://matplotlib.org/examples/color/colormaps_reference.html).
# 
# The one below is an example of the possible colormaps that can be fed into `cmap`.
# 
# ![colormaps](https://matplotlib.org/mpl_examples/color/colormaps_reference_02.png)
# 
# And finally, we add a color bar to the map.

# In[32]:


vmin, vmax = round(min(pop_dens_list),2), round(max(pop_dens_list),2)

# plot the graph
ax = data.plot(column='POPSQKM', cmap='Wistia', scheme='quantiles', figsize=(plot_size))

# add colorbar
fig = ax.get_figure()
cax = fig.add_axes([0.8, 0.15, 0.015, 0.3])
sm = plt.cm.ScalarMappable(cmap='Wistia', norm=plt.Normalize(vmin=vmin, vmax=vmax))
sm._A = []
fig.colorbar(sm, cax=cax)

# add latitude and longitude lines
ax.grid('on', which='major', axis='x', linestyle='dashed', alpha=0.3)
ax.grid('on', which='major', axis='y', linestyle='dashed', alpha=0.3)

