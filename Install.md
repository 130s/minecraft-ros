# Introduction #

This page outlines the instructions for installing the minecraft-ros package.

# Details #

## Prerequistes ##

**ROS**: This package assumes that you've already got ROS running.  If not, you probably won't find this program useful.  If you really want to get started with ROS, [ROS installation instructions can be found here](http://www.ros.org/wiki/ROS/Installation).

**Minecraft**: Minecraft must have been run from this account.  (The minecraft level files get copied to ~/.minecraft/saves)  [Minecraft can be downloaded here.](https://minecraft.net/download)

## download minecraft\_ros (this package) ##
```
roscd
git clone https://code.google.com/p/minecraft-ros/ minecraft_ros
chmod +x minecraft_ros/src/*.py
chmod +x minecraft_ros/src/pymclevel/*.py
```
## install octomap ##
It is possible that installing the ROS package is sufficient:
```
sudo apt-get install ros-groovy-octomap
```
But I got it from the git repo:
```
roscd
git clone git://github.com/OctoMap/octomap.git
cd octomap
mkdir build
cd build
cmake ..
make
sudo make install
```
## install pymcedit ##
```
roscd
cd minecraft_ros
cd src
git clone git://github.com/mcedit/pymclevel.git
```
## build this package ##
```
roscd
cd minecraft_ros
mkdir build
cd build
cmake ..
make
```

Next: [Converting a 2d map to minecraft](map_2d_2_minecraft.md)