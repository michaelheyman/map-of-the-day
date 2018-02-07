import requests
import matplotlib.pyplot as plt
import geopandas as gpd
from mpl_toolkits.axes_grid1 import make_axes_locatable


# ### Downloading Data
# 
# This script downloads the file from `url`, saves it in the current directory, and loads the shapefile with `geopandas`.

# In[2]:


#url = 'http://www2.census.gov/geo/tiger/TIGER2010DP1/State_2010Census_DP1.zip'
file_name = 'State_2010Census_DP1.zip'


## In[3]:


#r = requests.get(url)
#with open(f'{file_name}', 'wb') as f:
#    f.write(r.content)

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
# This plots the raw map without any changes.


plot_size = (50,20)

data = data.drop([17]) # delete alaska
data = data.drop([34]) # delete hawaii
data = data.drop([7])  # delete puerto rico


# The `normalize` function normalizes a list of numbers to between 0 and 1.


def normalize(lst):
    max_num = max(lst)
    min_num = min(lst)

    for idx, num in enumerate(lst):
        lst[idx] = (num - min_num) / (max_num - min_num)

    return lst


# ### Manipulating Data
# 
# Here we create a new row of the attribute table called `color` that is populated with the habitants per square kilometer. This value is then normalized to be plotted.

# In[7]:


pop_dens_list = list()

for idx, row in data.iterrows():
    people_per_square_mile = row['DP0010001'] / (row['ALAND10'] / 1000)
    pop_dens_list.append(people_per_square_mile)


# In[11]:


#pop_dens_list = normalize(pop_dens_list)
data['POPSQKM'] = pop_dens_list


# Matplotlib supports different colormaps, which can be found [here](https://matplotlib.org/examples/color/colormaps_reference.html).
# 
# The one below is an example of the possible colormaps that can be fed into `cmap`.
# 
# ![colormaps](https://matplotlib.org/mpl_examples/color/colormaps_reference_02.png)

#data.plot(column='POPSQKM', cmap='Wistia', scheme='quantiles', figsize=plot_size)

vmin, vmax = round(min(pop_dens_list),2), round(max(pop_dens_list),2)

ax = data.plot(column='POPSQKM', cmap='Wistia', scheme='quantiles', figsize=plot_size)

# add colorbar
fig = ax.get_figure()
cax = fig.add_axes([0.9, 0.272, 0.03, 0.446])
sm = plt.cm.ScalarMappable(cmap='Wistia', norm=plt.Normalize(vmin=vmin, vmax=vmax))
sm._A = []
fig.colorbar(sm, cax=cax)

plt.show()
