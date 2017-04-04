#!/usr/bin/python3

class Module:
    def __init__(self):
        self.name = ""
        self.type = ""
        self.version = ""
        self.artefactos = [];
        self.checked = False;


class BuildConf:
    def __init__(self,build_conf_file):
        self.modules = [];
        self.load_from_buildconf(build_conf_file);

    def get_module(self,module_name):
        for m in self.modules:
            if m.name == module_name:
                m.checked = True;
                return m;
        return None;

    def load_from_buildconf(self,buildconffile):
        with open(buildconffile) as f:
            process_line = False;
            for l in f:
                if process_line:
                    line = l.lstrip(" ");
                    line = line.rstrip("\n");
                    if len(line) == 0:
                        continue;
                    if line[0] == "#":
                        continue;
                    if line[0] == ")":
                        break;
                    lsplit = line.split(":")
                    module= {}
                    module = Module();
                    module.type = lsplit[0];
                    namespli = lsplit[1].split("-")
                    if len(namespli) == 1:
                        module.name = namespli[0]
                        module.version = "0";
                    elif len(namespli) == 2:
                        module.name = namespli[0]
                        module.version = namespli[1]
                    else:
                        print("Line:"+line+" has something weird");
                    if len(lsplit)==3:
                        module.artefactos = lsplit[2].split(",");
                    self.modules.append(module);
                if "MODULE_LIST" in l:
                    process_line = True;
                    continue;
