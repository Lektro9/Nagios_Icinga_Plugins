#!/usr/bin/python
import os, sys, re

outP=os.popen("""ORACLE_HOME=/usr/lib/oracle/18.3/client64; PATH=$ORACLE_HOME/bin:$PATH;
 LD_LIBRARY_PATH=$ORACLE_HOME/lib; export ORACLE_HOME; export LD_LIBRARY_PATH; export PATH;
 cat /usr/lib64/nagios/plugins/sqlplus.sq | 
 sqlplus "system/password123@(DESCRIPTION=(ADDRESS=(PROTOCOL=TCP)(HOST=192.168.90.163)(PORT=1521))(CONNECT_DATA=(SID=ORCL)))" """).read()
pattern="\n(\w+)\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)"
matches=re.findall(pattern, outP)

# for match in matches:
#     print("{}: {}MB used, {}MB free, {}MB total, {}% free".format(match[0], match[1], match[2], match[3], match[4]))

## check for status
indexes = []
for idx, match in enumerate(matches):
    fPercentage = int(match[4])
    if fPercentage < 15:
        indexes.append(idx)
    else:
        print("\nOK - {}: {}MB used, {}MB free, {}MB total, {}% free".format(match[0], match[1], match[2], match[3], match[4]))
        
for idx in indexes:
    print("\nCRITICAL - {} only has {}% Diskspace left ({}MB)".format(matches[idx][0], matches[idx][4], matches[idx][2]))

if len(indexes) > 0:
    sys.exit(2)
else:
    sys.exit(0)
