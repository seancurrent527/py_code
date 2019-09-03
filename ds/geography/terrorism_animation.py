'''
terrorism_animation.py
Sean Current
Produces an animation showing terrorism activity over time, from 1970 to 2018.
ISTA 131 Final Project
'''

import pandas as pd, numpy as np
import matplotlib.pyplot as plt
from matplotlib import animation
import matplotlib.colors as colors
import geopandas

def clean_file():
    files = [f + '.csv' for f in 
         ['globalterrorismdb_0718dist']]   
    with open('cleanterror.csv', 'w') as ftw:
        for f in files:
            with open(f, 'r') as ftr:
                for line in ftr:
                    for ch in line:
                        ch = ord(ch)
                        if (ch < 32 or ch > 126) and ch not in [10, 13]:
                            line = line.replace(chr(ch), '')
                    ftw.write(line)
                    
def get_data():
    df = pd.read_csv('cleanterror.csv', usecols = range(15), index_col = 0, dtype = str)
    df = df[df['imonth'] != '0'][df['iday'] != '0']
    df.rename(columns = {'iyear':'year', 'imonth':'month', 'iday':'day'}, inplace = True)
    df['date'] = pd.to_datetime(df[['year', 'month', 'day']])
    return df                    
                    
def world_grid(df): #for new_terror
    df = (df - 180) * -1
    world = np.full((260, 360), 0.01)
    for ev in df.index:
        world[300 - df.loc[ev, 'latitude'], 360 - df.loc[ev, 'longitude']] += 1
    return world                    
                    
def new_terror(df): #I LIKE THIS ONE    
    df = df[abs(df['longitude']) <= 180][abs(df['latitude']) <= 180]
    plotting = df.loc[:, ['year','longitude','latitude']].dropna().astype(int)
    years = [plotting[plotting['year'] == yr] for yr in range(1969,2019) if yr != 1993]
    plot_yrs = [world_grid(yr) for yr in years]
    fig = plt.figure()
    
    def update(n):
        world = plt.pcolormesh(plot_yrs[n], cmap = 'inferno', norm = colors.LogNorm())#, shading = 'gouraud')
        return world, 

    plt.title('Terrorism over Time (1970-2018)')
    plt.xlabel('Longitude'), plt.ylabel('Latitude')
    plt.xticks([]), plt.yticks([])
    anim = animation.FuncAnimation(fig, update, frames = 49, blit = True, interval = 100)
    anim.save('new_terror.html', fps = 10, extra_args = ['-vcodec', 'libx264'])

def choropleth_data(data):
    world = geopandas.read_file(geopandas.datasets.get_path('naturalearth_lowres'))
    for yr in (yr for yr in range(1969,2019) if yr != 1993):
        world[str(yr)] = pd.Series(0)
        

#=======================================================================================    
def main():
    '''
    clean_file()
    df = get_data()
    df.to_csv('globalterror.csv')
    '''
    
    df = pd.read_csv('globalterror.csv')
    new_terror(df)
    plt.show()
                    
if __name__ == '__main__':
    main()                 