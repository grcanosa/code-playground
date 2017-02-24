#!/usr/bin/python3
import sys
import json
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.ticker import FixedLocator
import datetime
import numpy as np
import optparse


def extract_string(text,tag):
  textspli = text.split();
  for t in textspli:
    if tag in t:
      textspli2 = t.split(":");
      return textspli2[1];

def extract_strings(text,tag):
  vstr = [];
  textspli = text.split();
  for t in textspli:
    if tag in t:
      textspli2 = t.split(":");
      vstr.append(textspli2[1]);
  return vstr;

def extract_number(text,tag):
  return float(extract_string(text,tag));

def str2date(datestr):
  #print(datestr,datestr[0:4],datestr[4:6],datestr[6:8])
  return datetime.date(int(datestr[0:4]), int(datestr[4:6]), int(datestr[6:8]))

def get_sprint_dates(wej):
  if "description" not in wej:
    print("Field description must be set for the board!!!!")
    print("Assumming 2 hour sprint with current week as first");
    no = datetime.datetime.now().date();
    desc = "";
    desc += "START:"+(no-datetime.timedelta(days=no.weekday())).strftime("%Y%m%d");
    desc += " "
    desc += "END:"+(no-datetime.timedelta(days=no.weekday())+datetime.timedelta(days=13)).strftime("%Y%m%d");
    wej["description"]= desc
  description = wej["description"]
  start = extract_string(description, "START");
  end = extract_string(description,"END");
  festivos = extract_strings(description, "FESTIVO")
  print("Sprint goes from "+start+" to "+end)
  dates=[];
  startd = str2date(start)
  endd = str2date(end)
  festd = [str2date(d) for d in festivos];
  auxd = startd;
  while auxd <= endd:
    if auxd not in festd and auxd.weekday() < 5:
      dates.append(auxd);
    auxd = auxd + datetime.timedelta(days=1);
  return dates;

def get_card_hours(a):
  if "HORAS:" in a["title"]:
    return extract_number(a["title"],"HORAS");
  if "description" in a and "HORAS:" in a["description"]:
    return extract_number(a["description"],"HORAS");
  print("CARD "+a["title"]+" HAS NOT HOURS SET!!!")
  return 0;

def get_hours(wej):
  total_h = 0;
  fin_h = 0;
  finListId = 0
  for l in wej["lists"]:
    if l["title"] == "FIN":
      finListId = l["_id"];
  for a in wej["cards"]:
    h = get_card_hours(a);
    total_h += h;
    if a["listId"] == finListId:
      fin_h += h;
  return total_h,fin_h;

def plot_values(dates,totalh,finh,now,title="Sprint"):
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
  ax.plot(ptotalh,'k-',label="Target (%d h)"% int(ptotalh[today_in]))
  ax.plot(pfinh,'b-',label="Current (%d h)"% int(pfinh[today_in]))
  ax.set_xticks(range(0,len(dates)+1))
  #ax.set_xticklabels(["0"]+[d.strftime("%d %b") for d in dates])     # set the ticklabels to the list of datetimes
  ax.set_xticklabels([d.strftime("%a %d") for d in dates]+["END"])     # set the ticklabels to the list of datetimes

  #plt.xticks(rotation=30)       # rotate the xticklabels by 30 deg
  plt.axvline(today_in,0,1,color="gray",dashes=[1,1])
  if(pfinh[today_in] > ptotalh[today_in]):
    plt.plot((today_in, today_in), (ptotalh[today_in], pfinh[today_in]), 'r-',linewidth=4,solid_capstyle="butt",label="Difference (%dh)" % round(pfinh[today_in]-ptotalh[today_in]));
  else:
    plt.plot((today_in, today_in), (pfinh[today_in], ptotalh[today_in]), 'g-',linewidth=4,solid_capstyle="butt",label="We are awesome!!");
  ax.legend(loc=1, fontsize=10) # make a legend and place in bottom-right (loc=4)
  plt.xlabel("Sprint Days");
  plt.ylabel("Hours");
  ax.set_ylim(0,max(pfinh)*1.1)
  plt.title(title+" (Total %dh)"%totalh)
  plt.show()
  # plt.plot(ptotald,ptotalh,pfind,pfinh);
  # #plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%d'))
  # plt.gca().xaxis.set_major_locator(FixedLocator())
  # plt.show()

def main(wekan_file):
  f = open(wekan_file)
  wej = json.load(f);
  f.close()
  dates = get_sprint_dates(wej)
  totalh,finh = get_hours(wej);
  plot_values(dates,totalh,finh,datetime.datetime.now(),title=wej["title"])


def parse_arguments(argv):
  parser = optparse.OptionParser();
  parser.add_option("-f","--f",help="Location of wekan file",default=None);
  options,args = parser.parse_args(argv);
  if options.f is None:
    print("Please provide wekan json file");
    parser.print_help();
    exit(1);
  return options.f;

if __name__ == "__main__":
  wekan_file = parse_arguments(sys.argv);
  sys.exit(main(wekan_file))
