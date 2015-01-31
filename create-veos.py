#!/usr/bin/python

####################################
# Automatically setup a ZTPServer VM
# Author: eosplus-dev@arista.com
# Date: 20150113
####################################

import sys
import os
newPath = os.path.join(os.getcwd(), "lib")
sys.path.append(newPath)
from eosplusvnets import *

ABOOT_FN = "Aboot-vEOS.iso"
VMDK_FN = "vEOS.vmdk"
HYPERVISORS = ["vmware", "virtualbox"]
VEOS_NODES = ["vEOS1", "vEOS2", "vEOS3", "vEOS4"]

def createVM(hyper, hostOS, nodes, vmName, boottime, user, packerCmd):
    d = datetime.datetime.now()
    time = d.strftime("%Y%m%d_%H%M%S")
    if vmName:
        vmName = "%s_%s" % (time, vmName)
    else:
        vmName = "%s" % time

    print "Using VM name prefix %s" % vmName
    print "Creating VM with user %s" % user

    print bcolors.WARNING
    print "##############################################"
    print "WARNING: DO NOT TYPE IN VIRTUAL MACHINE WINDOW"
    print "##############################################"
    print bcolors.ENDC

    if "all" in nodes:
        OPTS = ""
    else:
        OPTS = "--only=%s" % ','.join(nodes)

    try:
        if (hyper == "virtualbox" and hostOS=="windows"):
            cmd = "%s build --parallel=false %s -var \'boot_time=%s\' -var \'name=%s\' vEOS-windows.json" % (packerCmd, OPTS, boottime, vmName)
            print "Executing command:%s" % cmd
            rc = subprocess.call([ cmd ], shell=True, cwd=hyper)
        else:
            cmd = "%s build --parallel=false %s -var \'boot_time=%s\' -var \'name=%s\' vEOS.json" % (packerCmd, OPTS, boottime, vmName)
            print "Executing command:%s" % cmd
            rc = subprocess.call([ cmd ], shell=True, cwd=hyper)

        print "Return code:%s" % rc
    except OSError as e:
        if e.errno == os.errno.ENOENT:
            print "Unable to create Virtual Machine"
            raise
        else:
            print "Something else went wrong"
            raise

    if rc == 0:
        return vmName
    elif rc > 0:
        print "Packer install failed!!!"
        print "Please copy raise an issue at https://github.com/arista-eosplus/packer-ztpserver/issues with your console output."
        exit(rc)

def registerVbox(hyper, libDir, vmName, nodes):
    #Import the VM into Vbox
    if hyper == "virtualbox":
        cmd = "%s/vboxmanage" % libDir
        if "all" in nodes:
            for n in VEOS_NODES:
                vmPath = "%s-%s/%s-%s.ovf" % (vmName, n, vmName, n)
                print "Importing VM: %s" % vmPath
                subprocess.call([ cmd, "import", "--options", "keepallmacs", vmPath ], cwd=hyper)
            return True
        else:
            for n in nodes:
                vmPath = "%s-%s/%s-%s.ovf" % (vmName, n, vmName, n)
                print "Importing VM: %s" % vmPath
                subprocess.call([ cmd, "import", "--options", "keepallmacs", vmPath ], cwd=hyper)
            return True

def main():


    parser = argparse.ArgumentParser(description="Automatically install the vEOS Demo Nodes")
    parser.add_argument("-H", "--hypervisor", required=True, choices=HYPERVISORS,
                        help="Hypervisor to create VM in")
    parser.add_argument("-n", "--nodes", choices=VEOS_NODES, nargs='+',
                        default=["all"], help="Space-separated list of nodes to build OR omit to build all")
    # parser.add_argument("-a", "--aboot", help="Location of Aboot ISO")
    # parser.add_argument("-d", "--disk", help="Location of vEOS VMDK")
    parser.add_argument("-b", "--boottime", default="2m30s",
                        help="This is the time Packer will wait before it sends commands over VNC")
    parser.add_argument("-N", "--vmname", help="The Virtual Machine name prefix")
    args = parser.parse_args()

    # Set install variables
    user = getpass.getuser()
    if user == "root" and os.getenv("SUDO_USER") != "root":
        print bcolors.FAIL, "ERROR: DO NOT RUN THIS SCRIPT WITH SUDO", bcolors.ENDC
        exit()

    hyper = args.hypervisor
    nodes = args.nodes
    boottime = args.boottime

    # Check for aboot and vmdk file existance
    print "Looking for required source files..."
    sourcePath = os.path.join( os.getcwd(), hyper, "source/")
    aboot = os.path.join( sourcePath, ABOOT_FN )
    vmdk = os.path.join( sourcePath, VMDK_FN )
    if os.path.isfile(aboot):
        print " - %s found in %s" % (ABOOT_FN, sourcePath)
    else:
        print bcolors.FAIL
        print " - ERROR:Cannot find '%s' in '%s'" % (ABOOT_FN, sourcePath)
        print " - Please make sure the file is named '%s' and located in '%s'" % (ABOOT_FN, sourcePath)
        print bcolors.ENDC
        exit(1)

    if os.path.isfile(vmdk):
        print " - %s found in %s" % (VMDK_FN, sourcePath)
    else:
        print bcolors.FAIL
        print " - ERROR:Cannot find '%s' in '%s'" % (VMDK_FN, sourcePath)
        print " - Please make sure the file is named '%s' and located in '%s'" % (VMDK_FN, sourcePath)
        print bcolors.ENDC
        exit(1)

    if args.vmname:
        vmName = args.vmname
    else:
        vmName = ""

    # Get host machine information
    hostOS = getHostOS()
    hostArch = getHostArch()
    print "Tailoring install for a %s bit %s environment" % (hostArch, hostOS)

    print "Looking for hypervisor libraries"
    if hyper == "vmware":
        if hostOS == "darwin":
            libDir = find("/Applications", "vmnet-cli")
        elif hostOS == "windows":
            libDir = find("C:\\", "vmware.exe")
    elif hyper == "virtualbox":
        if hostOS == "darwin":
            libDir = find("/usr", "VBoxManage")
        elif hostOS == "windows":
            libDir = find("C:\\", "VBoxManage.exe")

    # Test to see if Packer is installed
    packerCmd = which("packer")
    if not packerCmd:
        print "Packer not found - install it"
        packerCmd = installPacker(hostOS, hostArch)

    # Setup vnets then create VM
    if hyper == "virtualbox":
        if createVBoxNets(hostOS, hostArch, libDir):
            # Create the Virtual Machine
            vmName = createVM(hyper, hostOS, nodes, vmName, boottime, user, packerCmd)
            if vmName:
                if registerVbox(hyper, libDir, vmName, nodes):
                    print "Successfully created VM %s!" % vmName
                    exit(0)

    elif hyper == "vmware":
        if createVmNets(hostOS, hostArch, libDir):
            # Create the Virtual Machine
            vmName = createVM(hyper, hostOS, nodes, vmName, boottime, user, packerCmd)
            if vmName:
                print "Successfully created VM %s!" % vmName
                exit(0)


if __name__ == "__main__":
   main()
