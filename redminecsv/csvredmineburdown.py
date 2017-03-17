#!/usr/bin/python3
import sys
import optparse
import csv
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.ticker import FixedLocator
import numpy as np
import datetime


def get_column_indexes(first_row):
    col_index = {}
    col_index["issue"] = 0;
    col_index["state"] = 1
    col_index["type"] = 3
    col_index["proyect"] = 2
    col_index["percentage"] = 12
    col_index["hours"] = 13
    for index,val in enumerate(first_row):
        if val == "#":
            col_index["issue"] = index;
        elif val == "Estado":
            col_index["state"] = index;
        elif val == "Proyecto":
            col_index["proyect"] = index;
        elif val == "Tipo":
            col_index["type"] = index;
        elif "Realizado" in val:
            col_index["percentage"] = index;
        elif val == "Tiempo estimado":
            col_index["hours"] = index;
    return col_index;

def fill_stats_from_row(col_index,row,stats):
    #print(row[col_index["proyect"]])
    finished = False;
    blocked = False;
    hours = float(row[col_index["hours"]].replace(",","."));
    percentage = float(row[col_index["percentage"]].replace(",","."))
    state = row[col_index["state"]]
    typeT = row[col_index["type"]]
    proyect = row[col_index["proyect"]]
    if ( (state == "Pte Validacion" or state == "Corregida") and percentage == 100.0 ):
        #TASK IS FINISHED
        finished = True;
    elif ( (state == "Pte Validacion" or state == "Corregida") or percentage == 100.0 ):
        print("Task "+row[col_index["issue"]]+" has inconsistent State/Percentage, marking as not finished");
    elif state == "Bloqueada":
        blocked = True;
    stats["totalH"] += hours;
    if finished:
        stats["doneH"] += hours;
    if blocked:
        stats["blockedH"] += hours;
    if proyect in stats["proyectsH"]:
        stats["proyectsH"][proyect] += hours;
    else:
        stats["proyectsH"][proyect] = hours;
    if state in stats["States"]:
        stats["States"][state] += 1;
    else:
        stats["States"][state] = 1;
    if typeT in stats["Types"]:
        stats["Types"][typeT] += 1;
    else:
        stats["Types"][typeT] = 1;


def get_sprint_stats(csv_file):
    stats={}
    stats["totalH"] = 0
    stats["doneH"] = 0
    stats["blockedH"] = 0
    stats["proyectsH"] = {}
    stats["States"] = {}
    stats["Types"] = {}
    with open(csv_file,newline='',encoding='latin-1') as f:
        reader=csv.reader(f,delimiter=";");
        col_index = get_column_indexes(reader.__next__())
        for row in reader:
            fill_stats_from_row(col_index,row,stats);
    return stats

def str2date(datestr):
    #print(datestr,datestr[0:4],datestr[4:6],datestr[6:8])
    return datetime.date(int(datestr[0:4]), int(datestr[4:6]), int(datestr[6:8]))

def get_sprint_dates(startDate,endDate,holidayDates):
    if startDate is None or endDate is None:
        print("Start or End Date not provided, assumming 2 week sprint starting this week");
        no = datetime.datetime.now().date()
        startDate = (no-datetime.timedelta(days=no.weekday())).strftime("%Y%m%d");
        endDate = (no-datetime.timedelta(days=no.weekday())+datetime.timedelta(days=13)).strftime("%Y%m%d")
        holidayDates = []
    print("Sprint goes from "+startDate+" to "+endDate)
    dates=[];
    startd = str2date(startDate)
    endd = str2date(endDate)
    festd = [str2date(d) for d in holidayDates];
    auxd = startd;
    while auxd <= endd:
        if auxd not in festd and auxd.weekday() < 5:
            dates.append(auxd);
        auxd = auxd + datetime.timedelta(days=1);
    return dates;

