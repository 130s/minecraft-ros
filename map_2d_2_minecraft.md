# Introduction #

The map\_2d\_2\_minecraft.py script will convert a 2D .pgm map file into a minecraft world.  The world file is copied into the ~/.minecraft/saves folder.

<img src='https://minecraft-ros.googlecode.com/files/map_whole_house_13_02_17_fixed.jpg' width='250' height='200' />  ----->   <img src='https://minecraft-ros.googlecode.com/files/minecraft_2d_map.png' width='250' height='200'>


The default arguments convert "mymap.pgm" into the minecraft world "robot_map", but these parameters can be specified at the command prompt, or in the map_2d.yaml file.<br>
<br>
<h1>Instructions</h1>

<pre><code>roscd<br>
cd minecraft_ros/src<br>
./map_2d_2_minecraft.py --map_file mymap.pgm --level_name mymap<br>
</code></pre>

<h1>Parameters</h1>

Any of these parameters can be overwritten at the command prompt using the format:<br>
<br>
<pre><code>./map_2d_2_minecraft.py --param_name param_value<br>
</code></pre>



<pre><code># The name of the level to be created<br>
level_name: robot_map<br>
<br>
# The occupancy threshold - any map value less thatn<br>
# this will be considered occupied.<br>
occ_thresh: 200<br>
<br>
# The empty theshold - any map value greater than this<br>
# will be considered empty.<br>
# Values between occ_thresh and empty_thresh are<br>
# unexplored.<br>
empty_thresh: 250<br>
<br>
# The input map file<br>
map_file: "mymap.pgm"<br>
<br>
# The block to be placed in empty regions.<br>
# Default: 12:0 - sand.<br>
empty_item: "12:0"<br>
<br>
# The height of the empty_items in the empty<br>
# regions.<br>
empty_height: 1<br>
<br>
# The block to be placed in occupied regions<br>
# Default: 5:0 - wooden planks<br>
occupied_item: "5:0"<br>
<br>
# The height of the blocks to be built in the occipied<br>
# regions.  Values of more than about 4 will build a <br>
# wall out of the map.<br>
occupied_height: 15<br>
<br>
# The item to be placed in unexplored regions of the map.<br>
# Default: 3:0 - dirt<br>
unexplored_item: "3:0"<br>
<br>
# The origin of the minecraft world.  This point will<br>
# correspond to 0,0 on the input map.<br>
origin_x: 0<br>
origin_y: 20<br>
origin_z: 0<br>
<br>
# The spawn point of the minecraft world.  This is<br>
# where the player is placed when entering the world,<br>
# or when re-spawning.<br>
spawn_x: 246<br>
spawn_y: 21<br>
spawn_z: 77<br>
<br>
# The size of the area to be cleared out around the map<br>
oversize: 100<br>
clear_height: 256<br>
<br>
# Setting do_ceilint to true will cause a ceiling to be built<br>
# on the map, at the height of the occupied item,<br>
# made out of the ceiling item.<br>
do_ceiling: false<br>
ceiling_item: "89:0"<br>
</code></pre>