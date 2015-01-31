#!/usr/bin/python

##############################################
# Library for creating ZTPServer-related Demos
# Author: eosplus-dev@arista.com
# Date: 20150113
##############################################

import sys
import os
import re
import platform
import argparse
import subprocess
import datetime
import urllib
import zipfile
import getpass


packerURL = "http://dl.bintray.com/mitchellh/packer"
packerVersion = "0.7.5"

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def getHostOS():
    return platform.system().lower()

def getHostArch():
    is_64bits = sys.maxsize > 2**32
    return 64 if is_64bits else 32

def which(program):
    def is_exe(fpath):
        return os.path.isfile(fpath) and os.access(fpath, os.X_OK)

    fpath, fname = os.path.split(program)
    if fpath:
        if is_exe(program):
            return program
    else:
        for path in os.environ["PATH"].split(os.pathsep):
            path = path.strip('"')
            exe_file = os.path.join(path, program)
            if is_exe(exe_file):
                return exe_file

    return False

def find(path, name):
    print "Searching %s for %s..." % (path, name)
    # Look recursively through OS for files
    for root, dirs, files in os.walk(path):
        #print files
        if name in files:
            print "Found file here:%s" % root
            return root
        if name in dirs:
            print "Found file here:%s" % root
            return os.path.join(root, name)

    # File wasn't found, return false
    return False

def getUnzipped(url, dest, fn):
    name = os.path.join(dest, fn)
    try:
        if find(dest, fn.split(".zip")[0]):
            print "%s already exists, no need to download again." % fn.split(".zip")[0]
        else:
            print "Downloading Packer binaries to %s" % name
            print "This may take a few minutes (~85MB)..."
            name, hdrs = urllib.urlretrieve(url, name)
            print "Download successful!"
    except IOError, e:
        print "Can't retrieve %r to %r: %s" % (url, name, e)
        raise

    try:
        print "Unzipping %s..." % name
        with zipfile.ZipFile(name, "r") as z:
            bin = os.path.join(dest, "packer-bin")
            z.extractall(bin)
    except zipfile.error, e:
        print "Bad zipfile (from %r): %s" % (url, e)
        raise
    print "Unzipped successfully to %s" % bin
    return bin

def installPacker(hostOS, hostArch):
    if hostArch == 64:
        arch = "amd64"
    else:
        arch = "386"

    url = "%s/packer_%s_%s_%s.zip" % (packerURL, packerVersion, hostOS, arch)

    installPath = os.path.expanduser('~')
    packerZipDir = getUnzipped(url, installPath, "packer-bin.zip")
    packerDir = os.path.join(installPath, "packer-bin")

    # Make all Packer binaries executable
    for file in os.listdir(packerDir):
        file = os.path.join(packerDir, file)
        os.chmod(file, 0o777)

    # Add packer-bin to path
    os.environ["PATH"] += os.pathsep + packerDir
    print "Updated path to be:%s" % os.environ["PATH"]
    print "Packer installed!"
    return os.path.join(packerDir, "packer")

def getActiveNets(cmd, regex):
    # Get existing networks and return array of numbers
    try:
        ifconfig = subprocess.check_output(cmd)
        return re.findall(r"%s" % regex, ifconfig)
    except OSError as e:
        if e.errno == os.errno.ENOENT:
            print "vboxnet creation failed. Check output above"
            raise
        else:
            print "Something else went wrong"
            raise

