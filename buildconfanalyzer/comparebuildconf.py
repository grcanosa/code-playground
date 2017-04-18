#!/usr/bin/python3

import sys
import optparse

import buildconf

class bcolors:
    HEADER = '\033[95m'
    USO = '\033[94m'
    OK = '\033[92m'
    WARNING = '\033[93m'
    KO = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def main(build1,build2):
    b1 = buildconf.BuildConf(build1)
    b2 = buildconf.BuildConf(build2)
    print("Modules in build conf 1 with their correspondent modules of build 2");
    for m1 in b1.modules:
        m2 = b2.get_module(m1.name)
        if m2 is not None:
            modifier = "";
            text = ""
            if m1.version != m2.version or m1.type != m2.type:
                modifier = (bcolors.KO)
                text = "KO"
            else:
                modifier = (bcolors.OK)
                text = "OK"
            print("{}{:<4}{:<30}{:<5}{:<12}{:<5}{:<10}{}".format(modifier,text,m1.name,
                        m1.type,m1.version,m2.type,m2.version,bcolors.ENDC))
        else:
            print("{}{:<4}{:<30}{:<5}{:<12}{:<5}{:<10}{}".format(bcolors.KO,"KO",m1.name,
                        m1.type,m1.version,"--","NOT PRESENT",bcolors.ENDC))

    print("Modules in build 2 that were not in build 1")
    for m2 in b2.modules:
        if not m2.checked:
            print("{:<4}{:<30}{:<5}{:<12}{:<5}{:<10}".format("",
                    m2.name,"","",m2.type,m2.version));


def parse_arguments(argv):
  parser = optparse.OptionParser();
  parser.add_option("--b1",help="Path to build conf 1",default = None,dest ="build1")
  parser.add_option("--b2",help="Path to build conf 2",default = None,dest ="build2")
  options,args = parser.parse_args(argv);
  if options.build1 is None or options.build2 is None:
    print("Please provide both build.conf files");
    parser.print_help();
    exit(1);
  return options;


if __name__ == '__main__':
    options = parse_arguments(sys.argv)
    main(options.build1,options.build2)
