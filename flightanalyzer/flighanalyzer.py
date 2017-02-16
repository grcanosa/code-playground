#!/usr/bin/python3

import sys
import os


class FileAnalyzer:
  def __init__(self):
    self._path = "";
    self._file_level = 2; # Files are 2 levels below the given path
    self._data = {}; #Data is a dictionary
    self._analyzed_path = ""
    self._dest_path = ""
    #Parameters to look for in each file.
    #We the last one (in the order that they appear in this vector)
    #is found we stop searching that file.
    self._flight_file_param = ["TIMESTAMP","EVENT","EVENTCLASS","IFPLID","REGUL"]

  def analyze_path(self,path,dest_path):
    self._data = {}; # Clear the data before doing anything
    self.analyzed_path = path;
    self._dest_path = dest_path;
    self.process_dir(path, 0);


  def complete_full_data(self,flightdata):


  def move_file(self,filepath,flightdata):
    newfilepath = os.path.join(self._dest_path, flightdata["IFPLID"])
    newfilepath = os.path.join(newfilepath, os.path.basename(filepath))
    os.renames(filepath, newfilepath);

  def process_file(self,filepath):
    flightdata = {};
    with open(filepath,'r') as f:
      for l in f:
        for param in self._flight_file_param:
          if param in l:
            flightdata[param] = l.split()[1];
            break;
        if self._flight_file_param[-1] in flightdata:
          #Last parameter is found.
          break;

    self.move_file(filepath,flightdata);
    self.complete_full_data(flightdata);


  def process_dir(self,dirpath,level):
    for entry in os.listdir(dirpath):
      fullentrypath = os.path.join(dirpath, entry);
      if level == self._file_level: # WE SHOULD BE FINDING FILES:
        if os.path.isfile(fullentrypath):
          self.process_file(fullentrypath);
        else:
          print("ERR: Found non-file in file level: %s" % fullentrypath);
      else: # We are not yet in the file-level
        level += 1;
        self.process_dir(fullentrypath,level);


  def print_results(self):
    print("Printing results of analyzed path: %s" % self._analyzed_path)



def main(path,dest_path):
  fa = FileAnalyzer();
  fa.analyze_path(path,dest_path);
  fa.print_results();

def parse_arguments(args):
  parser = optparse.OptionParser();
  parser.add_option("--path",help="Path to the dates folders",default=None);
  parser.add_option("--dest_path",help="Path copy the files to",default=None);
  options,args = parser.parse_args(argv);
  if options.path is None or options.dest_path is None:
    print("Please provide paths");
    parser.print_help();
    exit(1);
  return options.path,options.dest_path;

if __name__ == "__main__":
  path,dest_path = parse_arguments(sys.argv);
  return main(path,dest_path)