def createVBoxNets(hostOS, hostArch, libDir):
    print "Creating virtual networks for Virtual Box"

    if hostOS == "darwin":
        # Open VirtualBox App
        print "Opening VirtualBox application..."
        cmd = ["open", "-a", "VirtualBox"]
        process = subprocess.Popen(cmd)

        #Get list of current networks
        cmd = ["ifconfig", "-a"]
        regex = "vboxnet(\d+)"
        activeNets = getActiveNets(cmd, regex)

        print "\nAnalyzing Host-Only Networks..."

        # Create vmnets
        vmnets = (0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10)
        if len(activeNets) < len(vmnets):
            if len(activeNets) > 0:
                print "Existing Host-Only networks found:"
                for n in activeNets:
                    print " - %s" % n
            else:
                print "No existing Host-Only networks found."

            numCreate = len(vmnets) - len(activeNets)
            for i in range(0, numCreate):
                try:
                    cmd = "%s/vboxmanage" % libDir
                    subprocess.call([cmd, "hostonlyif", "create"])
                except OSError as e:
                    if e.errno == os.errno.ENOENT:
                        print "vboxnet creation failed. Check output above"
                        raise
                    else:
                        print "Something else went wrong"
                        raise
        else:
            print "Enough existing virtual networks exist. Let's just reconfigure them."

        try:
            for net in vmnets:

                print "Creating/modifying vboxnet%s" % net
                network = int(net) + 128
                print " - Assigning vboxnet%s to 172.16.%s.1/24" % (net, network)

                cmd = "%s/vboxmanage" % libDir
                vboxnet = "vboxnet%s" % net
                ip = "172.16.%s.1" % network
                subprocess.call([cmd, "hostonlyif", "ipconfig", vboxnet,
                                 "-ip", ip, "-netmask", "255.255.255.0"])
        except OSError as e:
            if e.errno == os.errno.ENOENT:
                print "vboxnet creation failed. Check output above"
                raise
            else:
                print "Something else went wrong"
                raise

        # Remove any DHCP Servers from virtual networks
        try:
            cmd = "%s/vboxmanage" % libDir
            dhcpList = subprocess.check_output([cmd, "list", "dhcpservers"])
            regex = "NetworkName:\s+(\S+)"
            hostOnlyDHCPSrvs = re.findall(r"%s" % regex, dhcpList)

            print "Disabling DHCP Servers"
            for srv in hostOnlyDHCPSrvs:
                print "Disabling HostOnlyIf DHCP Server %s" % srv
                subprocess.call([cmd, "dhcpserver", "remove", "--netname", srv])

            return True

        except OSError as e:
            if e.errno == os.errno.ENOENT:
                print "vboxnet creation failed. Check output above"
                raise
            else:
                print "Something else went wrong"
                raise

    elif hostOS == "windows":
        # Open VirtualBox App
        print "Opening VirtualBox application..."
        cmd = ["%s/VirtualBox.exe" % libDir]
        process = subprocess.Popen(cmd)

        #Get list of current networks
        cmd = ["ipconfig"]
        regex = "Ethernet.*(VirtualBox Host-Only.*):"
        activeNets = getActiveNets(cmd, regex)

        print "\nAnalyzing Host-Only Networks..."

        # Create vmnets
        vmnets = ("", " #2", " #3", " #4", " #5", " #6", " #7", " #8", " #9", " #10")
        if len(activeNets) < len(vmnets):
            if len(activeNets) > 0:
                print "Existing Host-Only networks found:"
                for n in activeNets:
                    print " - %s" % n
            else:
                print "No existing Host-Only networks found."

            numCreate = len(vmnets) - len(activeNets)
            print "Creating %s new Host-Only Networks" % numCreate
            for i in range(0, numCreate):
                try:
                    cmd = "%s/vboxmanage" % libDir
                    subprocess.call([cmd, "hostonlyif", "create"])
                except OSError as e:
                    if e.errno == os.errno.ENOENT:
                        print "vboxnet creation failed. Check output above"
                        raise
                    else:
                        print "Something else went wrong"
                        raise
        else:
            print "Enough existing virtual networks exist. Let's just reconfigure them."
            print "Existing Host-Only networks found:"
            for n in activeNets:
                print " - %s" % n

        try:
            network = 128
            for net in vmnets:

                print "Modifying VirtualBox Host-Only Ethernet Adapter%s" % net
                print " - Assigning VirtualBox Host-Only Ethernet Adapter%s to 172.16.%s.1/24\n" % (net, network)

                cmd = "%s/vboxmanage" % libDir
                vboxnet = "VirtualBox Host-Only Ethernet Adapter%s" % net
                ip = "172.16.%s.1" % network
                subprocess.call([cmd, "hostonlyif", "ipconfig", vboxnet,
                                 "-ip", ip, "-netmask", "255.255.255.0"])
                network += 1

        except OSError as e:
            if e.errno == os.errno.ENOENT:
                print "vboxnet creation failed. Check output above"
                raise
            else:
                print "Something else went wrong"
                raise

        # Remove any DHCP Servers from virtual networks
        try:
            cmd = "%s/vboxmanage" % libDir
            dhcpList = subprocess.check_output([cmd, "list", "dhcpservers"])
            regex = "NetworkName:\s+(\S+.*)"
            hostOnlyDHCPSrvs = re.findall(r"%s" % regex, dhcpList)

            print "Disabling DHCP Servers"
            for srv in hostOnlyDHCPSrvs:
                print " - Disabling DHCP Server %s" % srv
                subprocess.call([cmd, "dhcpserver", "remove", "--netname", "%s" % srv], shell=True)
        except OSError as e:
            if e.errno == os.errno.ENOENT:
                print "vboxnet creation failed. Check output above"
                raise
            else:
                print "Something else went wrong"
                raise
        return True

