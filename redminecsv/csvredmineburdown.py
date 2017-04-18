#!/usr/bin/python3
import sys
import optparse
import csv
import json
import matplotlib.pyplot as plt
from matplotlib import cm
import matplotlib.dates as mdates
from matplotlib.ticker import FixedLocator
import numpy as np
import datetime

import sprintstats as ST
import csvredmineparser as CRP
import sprintstatsplot as STP


def main(csv_file,startDate,endDate,holidayDates,title,endDay):
    sprintST = ST.SprintStats()
    sprintST.startDate = startDate
    sprintST.endDate = endDate
    sprintST.festivos = holidayDates
    sprintST.title = title;
    sprintST = CRP.load_from_csv(csv_file,sprintST);
    print(sprintST.toDict())
    STP.plot_stats(sprintST,endDay)

def parse_arguments(argv):
  parser = optparse.OptionParser();
  parser.add_option("-f","--f",help="Location of csv file",default=None,dest = "filename");
  parser.add_option("-s","--start",help="Provide start date of this sprint, format: 20170315",default=None,dest="start")
  parser.add_option("-e","--end",help="Provide end date of this sprint,format: 20170315",default=None,dest="end")
  parser.add_option("-n","--nowork",help="Provide holidays in this spring,format: 20170315 (multiple can be provided)",action="append",dest="holidays",default=[])
  parser.add_option("-t","--title",help="Sprint title",default="Sprint",dest="title")
  parser.add_option("-r","--result",help="Indicate today is the end of hte last day, generate the result",dest="endDay",action="store_true",default=False)
  options,args = parser.parse_args(argv);
  if options.filename is None:
    print("Please provide redmine csv file");
    parser.print_help();
    exit(1);
  return options;


if __name__ == "__main__":
    options=parse_arguments(sys.argv)
    sys.exit(main(options.filename,options.start,options.end,options.holidays,options.title,options.endDay));
