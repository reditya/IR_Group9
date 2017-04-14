## Purpose
Folder used to make all the tests before integrating them into the final application: clustering and visualisation.

## File description
These first files contain the python functions used to generate geojson files to visualize.
- **show_cat.py**: python script to process the json files and output the geojson file to visualize. Depending on the input, yit returns clusters or heatmaps based on food catory or food term.
- **list_function.py**: File containing the list of possible functions to use.
- **eval_test.py**: python script to perform grid search on the geoSOM clustering algorithm. Return plots of the different index measured.
These are examples of files to visualize (input within the javascript):
- **new_point.geojson**: geojson file created after executing the scripts. 
- **new_poly.geojson**: geojson file created after executing the scripts. 
These are the data files required to run the scripts:
- **food_category.csv**: File containing the association of retrieved food terms and their categories.
- **instagram.json**: data file source for processing.
- ** food_term_cluster.py**: python script to get the geojson files containing only one food term.
- **category.html**: main html file to open in the browser.

Required javascript libraries and the javascript code:
- **/Leaflet.heat-gh-pages**: Folder containing files to create the heatmap.
- **leaflet-heat.js**: leaflet heatmap library.
- **/leaflet**: Folder containing the leaflet library files.
- **/javascript**: Folder containing javascript files to show the map, heatmap, cluster, and help button.


- **/old_files**: Folder containing python script previously used to test clustering algorithms such as Max-p.
For example, 
-  **json_resto_to_geoson_fours.py**: python script to transform json to geojson for Foursquare.
- **json_to_geo_tweets_and_insta.py**: python script to transform json to geojson for Instagram and Twitter.
- **/map_test**: Folder containing example shapefile created during the script running.

- **all_restaurants_test.json**: example of json file containing the list of restaurants from Foursquare (can be shown on the map).
- **all_resto_geojson.geojson**: example trasnsformed json to geojson file to show on the map.

- **food_term.txt**: file showing the frequency of each food term retrieved.

- **jquery-2.1.1.min.js**: jquery library.