def createVmNets(hostOS, hostArch, libDir):
    print "Creating virtual networks for VMware"

    if hostOS == "darwin":
        # Open VMware Fusion App
        cmd = ["open", "-a", "VMware Fusion"]
        process = subprocess.Popen(cmd)

        #Get list of current networks
        cmd = ["ifconfig"]
        regex = "vmnet(\d+)"
        activeNets = getActiveNets(cmd, regex)

        print "\nAnalyzing Host-Only Networks..."

        # Create/modify vmnets
        vmnets = (2, 3, 4, 5, 6, 7, 9, 10, 11)
        try:
            if len(activeNets) > 0:
                print "Existing vmnets found:"
                for n in activeNets:
                    print " - VMnet%s" % n
            else:
                print "No existing vmnets found."

            print "Creating/modifying vmnets"
            for net in vmnets:

                print "Creating/modifying vmnet%s" % net
                print "---------------------------"

                network = int(net) + 128
                netcfgCmd = r"%s/vmnet-cfgcli" % libDir
                cfgCmd = r"%s/vmnet-cli" % libDir
                dhcpCmd = "VNET_%s_DHCP" % net
                subnetCmd = "VNET_%s_HOSTONLY_SUBNET" % net
                subnet = "172.16.%s.0" % network
                netmaskCmd = "VNET_%s_HOSTONLY_NETMASK" % net
                virtualCmd = "VNET_%s_VIRTUAL_ADAPTER" % net
                subprocess.call(["sudo", netcfgCmd, "vnetcfgadd", dhcpCmd, "no"])
                subprocess.call(["sudo", netcfgCmd, "vnetcfgadd", subnetCmd, subnet])
                subprocess.call(["sudo", netcfgCmd, "vnetcfgadd", netmaskCmd, "255.255.255.0"])
                subprocess.call(["sudo", netcfgCmd, "vnetcfgadd", virtualCmd, "yes"])

            # Configure and restart to take effect
            print "Committing vmware network services"
            print "----------------------------------"
            subprocess.call(["sudo", cfgCmd, "--configure"])

            print "Stopping vmware network services"
            print "--------------------------------"
            subprocess.call(["sudo", cfgCmd, "--stop"])

            print "Starting vmware network services"
            print "--------------------------------"
            subprocess.call(["sudo", cfgCmd, "--start"])

            print "VMNets Installed!"

        except OSError as e:
            if e.errno == os.errno.ENOENT:
                print "vmnet creation failed. Check output above"
                raise
            else:
                print "Something else went wrong"
                raise

        return True

    elif hostOS == "windows":
        # Open VMware Fusion App
        cmd = ["%s/vmware.exe" % libDir]
        process = subprocess.Popen(cmd)

        #Get list of current networks
        cmd = ["ipconfig"]
        regex = "VMnet(\d+)"
        activeNets = getActiveNets(cmd, regex)

        print "\nAnalyzing Host-Only Networks..."

        # Create/modify vmnets
        vmnets = ["2", "3", "4", "5", "6", "7", "9", "10", "11"]

        try:
            if len(activeNets) > 0:
                print "Existing vmnets found:"
                for n in activeNets:
                    print " - VMnet%s" % n
            else:
                print "No existing vmnets found."

            # Trim vmnets
            createNets = [x for x in vmnets if x not in activeNets]

            netcfgCmd = r"%s/vnetlib.exe" % libDir
            print netcfgCmd

            # Stop Workstation services - nat dhcp
            print "Stopping VMware Workstation NAT service"
            rc = subprocess.call([netcfgCmd, "--", "stop", "nat"])
            print "Stopping VMware Workstation DHCP service"
            rc = subprocess.call([netcfgCmd, "--", "stop", "dhcp"])

            # create networks that dont already exist
            for net in createNets:
                netName = "vmnet%s" % net
                print " - Creating new virtual network %s" % netName
                rc = subprocess.call([netcfgCmd, "--", "add",
                                      "adapter", netName])
                rc = subprocess.call([netcfgCmd, "--", "update",
                                      "adapter", netName])

            # Configure ALL of the networks in vmnets list
            for net in vmnets:
                network = 128 + int(net)
                netName = "vmnet%s" % net
                mask = "255.255.255.0"
                addr = "172.16.%s.0" % network
                print "Modifying virtual network %s" % netName
                print " - setting netmask to %s" % mask
                rc = subprocess.call([netcfgCmd, "--", "set", "vnet",
                                      netName, "mask", mask])
                print " - setting address to %s" % addr
                rc = subprocess.call([netcfgCmd, "--", "set", "vnet",
                                      netName, "addr", addr])
                print " - disabling DHCP server on vmnet%s" % net
                rc = subprocess.call([netcfgCmd, "--", "remove",
                                      "dhcp", netName])
                print " - disabling NAT on vmnet%s" % net
                rc = subprocess.call([netcfgCmd, "--", "remove",
                                      "nat", netName])
                print " - saving changes for vmnet%s" % net
                rc = subprocess.call([netcfgCmd, "--", "update",
                                      "dhcp", netName])
                rc = subprocess.call([netcfgCmd, "--", "update",
                                      "nat", netName])
                rc = subprocess.call([netcfgCmd, "--", "update",
                                      "adapter", netName])

            # Start DHCP and NAT
            print "Starting VMware Workstation NAT service"
            rc = subprocess.call([netcfgCmd, "--", "start", "nat"])
            print "Starting VMware Workstation DHCP service"
            rc = subprocess.call([netcfgCmd, "--", "start", "dhcp"])

            print "VMNets Installed!"
        except OSError as e:
            if e.errno == os.errno.ENOENT:
                print "vmnet creation failed. Check output above"
                raise
            else:
                print "Something else went wrong"
                raise

        return True
