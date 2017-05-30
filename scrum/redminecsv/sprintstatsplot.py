#!/usr/bin/python3
import datetime
import matplotlib.pyplot as plt
from matplotlib import cm
import numpy as np

import sprintstats as ST;

def str2date(datestr):
    #print(datestr,datestr[0:4],datestr[4:6],datestr[6:8])
    return datetime.date(int(datestr[0:4]), int(datestr[4:6]), int(datestr[6:8]))


def calcDates(sprintST):
    startDate = sprintST.startDate;
    endDate = sprintST.endDate;
    holidayDates = sprintST.festivos;
    if startDate == "" or endDate == "":
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

def down_linear_regression(n1,n2,ticks):
    inc = (n1-n2)/(ticks-1)
    regr = [n1-d*inc for d in range(0,ticks)];
    #print(n1,n2,ticks,regr)
    return regr;


def get_today_index(dates):
    now_date = datetime.datetime.now().date()
    today_in = -1;
    for d in dates:
        today_in +=1;
        if d == now_date:
            break;
    if today_in == -1:
        print("BAD DATES, assumming first day of sprint")
        today_in = 0;
    return today_in

def plot_burndown(sprintST,dates,endDay,printAll=True):
    today_in = len(dates);
    if not endDay:
        today_in = get_today_index(dates)
    ticks = range(0,len(dates)+1)
    tickslabels = [d.strftime("%a %d") for d in dates]+["END"]
    total_val = down_linear_regression(sprintST.horasSprint.total, 0, len(dates)+1)
    fig, ax = plt.subplots()
    ax.plot(total_val,'k-',label="Target (%dh to finish)"% int(total_val[today_in]))
    if sprintST.horasSupport.total > 0 and printAll:
        total_val_support = down_linear_regression(sprintST.horasSprint.total+sprintST.horasSupport.total, sprintST.horasSupport.total, len(dates)+1)
        ax.plot(total_val_support,'r-',label="Target with support (%dh to finish)"% int(total_val_support[today_in]))

    not_done_h = sprintST.horasSprint.total-sprintST.horasSprint.doneFinished
    not_done_val = down_linear_regression(sprintST.horasSprint.total, not_done_h , today_in+1)
    ax.plot(not_done_val,'b-',label="Finished (%dh to finish)"% int(not_done_val[today_in]))
    not_done_real_h = sprintST.horasSprint.total - sprintST.horasSprint.doneReal;
    not_done_real_val = down_linear_regression(sprintST.horasSprint.total, not_done_real_h , today_in+1)
    ax.plot(not_done_real_val,'y--',label="Done (%dh to finish)"% int(not_done_real_val[today_in]))
    if sprintST.horasSupport.total > 0:
        if printAll:
            not_done_sup_h = not_done_h + sprintST.horasSupport.total - sprintST.horasSupport.doneFinished
            not_done_sup_val = down_linear_regression(sprintST.horasSprint.total+sprintST.horasSupport.total, not_done_sup_h , today_in+1)
            ax.plot(not_done_sup_val,'g-',label="Current with support (%dh to finish)"% int(not_done_sup_val[today_in]))
        not_done_without_support_h = sprintST.horasSprint.total-sprintST.horasSprint.doneFinished-sprintST.horasSupport.total
        not_done_without_support_val = down_linear_regression(sprintST.horasSprint.total, not_done_without_support_h , today_in+1)
        ax.plot(not_done_without_support_val,'b--',label="Finished (prediction if no support) (%dh to finish)"% int(not_done_without_support_val[today_in]))

    total_hours_done = sprintST.horasSprint.doneFinished + sprintST.horasSupport.doneFinished;
    ax.plot(today_in,total_hours_done,'w',label="Hours done (sprint + support) %dh"%int(total_hours_done))
    hours_blocked = sprintST.horasSprint.blockedReal + sprintST.horasSupport.blockedReal;
    total_hours_blocked = sprintST.horasSprint.blockedTotal + sprintST.horasSupport.blockedTotal;
    ax.plot(today_in,total_hours_done,'w',label="Hours blocked %dh"%int(total_hours_blocked))
    #FORMATTINGS
    ax.set_xticks(ticks)
    ax.set_xticklabels(tickslabels)
    ax.axvline(today_in,0,1,color="gray",dashes=[1,1])
    plt.xlabel("Sprint Days");
    plt.ylabel("Hours");
    ax.set_ylim(0,(sprintST.horasSprint.total+sprintST.horasSupport.total)*1.1)
    title = sprintST.title+ " ("+ str(int(sprintST.horasSprint.total))+" hours"
    if sprintST.horasSupport.total > 0:
        title += " and "+str(int(sprintST.horasSupport.total))+ " support hours"
    title +=")"
    plt.title(title)
    plt.legend(loc=3, fontsize=10) # make a legend and place in bottom-right (loc=4)
    fig.show()

def plot_pie(horas,labels, ax1,ax2,title):
    cs = cm.Set1(np.arange(len(horas))/len(horas))
    ax1.pie(horas,startangle=90,colors=cs)
    ax1.axis("equal")
    cells = []
    total = sum(horas);
    for i,l in enumerate(labels):
        cells.append([str(horas[i])+" h",str(round(horas[i]/total*100.0))+" %"])
    ax2.axis("off")
    ax2.set_title(title)
    tab = ax2.table(cellText=cells,loc="center", cellLoc='center',rowLabels=labels,rowColours=cs,colWidths=[.2]*2)
    #tab.set_fontsize(20)
    #tab.scale(1.2,1.2)
    #plt.tight_layout();

def plot_pies(sprintST):
    fig, ((ax11,ax12),(ax21,ax22)) = plt.subplots(2,2);
    horas = sprintST.horasSprint
    hours = [horas.doneFinished];
    hours.append(horas.doneReal-horas.doneFinished);
    hours.append(horas.blockedReal);
    hours.append(horas.total-horas.doneReal-horas.blockedReal)

    labels = ["Finished","In progress","Blocked","Waiting"]
    plot_pie(hours,labels, ax11, ax21,"Sprint Hours \n (calculated with percentages)")
    # horas = sprintST.horasSprint
    # hours = [horas.doneFinished+sprintST.horasSupport.doneFinished];
    # hours.append(horas.total-horas.doneFinished-horas.blockedTotal);
    # hours.append(horas.blockedTotal);
    # plot_pie(hours,labels, ax12, ax22,"Sprint and Support Hours")

def plot_stats(sprintST,endDay):
    dates = calcDates(sprintST);
    plot_burndown(sprintST,dates,endDay,False);
    plot_pies(sprintST)
    plt.show()
    #plot_burndown_bars(sprintST);
