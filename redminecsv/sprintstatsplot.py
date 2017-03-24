#!/usr/bin/python3
import datetime
import matplotlib.pyplot as plt
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

def plot_burndown(sprintST,dates):
    today_in = get_today_index(dates)
    ticks = range(0,len(dates)+1)
    tickslabels = [d.strftime("%a %d") for d in dates]+["END"]
    total_val = down_linear_regression(sprintST.horasSprint.total, 0, len(dates)+1)
    fig, ax = plt.subplots()
    ax.plot(total_val,'k-',label="Target (%dh to finish)"% int(total_val[today_in]))
    if sprintST.horasSupport.total > 0:
        total_val_support = down_linear_regression(sprintST.horasSprint.total+sprintST.horasSupport.total, sprintST.horasSupport.total, len(dates)+1)
        #ax.plot(total_val_support,'r-',label="Target with support (%dh to finish)"% int(total_val_support[today_in]))

    not_done_h = sprintST.horasSprint.total-sprintST.horasSprint.done
    not_done_val = down_linear_regression(sprintST.horasSprint.total, not_done_h , today_in+1)
    ax.plot(not_done_val,'b-',label="Current (%dh to finish)"% int(not_done_val[today_in]))
    if sprintST.horasSupport.total > 0:
        not_done_sup_h = not_done_h + sprintST.horasSupport.total - sprintST.horasSupport.done
        not_done_sup_val = down_linear_regression(sprintST.horasSprint.total+sprintST.horasSupport.total, not_done_sup_h , today_in+1)
        #ax.plot(not_done_sup_val,'g-',label="Current with support (%dh to finish)"% int(not_done_sup_val[today_in]))
        not_done_without_support_h = sprintST.horasSprint.total-sprintST.horasSprint.done-sprintST.horasSupport.total
        not_done_without_support_val = down_linear_regression(sprintST.horasSprint.total, not_done_without_support_h , today_in+1)
        ax.plot(not_done_without_support_val,'b--',label="Current (prediction if no support) (%dh to finish)"% int(not_done_without_support_val[today_in]))
    ax.set_xticks(ticks)
    ax.set_xticklabels(tickslabels)
    ax.axvline(today_in,0,1,color="gray",dashes=[1,1])
    ax.legend(loc=1, fontsize=10) # make a legend and place in bottom-right (loc=4)
    plt.xlabel("Sprint Days");
    plt.ylabel("Hours");
    ax.set_ylim(0,(sprintST.horasSprint.total+sprintST.horasSupport.total)*1.1)
    title = sprintST.title+ " ("+ str(int(sprintST.horasSprint.total))+" hours"
    if sprintST.horasSupport.total > 0:
        title += " and "+str(int(sprintST.horasSupport.total))+ " support hours"
    title +=")"
    plt.title(title)
    plt.show()


def plot_stats(sprintST):
    dates = calcDates(sprintST);
    plot_burndown(sprintST,dates);
    #plot_burndown_bars(sprintST);
