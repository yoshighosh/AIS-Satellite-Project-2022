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

> **histcol.py** -- *Utility file*

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
Files Used
> **graphics_code_color.py** -- *Plots tracks with a time gradient and key*

To download the packages need for graphics, run the following lines of code (assuming you have Anaconda Package Distributer)
```
conda config --prepend channels conda-forge
conda create -n geo --strict-channel-priority geopandas jupyterlab
```
If this does not work, follow the instructions in this article: https://geoffboeing.com/2014/09/using-geopandas-windows/
After installing the packages, activate the environment and run the code using the following lines of code:
```
conda activate geo
python graphics_code_color.py
```
NOTE: Do NOT try to install geopandas using pip, it does not download all of the neccessary dependencies


## WEKA
Files Used
> **metadata.csv** -- *Stores all the metadata for the ships*

> **delimited_to_weka.py** -- *Converts CSV into ARFF file*

> **metadata_table_values.txt** -- *Stores the names of all the metadata columns in order*

In order to convert **metadata.csv** into an ARFF file, use excel to delete all (, ), %, ', " and replace all spaces with _ . Additionally, fill all blank cells with 0 or N/A depending on the attribute type. Then run the following code in the CMD prompt.
```
python delimited_to_weka.py "metadata.csv" "," ship_key numeric_ship_type string_ship_type type_of_ID ratio_of_time_moving num_line_segments avg_speed std_dev_speed num_accel_points length_ship width_to_length_ratio numeric_cargo_type receiver_class num_neighbors ratio_displacement_to_distance
```
Then upload the resulting ARFF file into WEKA Explorer to create models. Remove ```ship_key``` and any other columns deemed unneccessary. Make sure to test models using the correct column as the class variable (ship type, receiver class, etc).


## Creating a Coincidence Matrix
> **get_coincidence_matrix.py**

> **get_top_coincidences.py**



## Miscellaneous Files
Files Used
> **get_test_tracks.py** -- *Creates a copy of every 10th track in a separate directory*

> **find_redundant_tracks.py** -- *Return a list of track names that are subsets of other names*

> **barplot.py** -- *Create histogram of the ship type*

> **combine_cols_AIS.py** -- *Extracts a given column from all 7 raw data files and outputs the values into a CSV files*

> **find_faulty_transponders.py** -- *Makes a list of ship keys that have no track data*

> **quickstats_col** -- *Calculates the mean, standard deviation, max, and min for given metadata column*

> **get_sizes_versus_types.py** -- *Creates a table of ship types and their average size*
