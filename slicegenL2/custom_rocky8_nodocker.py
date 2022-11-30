

import os
import time

import json
import traceback

from fabrictestbed.slice_manager import SliceManager, Status, SliceState

from fabrictestbed_extensions.fablib.fablib import fablib

command= """echo Hello, FABRIC from node `hostname -s`; whoami; 
            df -h; cat /etc/centos-release; 
            sudo whoami;
            sudo ls -ltr  /etc/yum.repos.d/;
            sudo yum list epel-release;
            sudo yum -y install epel-release;
            sudo sed -i 's/enabled=0/enabled=1/g'  /etc/yum.repos.d/Rocky-PowerTools.repo;
            sudo echo -e '[htcondor]\nname=HTCondor for Enterprise Linux 8 - Release\nbaseurl=https://research.cs.wisc.edu/htcondor/repo/9.x/el8/x86_64/release\nenabled=1\ngpgcheck=1\ngpgkey=file:///etc/pki/rpm-gpg/HTCondor-9.x-Key\npriority=90\n' | sudo tee /etc/yum.repos.d/htcondor.repo;
            sudo yum makecache;
            sudo yum -y install wget;
            cd /etc/pki/rpm-gpg/
            sudo wget https://research.cs.wisc.edu/htcondor/repo/keys/HTCondor-9.x-Key
            sudo wget https://research.cs.wisc.edu/htcondor/repo/keys/HTCondor-9.0-Key
            sudo yum -y install singularity;
            sudo yum -y install condor;
            sudo yum -y install git;
            sudo yum -y install time;
            sudo yum -y install iperf3;
            sudo yum -y install nginx;
            sudo yum -y install python39;
            pip3 install --user awscli;
            mkdir -p /home/rocky/.aws;
            pwd;
            df -h;
            ssh-keygen -q  -b 3072 -t rsa -N '' <<< $'\ny' >/dev/null;
            cat /home/rocky/.ssh/id_rsa.pub;
            cat /home/rocky/.ssh/id_rsa.pub >> /home/rocky/.ssh/authorized_keys;
            sudo pwd"""

print("command defined")

slice_name="TestSliceNov23A"

try:
    slice = fablib.get_slice(slice_name)
    for idx, node in enumerate(slice.get_nodes()):
        print("Index")
        print(idx)
        print(node.get_name())
        stdout, stderr = node.execute(command)
        print(stdout)
except Exception as e:
    print(f"Fail: {e}")

print("command executed")

