# AIS-Satellite-Project-2022
All code and data files for the NPS 2022 AIS Satellite project


## Preprocessing
Files used
> **extract_ship_key.py** -- *Given a line of raw AIS data in CSV format, construct a primary key for the ship using the IMO number, CALL sign, and MMSI mobile number*

> **sort_big.py** -- *Sort a large file by breaking it into pieces using the input file, partition size, and sorting type (int, str, float) as arguments, utility file*

> **splitmergeproc.py** -- *Generalized split-merging distributed processing, utility file*

> **copy_file_general.py** -- *Utility file*

> **cleanrawdata_tracks.py** -- *Apportions cleaned data to individual files for each ship key, the last part of cleanrawdata.py*

> **cleanrawdata.py** -- *Converts a raw AIS file into something sortable by ship ID and date*

> **find_track_delimitation_times.py** - *Finds places in each track where there is a time gap or change in velocity that exceeds a threshold*

> **get_average_sampling_gap.py** -- *Finds the average time gap and standard deviation in timestamps between successive records of a ship*

> **combine_metadata_files.py** -- *Utility file*

> **cleanrawdata_all.py** -- *Final preprocessing file that extracts cleaned tracks records for each ship*

To start preprocessing, run ```python cleanrawdata_all.py 'data'``` assuming 'data' is the folder with all original AIS zip files. Ensure that all files listed above are in the current directory and not in subdirectories.


## Metadata
Files used
> **extractcols.py** -- *Extracts columns from a CSV file into a new CSV file*

> **histcol.py**

> **extract_stated_speeds.py** -- *Extracts the speed reported by AIS into a txt file*

> **get_geo_hist.py** -- *Returns the number of ships that have entered a geo bin*

> **linear_fit_general.py** -- *Finds the line of best fit given a series of latitude and longitude points*

> **linear_fit_all.py** -- *Creates a series of line segments for a track record, storing the information in the output file*

> **logistic_function.py** -- *Runs data through a custom logistic function*

> **track_speed.py** -- *Creates a new file for each ship track with the time difference, distance traveled, and speed*

> **map_coords_to_latlong_bin_center.py** -- *Returns the center coordinates of a geobin given a set of coordinates and a granularity*

> **create_metadata.py** -- *Creates the final metadata file used in WEKA*

Prior to creating the metadata, make sure that you have fully run the preprocessing code as well as **extract_stated_speeds.py** and **get_geo_hist.py** with granularity of 1.0. To create the final metadata file, run ```python create_metadata.py 'data/tracks' 'output'``` assuming that your current directory has empty folders called firstTwoCols, track_avg_speed, and output. Additionally, 'data/tracks' should be the location of your track files. Ensure that all files listed above are in the current directory and not in subdirectories.


## Track Graphics




## Plots of Attributes




## WEKA
