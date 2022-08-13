# Creates track images with color time gradient
# Author: Aroshi Ghosh (7/2022)



import pandas as pd
from shapely.geometry import Point
import geopandas as gpd
from geopandas import GeoDataFrame
import matplotlib.pyplot as plt
import sys, os, os.path, glob, csv
from numpy import nan
from datetime import datetime

def get_type(item):
    if item in range(1,21) or item in range(23,30) or item in range(33, 35) or item in range(38, 52) or item in range(53, 60) or item in range(90, 1001) or item in range(1005, 1012) or item == 1018 or item == 1022:
        return "Other"
    elif item in range(21, 23) or item in range (31, 33) or item == 53 or item == 1023 or item == 1025:
        return "Tug Tow"
    elif item == 30 or item in range(1001, 1003):
        return "Fishing"
    elif item == 35 or item == 1021:
        return "Military"
    elif item in range(36, 38) or item == 1019:
        return "Pleasure Craft/Sailing"
    elif item in range(60, 70) or item in range(1012, 1016):
        return "Passenger"
    elif item in range(70, 80) or item in range(1003, 1005) or item == 1016:
        return "Cargo"
    elif item in range(80, 90) or item == 1017 or item == 1024:
        return "Tanker"
    else:
        return "Unknown"



xfilenames = glob.glob('data/tracks/track*.csv')

for xfilename in xfilenames:
    filename = xfilename[12:len(xfilename)-4]
    print(filename)
    df = pd.read_csv(xfilename)
    try:
        filename = xfilename[12:len(xfilename)-4]
        print(filename)
        df = pd.read_csv(xfilename)
        df.columns = ['Time', 'Latitude', 'Longitude', 'Type']

        geometry = [Point(xy) for xy in zip(df['Longitude'],df["Latitude"])]
        gdf = GeoDataFrame(df, geometry=geometry)

        world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))
        ax=world.plot(figsize=(10, 10))
	
        df2 = pd.read_csv('sorted_portsdata.csv')
        df2.columns = ['Name', 'Latitude', 'Longitude']

        geometry2 = [Point(xy) for xy in zip(df2['Longitude'],df2["Latitude"])]
        gdf2 = GeoDataFrame(df2, geometry=geometry2)
        c = df['Time']

        #Set US Bounds
        ax.set_xlim(-130.42046, -67.06235)
        ax.set_ylim(13.554770000000001, 60.68005)
        print("test 1")
        print(get_type(df['Type'][0]))
        plt.title(filename[6:] + "   Ship Type: " + get_type(df['Type'][0]) + "\n   Time Period: " + str(datetime.fromtimestamp(df['Time'][0])) + " - " + str(datetime.fromtimestamp(df['Time'][len(df['Time'])-1]))) 

        ax2 = gdf2.plot(ax=ax, marker='o', color='cyan', markersize=20)
        #for item in df2.index:
        #    x = df2['Longitude'][item]
        #    y = df2['Latitude'][item]
        #    label = df2['Name'][item]
        #    ax2.annotate(label, xy=(x, y), xytext=(3, 3), textcoords="offset points")
        gdf.plot(column=c, ax=ax2, marker='o', c=c, cmap="gnuplot", markersize=1, legend=True, legend_kwds={'label': 'Time Period', 'orientation': 'horizontal'})
        plt.savefig('Track Images\\Set US Bounds\\' + filename + ".jpg")



        # Used to find the numerical bounds of the US
        minx, miny, maxx, maxy = gdf.total_bounds
        try:
            ax.set_xlim(minx-0.1, maxx+0.1)
            ax.set_ylim(miny-0.1, maxy+0.1)
            plt.title(filename[6:] + "   Ship Type: " + get_type(df['Type'][0]) + "\n   Time Period: " + str(datetime.fromtimestamp(df['Time'][0])) + " - " + str(datetime.fromtimestamp(df['Time'][len(df['Time'])-1])))
            ax2 = gdf2.plot(ax=ax, marker='o', color='cyan', markersize=20)
            #for item in df2.index:
                #x = df2['Longitude'][item]
                #y = df2['Latitude'][item]
                #label = df2['Name'][item]
                #ax2.annotate(label, xy=(x, y), xytext=(3, 3), textcoords="offset points")
            gdf.plot(column=c, ax=ax2, marker='o', c=c, cmap="gnuplot", markersize=1)
            plt.savefig('Track Images\\Zoomed Graphs\\' + filename + ".jpg")
            print("success!")
        except:
            print("failed")
    except:
        print("failed")
