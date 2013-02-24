#!/usr/bin/env python

# -*- coding: utf-8 -*-
"""
Created on Mon Feb 18 23:52:09 2013

@author: jfstepha
"""

# parts of this code borrowed from: 

# Minecraft save file creator from kinect images created by getSnapshot.py
#	By: Nathan Viniconis
#

# in it, he said: "You can use this code freely without any obligation to the original or myself"

from math import sqrt
import sys
from pymclevel import mclevel
from pymclevel.box import BoundingBox
import re
import argparse
import os
import yaml

# Possible blocks  in (Name, ID, (RGB1,RGB2,..),Data)
	#RGBs are used to color match. 
possibleBlocks = ( 	\
					("Smooth Stone", 1, (	\
						(125,125, 125),),0), \
					("Dirt", 3, (	\
						(133,96,66),),0), \
					("Cobblestone", 4, (	\
						(117,117,117),),0), \
					("Wooden Plank", 5, (	\
						(156,127,78),),0), \
					("Bedrock", 7, ( \
						(83,83,83),),0),	\
					#("Lava", 11, ( \
					#	(255,200,200),),0),	\
					("Sand", 12, (	\
						(217,210,158),),0), \
					("Gravel", 13, ( 	\
						(136, 126, 125),),0), \
					("Gold Ore", 14, (	\
						(143,139,124),),0),	\
					("Iron Ore", 15, (	\
						(135,130,126),),0),	\
					("Coal Ore", 16, (	\
						(115,115,115),),0),	\
					("Wood", 17, (	\
						(154,125,77),),0), \
					("Sponge", 19, (	\
						(182,182,57),),0), \
					#("Glass", 20, (	\
					#	(60,66,67),),0), \
					("White Wool", 35, (	\
						(221,221,221),),0),	\
					("Orange Wool", 35, (	\
						(233,126,55),),1),	\
					("Magenta Wool", 35, (	\
						(179,75,200),),2),	\
					("Light Blue Wool", 35, (	\
						(103,137,211),),3),	\
					("Yellow Wool", 35, (	\
						(192,179,28),),4),	\
					("Light Green Wool", 35, (	\
						(59,187,47),),5),	\
					("Pink Wool", 35, (	\
						(217,132,153),),6),	\
					("Dark Gray Wool", 35, (	\
						(66,67,67),),7),	\
					("Gray Wool", 35, (	\
						(157,164,165),),8),	\
					("Cyan Wool", 35, (	\
						(39,116,148),),9),	\
					("Purple Wool", 35, (	\
						(128,53,195),),10),	\
					("Blue Wool", 35, (	\
						(39,51,153),),11),	\
					("Brown Wool", 35, (	\
						(85,51,27),),12),	\
					("Dark Green Wool", 35, (	\
						(55,76,24),),13),	\
					("Red Wool", 35, (	\
						(162,44,42),),14),	\
					("Black Wool", 35, (	\
						(26,23,23),),15),	\
					("Gold", 41, (	\
						(249,236,77),),0), \
					("Iron", 42, (	\
						(230,230,230),),0),	\
					("TwoHalves", 43, (
						(159,159,159),),0),
					("Brick", 45, ( \
						(155,110,97),),0), \
					#("TNT", 46, ( \
					#	(200,50,50),),0), \
					("Mossy Cobblestone", 48, (	\
						(90,108,90),),0), \
					("Obsidian", 49, (	\
						(20,18,29),),0),	\
					("Diamond Ore", 56, (	\
						(129,140,143),),0), \
					("Diamond Block", 57, (	\
						(99,219,213),),0), \
					("Workbench", 58, (	\
						(107,71,42),),0), \
					("Redstone Ore", 73, (	\
						(132,107,107),),0),	\
					#("Ice", 79, (	\
					#	(125,173,255),),0),	\
					("Snow Block", 80, (	\
						(239,251,251),),0),	\
					("Clay", 82, (	\
						(158,164,176),),0),	\
					("Jukebox", 84, (	\
						(107,73,55),),0),	\
					("Pumpkin", 86, (	\
						(192,118,21),),0),	\
					("Netherrack", 87, (	\
						(110,53,51),),0),	\
					("Soul Sand", 88, (	\
						(84,64,51),),0),	\
					("Glowstone", 89, (	\
						(137,112,64),),0)	\
					)


