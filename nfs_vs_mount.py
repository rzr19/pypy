#!usr/bin/env python
#nagios custom check 1-on-1 between /etc/fstab entries and /proc/self/moounts

__author == "__rzr19__"

import subprocess,sys
#uuidFstabCmd="for i in `cat/etc/fstab|sed 's@\s+@\s@g;s@\(^s3fs\).*\s\(\/.*\)@\1\2@g'|grep -v '^#'|awk '{print$1}'|cut -c6-60`; do blkid -U $i; done"

uuidFstabCmd="cat /etc/fstab | grep -v "^[UUID=]"
proc1=subprocess.Popen(uuidFstabCmd,stdout=subprocess.PIPE,shell=True)
(out1,err)=proc1.communicate()
uuidFstabOut=out1.split()

mountListCmd="cat /proc/self/mounts|awk '{print $1}'"
proc2=subprocess.Popen(mountListCmd, stdout=subprocess.PIPE, shell=True)
(out2,err)=proc2.communicate()
mountListOut=out2.split()

diff=list(set(mountListOut)-set(uuidFstabCmd))
if(diff!=''):
    for i in diff:
        print("The /etc/fstab entry" + diff[i] + "is not mounted")
        syst.exit(2)
else:
    print("All the /etc/fstab entries are mounted")
    sys.exit(0)