def plot_values(dates,totalh,finh,blockedh,now,title="Sprint"):
    today_in = -1;
    for d in dates:
        today_in +=1;
        if d == now.date():
            break;
    #print(today_in);
    hinc = totalh/(len(dates));
    ptotalh = [totalh - d*hinc for d in range(0,len(dates)+1)];
    #print(len(dates),ptotalh)
    hincfin = finh / today_in;
    #print(hinc,hincfin)
    pfinh = [totalh - d*hincfin for d in range(0,today_in+1)];
    #print(hincfin,pfinh)
    fig, ax = plt.subplots()
    # plot 'ABC' column, using red (r) line and label 'ABC' which is used in the legend
    ax.plot(ptotalh,'k-',label="Target (%dh to finish)"% int(ptotalh[today_in]))
    ax.plot(pfinh,'b-',label="Current (%dh to finish)"% int(pfinh[today_in]))
    ax.set_xticks(range(0,len(dates)+1))
    #ax.set_xticklabels(["0"]+[d.strftime("%d %b") for d in dates])     # set the ticklabels to the list of datetimes
    ax.set_xticklabels([d.strftime("%a %d") for d in dates]+["END"])     # set the ticklabels to the list of datetimes

    #plt.xticks(rotation=30)       # rotate the xticklabels by 30 deg
    plt.axvline(today_in,0,1,color="gray",dashes=[1,1])
    if(pfinh[today_in] > ptotalh[today_in]):
        plt.plot((today_in, today_in), (ptotalh[today_in], pfinh[today_in]), 'r-',linewidth=4,solid_capstyle="butt",label="Difference (%dh)" % round(pfinh[today_in]-ptotalh[today_in]));
        if blockedh > 0:
            plt.plot((today_in, today_in), (ptotalh[today_in], ptotalh[today_in]+blockedh), 'y-',linewidth=6,solid_capstyle="butt",label="Blocked (%dh)" % round(blockedh));
    else:
        plt.plot((today_in, today_in), (pfinh[today_in], ptotalh[today_in]), 'g-',linewidth=4,solid_capstyle="butt",label="We are awesome!!");
    ax.legend(loc=1, fontsize=10) # make a legend and place in bottom-right (loc=4)
    plt.xlabel("Sprint Days");
    plt.ylabel("Hours");
    ax.set_ylim(0,max(pfinh)*1.1)
    plt.title(title+" (Total %dh)"%totalh)
    fig.show()
    # plt.plot(ptotald,ptotalh,pfind,pfinh);
    # #plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%d'))
    # plt.gca().xaxis.set_major_locator(FixedLocator())
    # plt.show()


def make_autopct(values):
    def my_autopct(pct):
        total = sum(values)
        val = int(round(pct*total/100.0))
        return '{v:d} ({p:.2f}%)'.format(p=pct,v=val)
    return my_autopct

def plot_sprint_pie(dictData,title):
    fig,ax = plt.subplots()
    labels = list(dictData.keys());
    values = list(dictData.values());
    plt.pie(values,labels=labels,autopct=make_autopct(values),startangle=90)
    plt.title(title);
    ax.axis("equal")
    fig.show()


def main(csv_file,startDate,endDate,holidayDates,title):
    stats = get_sprint_stats(csv_file);
    #print(stats)
    dates = get_sprint_dates(startDate,endDate,holidayDates);

    #plot_sprint_proyects(stats["proyectsH"]);
    plot_sprint_pie(stats["proyectsH"], "Hours by Proyect\n")
    plot_sprint_pie(stats["States"], "Tasks by State\n")
    plot_sprint_pie(stats["Types"], "Tasks by Type\n")
    plot_values(dates,stats["totalH"],stats["doneH"],stats["blockedH"],datetime.datetime.now(),title=title)
    plt.show()


def parse_arguments(argv):
  parser = optparse.OptionParser();
  parser.add_option("-f","--f",help="Location of csv file",default=None,dest = "filename");
  parser.add_option("-s","--start",help="Provide start date of this sprint, format: 20170315",default=None,dest="start")
  parser.add_option("-e","--end",help="Provide end date of this sprint,format: 20170315",default=None,dest="end")
  parser.add_option("-n","--nowork",help="Provide holidays in this spring,format: 20170315 (multiple can be provided)",action="append",dest="holidays",default=[])
  parser.add_option("-t","--title",help="Sprint title",default="Sprint",dest="title")
  options,args = parser.parse_args(argv);
  if options.filename is None:
    print("Please provide redmine csv file");
    parser.print_help();
    exit(1);
  return options;


if __name__ == "__main__":
    options=parse_arguments(sys.argv)
    sys.exit(main(options.filename,options.start,options.end,options.holidays,options.title));
