#!/usr/bin/python3

import sprintstats as ST;
import csv

FINISHED_STATES = ["Pte Validacion","Corregida","Resuelta"]
BLOCKED_STATES = ["Bloqueada"]
SUPPORT_TYPES = ["Soporte"]


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

def fill_hoursinfo_with_data(isue,hours,percentage,state,proyect,hoursinfo):
    if ( (percentage == 100) != (state in FINISHED_STATES) ):
        print("Task "+str(issue)+" inconsistent state ("+state+") and percentage ("+str(percentage)+"), fix it");
    hoursinfo.total += hours;
    if state in FINISHED_STATES:
        hoursinfo.done += hours;
    elif state in BLOCKED_STATES:
        hoursinfo.blockedTotal += hours;
        hoursinfo.blocked += hours*percentage;
    sumvalueindict(hoursinfo.proyectsH, proyect, hours)
    sumvalueindict(hoursinfo.statesH, state, hours)

def fill_stats_from_row(col_index,row,sprintST):
    #print(row[col_index["proyect"]])
    issue= row[col_index["issue"]]
    hours = float(row[col_index["hours"]].replace(",","."));
    percentage = float(row[col_index["percentage"]].replace(",","."))
    state = row[col_index["state"]]
    typeT = row[col_index["type"]]
    proyect = row[col_index["proyect"]]
    if typeT in SUPPORT_TYPES:
        fill_hoursinfo_with_data(issue, hours, percentage, state, proyect, sprintST.horasSupport)
    else:
        fill_hoursinfo_with_data(issue, hours, percentage, state, proyect, sprintST.horasSprint)

def load_from_csv(csv_file,sprintST = None):
    if sprintST is None:
        sprintST = ST.SprintStats();
    with open(csv_file,newline='',encoding='latin-1') as f:
        reader=csv.reader(f,delimiter=";");
        col_index = get_column_indexes(reader.__next__())
        for row in reader:
            fill_stats_from_row(col_index,row,sprintST);
    return sprintST;
