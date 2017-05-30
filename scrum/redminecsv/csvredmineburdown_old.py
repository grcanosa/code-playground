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

FINISHED_STATES = ["Pte Validacion","Corregida","Resuelta"]
BLOCKED_STATES = ["Bloqueada"]
SUPPORT_TYPES = ["Soporte"]

class HoursInfo:
    def __init__(self):
        self.hours = {};
        self.types = {};


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

def sumvalueindict(dictobj,key,value):
    if key in dictobj:
        dictobj[key] += value;
    else:
        dictobj[key] = value;

def fill_stats_from_row(col_index,row,stats):
    #print(row[col_index["proyect"]])
    hours = float(row[col_index["hours"]].replace(",","."));
    percentage = float(row[col_index["percentage"]].replace(",","."))
    state = row[col_index["state"]]
    typeT = row[col_index["type"]]
    proyect = row[col_index["proyect"]]
    if ( (state in FINISHED_STATES) and percentage == 100.0 ):
        #TASK IS FINISHED
        finished = True;
    elif ( (state in FINISHED_STATES) or percentage == 100.0 ):
        print("Task "+row[col_index["issue"]]+" has inconsistent State ("+state+") and percentage ("+str(percentage)+"), please fix it");
    # stats["totalH"] += hours;
    # if finished:
    #     stats["doneH"] += hours;
    # if blocked:
    #     stats["blockedH"] += hours;

    sumvalueindict(stats["ProyectsH"],proyect, hours);
    sumvalueindict(stats["StatesH"],state, hours);
    sumvalueindict(stats["TypesH"],typeT, hours);

def get_sprint_stats(csv_file):
    stats={}
    stats["ProyectsH"] = {}
    stats["StatesH"] = {}
    stats["TypesH"] = {}
    with open(csv_file,newline='',encoding='latin-1') as f:
        reader=csv.reader(f,delimiter=";");
        col_index = get_column_indexes(reader.__next__())
        for row in reader:
            fill_stats_from_row(col_index,row,stats);
    stats["HOURS"] = {};
    stats["HOURS"]["SPRINT"] = {}
    stats["HOURS"]["SPRINT"]["Total"] = sum([m[1] for m in stats["TypesH"].items() if m[0] not in SUPPORT_TYPES])
    stats["HOURS"]["SPRINT"]["Done"] = sum([m[1] for m in stats["StatesH"].items() if m[0] in FINISHED_STATES])
    stats["HOURS"]["SPRINT"]["Blocked"] = sum([m[1] for m in stats["StatesH"].items() if m[0] in BLOCKED_STATES])

    stats["HOURS"]["Support"] = sum([m[1] for m in stats["TypesH"].items() if m[0] in SUPPORT_TYPES])
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

def plot_bars(dates,totalh,finh,blockedh,now,title="Sprint"):
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
    hincblock = blockedh / today_in;
    #print(hinc,hincfin)
    plefth = [totalh - d*hincfin for d in range(0,today_in+1)];
    pfinh = [totalh-p for p in plefth];
    pblocked = [d*hincblock for d in range(0,today_in+1)];
    fig,ax = plt.subplots()
    bar_width = 0.35
    index = np.arange(len(pfinh))-bar_width/2;
    ax.bar(index,plefth,width=bar_width,color="r");
    ax.bar(index,pfinh,width=bar_width,color="b",bottom=plefth);
    # index = np.arange(len(pfinh))
    # ax.bar(index-bar_width/2,pfinh,width=bar_width,color="r");
    # index = np.arange(len(ptotalh))
    # ax.bar(index-bar_width/2,ptotalh,width=bar_width,color='b');
    ax.plot(ptotalh,'k-',linewidth=2,label="Target (%dh to finish)"% int(ptotalh[today_in]))
    ax.set_xticks(range(0,len(dates)+1))
    #ax.set_xticklabels(["0"]+[d.strftime("%d %b") for d in dates])     # set the ticklabels to the list of datetimes
    ax.set_xticklabels([d.strftime("%a %d") for d in dates]+["END"])     # set the ticklabels to the list of datetimes
    plt.tight_layout()

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
            plt.plot((today_in, today_in), (pfinh[today_in]-blockedh, pfinh[today_in]), 'y-',linewidth=6,solid_capstyle="butt",label="Blocked (%dh)" % round(blockedh));
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


# def make_autopct(values):
#     def my_autopct(pct):
#         total = sum(values)
#         val = int(round(pct*total/100.0))
#         return '{v:d} ({p:.2f}%)'.format(p=pct,v=val)
#     return my_autopct

def plot_sprint_pie(dictData,titlep):
    fig,ax = plt.subplots(2,1)
    cs = cm.Set1(np.arange(len(dictData))/len(dictData))
    data = sorted(dictData.items(), key=lambda x: x[1],reverse = True)
    labels = [x[0] for x in data];
    values = [x[1] for x in data];
    total = sum(values);
    cells = []
    for i,l in enumerate(labels):
        cells.append([str(values[i])+" h",str(round(values[i]/total*100.0))+" %"])
    ret = ax[0].pie(values,startangle=90,colors=cs)
    #ax[0].title(titlep);
    #legend = ax[0].legend(newlabels,bbox_to_anchor=(2.2, 0.5), loc=5, borderaxespad=0.)
    ax[0].axis("equal")
    ax[0].axis(aspect=2)
    ax[1].axis("off")
    rowlabels = labels;
    ax[1].table(cellText=cells,bbox=[0.25, 0, 0.75, 1], cellLoc='center',rowLabels=rowlabels,rowColours=cs,colWidths=[.2]*2)
    fig.show()


def main(csv_file,startDate,endDate,holidayDates,title):
    #plt.rcParams['axes.color_cycle'].remove('k')
    stats = get_sprint_stats(csv_file);
    print(json.dumps(stats,indent=4))
    #print(stats)
    dates = get_sprint_dates(startDate,endDate,holidayDates);

    plot_sprint_pie(stats["ProyectsH"], "Hours by Proyect\n")
    plot_sprint_pie(stats["StatesH"], "Hours by Task State\n")
    plot_sprint_pie(stats["TypesH"], "Hours by Task Type\n")
    plot_values(dates,stats["HOURS"]["SPRINT"]["Total"],stats["HOURS"]["SPRINT"]["Done"],stats["HOURS"]["SPRINT"]["Blocked"],datetime.datetime.now(),title=title)
    plot_bars(dates,stats["HOURS"]["SPRINT"]["Total"],stats["HOURS"]["SPRINT"]["Done"],stats["HOURS"]["SPRINT"]["Blocked"],datetime.datetime.now(),title=title)
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
