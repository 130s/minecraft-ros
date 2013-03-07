#!/usr/bin/env python


import re
import numpy
import yaml
import sys
import argparse
try:
    from pymclevel import mclevel
    from pymclevel.box import BoundingBox
except:
    print ("\nERROR: pymclevel could not be imported")
    print (" Get it with git clone git://github.com/mcedit/pymclevel.git\n\n")
    raise
import os

############################################################################
############################################################################
class Map2d2Minecraft():
############################################################################
############################################################################
    ###############################################
    def __init__(self):
    ###############################################
        self.settings = {}

    ###############################################
    def readBlockInfo(self, keyword):
    ###############################################
        blockID, data = map(int, keyword.split(":"))
        blockInfo = self.level.materials.blockWithID(blockID, data)
        return blockInfo
        
    ###############################################
    def read_settings(self, filename):
    ###############################################
                
        defaults = { 
            "level_name" : "robot_map",
            "map_file" : "/home/jfstepha/ros_workspace/maps/map_whole_house_13_02_17_fixed.pgm",
            "occ_thresh" : 200,
            "empty_thresh" : 250,
            "empty_item" : "12:0",
            "empty_height" : 1,
            "occupied_item" : "5:0",
            "occupied_height" : 15,
            "unexplored_item" : "3:0",
            "origin_x" : 0,
            "origin_y" : 100,
            "origin_z" : 0,
            "spawn_x" : 246,
            "spawn_y" : 1,
            "spawn_z" : 77,
            "oversize" : 100,
            "clear_height" : 256,
            "do_ceiling" : True,
            "ceiling_item" : "89:0"}
            
        parser = argparse.ArgumentParser(description='Translate a ROS map to a minecraft world')
        parser.add_argument("--settings", default=filename, dest="filename")
        for setting in defaults.keys():
            parser.add_argument("--"+setting, dest=setting)
        
        args = parser.parse_args()
        
        print( "reading settings from %s" % args.filename)
        this_dir, this_file = os.path.split( os.path.realpath(__file__) )
        stream = open( os.path.join( this_dir, args.filename ) )
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

    ###############################################
    def do_convert(self, image):
    ###############################################
        filename = self.settings["level_name"]
        self.level = mclevel.fromFile(filename)
        self.level.setPlayerGameType(1, "Player")
        pos = [self.settings["spawn_x"], self.settings["spawn_y"], self.settings["spawn_z"]]
        
        self.level.setPlayerPosition( pos  )
        self.level.setPlayerSpawnPosition( pos )
        
        rows = image.shape[0]
        cols = image.shape[1]
        
        o_x = self.settings["origin_x"]
        o_y = self.settings["origin_y"]
        o_z = self.settings["origin_z"]
        ovs = self.settings["oversize"]
        
        box = BoundingBox( (o_x - ovs, o_y - ovs, o_z - ovs ), 
                          ( rows + ovs * 2, ovs * 2, cols + ovs * 2))
        
        print("creating chunks")          
        chunksCreated = self.level.createChunksInBox( box )
        print("Created %d chunks" % len( chunksCreated ) )
        
        print("filling air")
        self.level.fillBlocks( box, self.level.materials.blockWithID(0,0) )
        print("filled %d blocks" % box.volume )
        
        print("filling base layer")
        box = BoundingBox( (o_x - ovs, o_y - 10, o_z - ovs ), 
                          ( rows + ovs * 2, 10, cols + ovs * 2))
        item = self.readBlockInfo( self.settings["unexplored_item"] )
        self.level.fillBlocks( box, item )
        print("filled %d blocks" % box.volume )
        
        print("creating map")

        for r in range( rows ):


            print("  row %d / %d" % (r, rows) );
            
            for c in range( cols ):
                x = o_x + r
                y = o_y
                z = o_z + c
                
                if image[rows-r-1,c] > self.settings["empty_thresh"]:
                    item = self.readBlockInfo( self.settings["empty_item"])
                    self.level.setBlockAt(x,y,z, item.ID)
                    if self.settings["do_ceiling"] :
                        item = self.readBlockInfo( self.settings["ceiling_item"])
                        y2 = y + self.settings["occupied_height"]
                        self.level.setBlockAt(x,y2,z, item.ID)
                if image[rows-r-1,c] < self.settings["occ_thresh"]:
                    h = self.settings["occupied_height"]
                    item = self.readBlockInfo( self.settings["occupied_item"])
                    box = BoundingBox( (x,y,z),(1,h,1) )

                    self.level.fillBlocks( box, item )
        print("saving map")
        self.level.saveInPlace()                
                
        print("done")

    ###############################################
    def read_pgm(self, filename, byteorder='>'):
    ###############################################
        """Return image data from a raw PGM file as numpy array.

        Format specification: http://netpbm.sourceforge.net/doc/pgm.html

        """
        with open(filename, 'rb') as f:
            buffer = f.read()
        try:
            header, width, height, maxval = re.search(
                b"(^P5\s(?:\s*#.*[\r\n])*"
                b"(\d+)\s(?:\s*#.*[\r\n])*"
                b"(\d+)\s(?:\s*#.*[\r\n])*"
                b"(\d+)\s(?:\s*#.*[\r\n]\s)*)", buffer).groups()
        except AttributeError:
            raise ValueError("Not a raw PGM file: '%s'" % filename)
        return numpy.frombuffer(buffer,
                                dtype='u1' if int(maxval) < 256 else byteorder+'u2',
                                count=int(width)*int(height),
                                offset=len(header)
                                ).reshape((int(height), int(width)))
                                
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
    def move_map(self):
    ###############################################
        print("moving to minecraft saves")
        os.system("mv %s ~/.minecraft/saves/" % self.settings["level_name"])


if __name__ == "__main__":
    map2d2minecraft = Map2d2Minecraft()
    map2d2minecraft.read_settings("map_2d.yaml")
    image = map2d2minecraft.read_pgm(map2d2minecraft.settings["map_file"], byteorder='<')
    map2d2minecraft.create_map()
    map2d2minecraft.do_convert( image )
    map2d2minecraft.move_map()

