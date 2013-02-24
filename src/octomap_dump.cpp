/*
 * OctoMap - An Efficient Probabilistic 3D Mapping Framework Based on Octrees
 * http://octomap.github.com/
 *
 * Copyright (c) 2009-2013, K.M. Wurm and A. Hornung, University of Freiburg
 * All rights reserved.
 * License: New BSD
 *
 * Redistribution and use in source and binary forms, with or without
 * modification, are permitted provided that the following conditions are met:
 *
 *     * Redistributions of source code must retain the above copyright
 *       notice, this list of conditions and the following disclaimer.
 *     * Redistributions in binary form must reproduce the above copyright
 *       notice, this list of conditions and the following disclaimer in the
 *       documentation and/or other materials provided with the distribution.
 *     * Neither the name of the University of Freiburg nor the names of its
 *       contributors may be used to endorse or promote products derived from
 *       this software without specific prior written permission.
 *
 * THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
 * AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
 * IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
 * ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE
 * LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
 * CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
 * SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
 * INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
 * CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
 * ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
 * POSSIBILITY OF SUCH DAMAGE.
 */

#include <octomap/octomap.h>
#include <octomap/OcTree.h>
#include <string.h>
#include <octomap/ColorOcTree.h>


using namespace std;
using namespace octomap;

void printUsage(char* self){
  std::cerr << "\nUSAGE: " << self << " input.ot [ depth ] [> output.txt ]\n\n";

  std::cerr << "This tool will convert the occupied voxels of a binary OctoMap \n"
      << "file input.ot to a script for minecraft.  The optional depth"
      << "parameter specifies a maximum depth to traverse the tree.\n\n";

  std::cerr << "WARNING: The output files will be quite large!\n\n";

  exit(0);
}

int main(int argc, char** argv) {
    
  string scriptFilename = "";
  string otFilename = "";

  if ( (argc != 2 && argc != 3) || (argc > 1 && strcmp(argv[1], "-h") == 0)){
    printUsage(argv[0]);
  }

  otFilename = std::string(argv[1]);
  int depth=0;
  if (argc > 2) {
     depth = strtol(argv[2], NULL, 10);
  }
    
  std::ifstream infile(otFilename.c_str(), std::ios_base::in |std::ios_base::binary);
  if (!infile.is_open()) {
    cout << "file "<< otFilename << " could not be opened for reading.\n";
    return -1;
  }
    //OcTree tree (0.1);  // create empty tree with resolution 0.1
  AbstractOcTree* read_tree = AbstractOcTree::read(otFilename);
  ColorOcTree* tree = dynamic_cast<ColorOcTree*>(read_tree);
  cerr << "opened file" << endl;
  cerr << "creating tree" << endl;
  cerr << "color tree read from "<< otFilename <<"\n"; 
  
  cerr << "walking the tree to get resolution " << endl;

  double res = 999;
  for(ColorOcTree::leaf_iterator it = tree->begin( depth ), end=tree->end(); it!= end; ++it) {
  if(tree->isNodeOccupied(*it)){
      double size = it.getSize();
      if (size < res) {
         res = size;
      }
    }
  }

  cerr << "writing parameters" << endl;
  double min_x, min_y,min_z;
  double max_x, max_y,max_z;
  double size_x, size_y,size_z;
  
  tree->getMetricMin( min_x, min_y, min_z);
  cout << "#octomap dump\n";
  cout << "min: x " << min_x << " y " << min_y << " z " << min_z << endl;
  tree->getMetricMax( max_x, max_y, max_z);
  cout << "max: x " << max_x << " y " << max_y << " z " << max_z << endl;
  tree->getMetricSize( size_x, size_y, size_z);
  cout << "size: x " << size_x << " y " << size_y << " z " << size_z << endl;
  cout << "resolution: " << res << endl;
  
  size_t count(0);
  
  cerr << "dumping tree" << endl;
  // std::ofstream outfile (scriptFilename.c_str());
  for(ColorOcTree::leaf_iterator it = tree->begin( depth ), end=tree->end(); it!= end; ++it) {
  if(tree->isNodeOccupied(*it)){
      count++;
      double size = it.getSize();
      cout << "block "
          << it.getX() << " " 
          << it.getZ() << " "
          << it.getY() << " "
          << it->getColor() << " "
          << size << endl; 
    }
  }


}