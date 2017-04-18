#!/usr/bin/python3


class HorasInfo:
    def __init__(self):
        self.total = 0;
        self.doneFinished = 0;
        self.doneReal = 0;
        self.blockedTotal = 0;
        self.blockedReal = 0;
        self.statesH = {}
        self.proyectsH = {}

class SprintStats:
    def __init__(self):
        self.title = ""
        self.startDate = "";
        self.endDate = "";
        self.festivos = [];
        self.horasSprint = HorasInfo();
        self.horasSupport = HorasInfo();

    def toDict(self):
        dD = self.__dict__.copy();
        dD["horasSprint"] = self.horasSprint.__dict__;
        dD["horasSupport"] = self.horasSupport.__dict__;
        return dD;