# /////////////////////////////////////////////////////////////////////////////		
# Calculates distance between two HLS colors
# /////////////////////////////////////////////////////////////////////////////	
def getColorDist(colorRGB, blockRGB):
    # RGB manhatten distance
    return sqrt( pow(colorRGB[0]-blockRGB[0],2) + pow(colorRGB[1]-blockRGB[1],2) + pow(colorRGB[2]-blockRGB[2],2))
	
	
# /////////////////////////////////////////////////////////////////////////////		
# For a given RGB color, determines which block should represent it
# /////////////////////////////////////////////////////////////////////////////	
def getBlockFromColor(RGB):
    # find the closest color
    smallestDistIndex = -1
    smallestDist = 300000
    curIndex = 0
    for block in possibleBlocks:
        for blockRGB in block[2]:
            curDist = getColorDist(RGB, blockRGB)
            
            if (curDist < smallestDist):
                smallestDist = curDist
                smallestDistIndex = curIndex
                
        curIndex = curIndex + 1
    if (smallestDistIndex == -1):
        return -1
    return possibleBlocks[smallestDistIndex]


########################################################
########################################################
class Octomap2Minecraft():
########################################################
########################################################
    ##########################################
    def __init__(self):
    ##########################################
        self.min_x = 1e99
        self.min_y = 1e99
        self.min_z = 1e99
        self.max_x = -1e99
        self.max_y = -1e99
        self.max_z = -1e99
        self.size_x = 0
        self.size_y = 0
        self.size_z = 0
        self.resolution = 0
        
        self.settings = {}
        
    ###############################################
    def read_settings(self, filename):
    ###############################################
                
        defaults = { 
            "level_name" : "robot_octo",
            "origin_x" : 0,
            "origin_y" : 100,
            "origin_z" : 0,
            "spawn_x" : 246,
            "spawn_y" : 1,
            "spawn_z" : 77,
            "oversize" : 100,
            "clear_height" : 256,
            "base_item" : "3:0"}
            
        parser = argparse.ArgumentParser(description='Translate a ROS map to a minecraft world')
        parser.add_argument("--settings", default=filename, dest="filename")
        for setting in defaults.keys():
            parser.add_argument("--"+setting, dest=setting)
        
        args = parser.parse_args()
        
        print( "reading settings from %s" % args.filename)
            
        stream = open(args.filename)
        settings_file = yaml.load(stream)
       
        for setting in defaults.keys():
            if vars(args)[setting] == None:
                if setting in settings_file:
                    self.settings[ setting ] = settings_file[ setting ]
                else:
                    self.settings[ setting ] = defaults[ setting ]
            else:
                self.settings[ setting ] = vars(args)[setting]
                
        print( "settings: %s" % (str(self.settings)))

    ##########################################
    def check_empty(self):
    ##########################################
        retval = False
        if self.min_x == 1e99:
            print "no value for min_x found"
            retval = True
        if self.min_y == 1e99:
            print "no value for min_y found"
            retval = True
        if self.min_z == 1e99:
            print "no value for min_z found"
            retval = True

        if self.max_x == -1e99:
            print "no value for max_x found"
            retval = True
        if self.max_y == -1e99:
            print "no value for max_y found"
            retval = True
        if self.max_z == -1e99:
            print "no value for max_z found"
            retval = True

        if self.size_x == 0:
            print "no value for size_x found"
            retval = True
        if self.size_y == 0:
            print "no value for size_y found"
            retval = True
        if self.size_z == 0:
            print "no value for size_z found"
            retval = True
            
        if self.resolution == 0:
            print "no value for resolution found"
            retval = True
            
        return retval
        
        
    ##########################################
    def read_input(self):
    ##########################################
        print "starting"    
        firstline = True
        beforefirstblock = True
        linecount = 0

        print "opening file"
        for line in sys.stdin:
            if firstline:
                firstline = False
                if re.match("^#octomap dump", line)  :
                    print "first line found"
                else:
                    print "ERROR: First line is not ""#octomap dump"""
                    exit(-1)
                    
            if beforefirstblock:
                
                a = re.match("(\w+): x (-?\d+.\d+) y (-?\d+.\d+) z (-?\d+.\d+)", line)
                if a:
                    print("found values: %s" % str(a.groups()))
                    
                    if (a.groups()[0] == 'min'):
                        self.min_x = float(a.groups()[1])
                        self.min_y = float(a.groups()[2])
                        self.min_z = float(a.groups()[3])
                        
                    if (a.groups()[0] == 'max'):
                        self.max_x = float(a.groups()[1])
                        self.max_y = float(a.groups()[2])
                        self.max_z = float(a.groups()[3])

                    if (a.groups()[0] == 'size'):
                        self.size_x = float(a.groups()[1])
                        self.size_y = float(a.groups()[2])
                        self.size_z = float(a.groups()[3])
                
                a = re.match("resolution: (-?\d+.\d+)", line)
                if a:
                    print("found resolution: %s" % str(a.groups()))                    
                    self.resolution = float(a.groups()[0])
                    
                        
                if re.match("^block", line):
                    if self.check_empty():
                        print "ERROR: not all values found!"
                        exit(-1)
                    self.init_map()
                    beforefirstblock = False
                    
            if beforefirstblock == False:
                a = re.match("block (-?\d+.?\d*) (-?\d+.?\d*) (-?\d+.?\d*) \((\d+) (\d+) (\d+)\) (-?\d+.?\d*)", line)
                if a:
                    linecount += 1
                    if linecount % 1000 == 0 :
                        print "processed %d lines" % linecount
                    self.add_block(a.groups())
                else:
                    print "ERROR: line improperly formed: %s" % line

        print("saving map")
        self.level.saveInPlace()      
                    

    ###############################################
    def readBlockInfo(self, keyword):
    ###############################################
        blockID, data = map(int, keyword.split(":"))
        blockInfo = self.level.materials.blockWithID(blockID, data)
        return blockInfo
        
    ###############################################
    def create_map(self):
    ###############################################
        if (os.path.exists( self.settings["level_name"])) :
            print("ERROR: %s directory already exists.  Delete it or pick a new name" % self.settings["level_name"])
            sys.exit()
        if (os.path.exists( os.getenv("HOME") + "/.minecraft/saves/" + self.settings["level_name"])) :
            print("ERROR: Minecraft world %s already exists.  Delete it (at ~/.minecraft/saves/%s) or pick a new name" % (self.settings["level_name"], self.settings["level_name"]))
            sys.exit()
        print("creating map file")
        os.system("pymclevel/mce.py " + self.settings["level_name"] + " create")

    ###############################################
    def init_map(self):
    ###############################################
        filename = self.settings["level_name"]
        self.level = mclevel.fromFile(filename)
        self.level.setPlayerGameType(1, "Player")
        pos = [self.settings["spawn_x"], self.settings["spawn_y"], self.settings["spawn_z"]]
        
        self.level.setPlayerPosition( pos  )
        self.level.setPlayerSpawnPosition( pos )
        
        rows = self.size_x / self.resolution
        cols = self.size_y / self.resolution
        
        o_x = self.settings["origin_x"]
        o_y = self.settings["origin_y"]
        o_z = self.settings["origin_z"]
        ovs = self.settings["oversize"]
        
        box = BoundingBox( (o_x - ovs, o_y, o_z - ovs ), 
                          ( rows + ovs * 2, ovs, cols + ovs * 2))
        
        print("creating chunks")          
        chunksCreated = self.level.createChunksInBox( box )
        print("Created %d chunks" % len( chunksCreated ) )
        
        print("filling air")
        self.level.fillBlocks( box, self.level.materials.blockWithID(0,0) )
        print("filled %d blocks" % box.volume )
        
        print("filling base layer")
        box = BoundingBox( (o_x - ovs, o_y - 10, o_z - ovs ), 
                          ( rows + ovs * 2, 10, cols + ovs * 2))
        item = self.readBlockInfo( self.settings["base_item"] )
        self.level.fillBlocks( box, item )
        print("filled %d blocks" % box.volume )
        
    ###############################################
    def add_block(self, blk):
    ###############################################
        
        o_x = self.settings["origin_x"]
        o_y = self.settings["origin_y"]
        o_z = self.settings["origin_z"]

        blk_size = float(blk[6]) / self.resolution        
        
        x1 = (self.max_x - float(blk[0])) / self.resolution + o_x
        y1 = (float(blk[1]) - self.min_y) / self.resolution + o_y
        z1 = (float(blk[2]) - self.min_z) / self.resolution + o_z
        
        r = (int(blk[3]))
        g = (int(blk[4]))
        b = (int(blk[5]))
        
        box = BoundingBox( ( x1, y1, z1 ), (blk_size, blk_size, blk_size) )
        
        closest_block = getBlockFromColor( ( r,g,b))
        blockID = closest_block[1]
        data = closest_block[3]
        item = self.level.materials.blockWithID(blockID, data)
        
        self.level.fillBlocks( box, item )


        
if __name__ == "__main__":
    o = Octomap2Minecraft()
    o.read_settings("map_octo.yaml")
    o.create_map()
    o.read_input()





































































