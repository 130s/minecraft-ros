# Introduction #

The octomap\_2\_minecraft script, along with the octomap\_dump program will convert an octomap into a Minecraft map.

<img src='https://minecraft-ros.googlecode.com/files/kitchen.jpg' height='200' width='250'> --> <img src='https://minecraft-ros.googlecode.com/files/octomap_kitchen.jpg' height='200' width='250'>

<h1>Example usage</h1>

First, obtain an octomap.  The ccny_rgbd stack will allow you to generate and save octomap data with a Kinect.  The instructions for running the stack are found <a href='http://www.ros.org/wiki/ccny_rgbd/keyframe_mapper'>on the ccny_rgbd ROS wiki</a>.  Use the save_octomap service to save the octomap.<br>
<br>
Use the octovis tool to check out the octomap before converting it.  You can also use this to see what level of the octomap tree you would like to convert.  Convertig to a larger depth will make a higher resolution map, but it will turn out bigger in minecraft.<br>
<br>
The conversion happens in 2 steps.  First dump the octomap to a text file<br>
<pre><code>roscd<br>
cd minecraft_ros<br>
../octomap_dump myoctomapfile.ot &gt; mymap.dump<br>
</code></pre>

Then convert that dump file into a minecraft map.<br>
<br>
<pre><code>./octomap_2_minecraft.py &lt; mymap.dump<br>
</code></pre>

This will create the minecraft world as a subdirectory of the current directory then move it to ~/.minecraft/saves.<br>
<br>
<h1>Parameters</h1>
<pre><code># the output monecraft world name<br>
level_name: robot_octo<br>
<br>
# The smallest x,y,z point of the octomap will be placed at<br>
# these coordinates of the minecraft world<br>
origin_x: 10<br>
origin_y: 1<br>
origin_z: 10<br>
<br>
# the player's spawn point'<br>
spawn_x: 0<br>
spawn_y: 4<br>
spawn_z: 0<br>
<br>
# how much of the minecraft world to clear around the octomap<br>
oversize: 100<br>
<br>
# the height of the world to clear above the octomap<br>
clear_height: 256<br>
</code></pre>