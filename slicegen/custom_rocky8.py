

import os
import time

import json
import traceback

from fabrictestbed.slice_manager import SliceManager, Status, SliceState

from fabrictestbed_extensions.fablib.fablib import fablib

print(f"FABRIC_ORCHESTRATOR_HOST: {os.environ['FABRIC_ORCHESTRATOR_HOST']}")
print(f"FABRIC_CREDMGR_HOST:      {os.environ['FABRIC_CREDMGR_HOST']}")
print(f"FABRIC_TOKEN_LOCATION:    {os.environ['FABRIC_TOKEN_LOCATION']}")

print("Printed some Env vars")

command= """echo Hello, FABRIC from node `hostname -s`; whoami; 
            df -h; cat /etc/centos-release; 
            sudo whoami;
            sudo ls -ltr  /etc/yum.repos.d/;
            sudo yum list epel-release;
            sudo yum -y install epel-release;
            sudo yum-config-manager --add-repo https://download.docker.com/linux/centos/docker-ce.repo;
            sudo sed -i 's/enabled=0/enabled=1/g'  /etc/yum.repos.d/Rocky-PowerTools.repo;
            sudo echo -e '[htcondor]\nname=HTCondor for Enterprise Linux 8 - Release\nbaseurl=https://research.cs.wisc.edu/htcondor/repo/9.x/el8/x86_64/release\nenabled=1\ngpgcheck=1\ngpgkey=file:///etc/pki/rpm-gpg/HTCondor-9.x-Key\npriority=90\n' | sudo tee /etc/yum.repos.d/htcondor.repo;
            sudo yum makecache;
            sudo yum install -y yum-utils device-mapper-persistent-data lvm2;
            sudo yum -y install wget;
            cd /etc/pki/rpm-gpg/
            sudo wget https://research.cs.wisc.edu/htcondor/repo/keys/HTCondor-9.x-Key
            sudo wget https://research.cs.wisc.edu/htcondor/repo/keys/HTCondor-9.0-Key
            sudo yum -y install singularity;
            sudo yum -y install condor;
            sudo yum -y install docker-ce docker-ce-cli containerd.io;
            sudo yum -y install git;
            sudo yum -y install time;
            sudo yum -y install iperf3;
            sudo systemctl start docker;
            sudo docker pull centos:7.9.2009;
            sudo yum -y install python39;
            pip3 install --user awscli;
            mkdir -p /home/rocky/.aws;
            pwd;
            sudo docker run -a stdin -a stdout -i centos:7.9.2009 /bin/echo Welcome_here;
            df -h;
            ssh-keygen -q  -b 3072 -t rsa -N '' <<< $'\ny' >/dev/null;
            cat /home/rocky/.ssh/id_rsa.pub;
            cat /home/rocky/.ssh/id_rsa.pub >> /home/rocky/.ssh/authorized_keys;
            sudo pwd"""


slice_name="MySliceSep12B"

try:
    slice = fablib.get_slice(slice_name)
    print(slice_name)

    for idx, node in enumerate(slice.get_nodes()):
        print("Index")
        print(idx)
        print(node)

        stdout, stderr = node.execute(command)
        print(stdout)
except Exception as e:
    print(f"Fail: {e}")

print("command executed")

