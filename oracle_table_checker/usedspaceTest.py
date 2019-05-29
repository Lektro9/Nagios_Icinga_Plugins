#!/usr/bin/python

import argparse
import os, sys, re

# NAGIOS return codes :
# https://nagios-plugins.org/doc/guidelines.html#AEN78
OK       = 0
WARNING  = 1
CRITICAL = 2
UNKNOWN  = 3

cmd_df = """ORACLE_HOME=/usr/lib/oracle/18.3/client64; PATH=$ORACLE_HOME/bin:$PATH;
 LD_LIBRARY_PATH=$ORACLE_HOME/lib; export ORACLE_HOME; export LD_LIBRARY_PATH; export PATH;
 cat /usr/lib/nagios/plugins/sqlplus.sq | 
 sqlplus "system/password123@(DESCRIPTION=(ADDRESS=(PROTOCOL=TCP)(HOST=192.168.90.163)(PORT=1521))
 (CONNECT_DATA=(SID=ORCL)))" """

def get_args():
   """
   Supports the command-line arguments listed below.
   """
   parser = argparse.ArgumentParser(description="Oracle Tablesize Checker")
   parser._optionals.title = "Options"
   parser.add_argument('-c', '--critical', nargs=1, required=False, help='insert critical threshold', dest='critical', type=int, default=[15])
   parser.add_argument('-w', '--warning', nargs=1, required=False, help='insert warning threshold', dest='warning', type=int, default=[40])
   args = parser.parse_args()
   return args


def main():
   """
   CMD Line tool
   """

   # Handling arguments
   args            = get_args()
   critical_percentage = args.critical[0]
   warning_percentage = args.warning[0]

   #####################################
   # Oracle Table Check                #
   #####################################

   outP=os.popen(cmd_df).read()
   pattern="\n(\w+)\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)"
   matches=re.findall(pattern, outP)

   warning_indexes = []
   critical_indexes = []
   for idx, match in enumerate(matches):
       fPercentage = int(match[4])
       if fPercentage < critical_percentage:
           critical_indexes.append(idx)
       elif fPercentage < warning_percentage:
           warning_indexes.append(idx)
       else:
           print("\nOK - {} has {}% Diskspace left ({}MB)".format(match[0], match[4], match[2]))
          
   for idx in critical_indexes:
       print("\nCRITICAL - {} only has {}% Diskspace left ({}MB)".format(matches[idx][0], matches[idx][4], matches[idx][2]))
   for idx in warning_indexes:
       print("\nWARNING - {} only has {}% Diskspace left ({}MB)".format(matches[idx][0], matches[idx][4], matches[idx][2]))

   if len(critical_indexes) > 0:
       sys.exit(CRITICAL)
   elif len(critical_indexes) > 0:
       sys.exit(WARNING)
   else:
       sys.exit(OK)

if __name__ == "__main__":
  main()
