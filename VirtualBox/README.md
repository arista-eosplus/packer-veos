#Automatically Create vEOS Nodes with Packer
##Introduction
It can be a time-consuming and tedious task to turn up a handful of vEOS nodes up, especially when you want to simulate dedicated links between nodes. Here is a way to automate that procedure so that you can start testing ZTPServer even faster.
If you used [packer-ztpserver](https://github.com/arista-eosplus/packer-ztpserver) to create your ztpserver, you will have a set of demo files already on your server that complement the topology below.

The following procedure will create four vEOS nodes,
and assign the virtual networks as depicted in the diagram below.

![vEOS Networks](https://raw.githubusercontent.com/arista-eosplus/packer-veos/master/gh-pages/images/vEOS-spine-leaf-vbox.jpg)

###Prerequisites

 * **VirtualBox**The following procedure was tested using VirtualBox 4.3.12. **This does not work on Windows with 4.3.14**.
 * You will need to log into your Arista.com account to obtain the following files from https://www.arista.com/en/support/software-download:
     * Aboot-[release].iso and **rename it Aboot-vEOS.iso**
     * vEOS-[release].vmdk and **rename it vEOS.vmdk**

**NOTE:** You can use the any Aboot and vEOS release combination you want, but make sure that the two are compatible. If you are not sure the two files you indend to use are compatible, please contact support@arista.com.

 * **Virtual Networks**
     If you have not configured the vboxnets described in the diagram above, you can run ```./setup-vbox.sh``` to do this for you.
 * **VBoxBuilder will export a VM, but will NOT import/register it in VirtualBox afterwards.** Please go to the newly created folders and double click the .ovf files in order to import the VMs into VirtualBox. 


##1. Install Packer
First things first; we need Packer. Follow the steps below if you don't already have Packer installed.

###Manually
1. Download the appropriate binaries http://www.packer.io/downloads.html
2. Unzip and move to desired location eg ~/packer or /usr/local/share/
3. Set ENV variable (or just put Packer somewhere the ```PATH``` is already pointing - ```echo $PATH```)
    * EG: in ~/.bash_login, add ```EXPORT PATH=$PATH:/path/to/packer/files```

###Automatically (MacOSX)
<pre>
$ brew tap homebrew/binary
$ brew install packer
</pre>

###Verify Installation
Run this command to make sure Packer is properly installed.
<pre>
packer -v
</pre>


##2a. Create vEOS Nodes for VirtualBox (Mac OSX and Linux)
[I want to build vEOS nodes on Windows VirtualBox - skip to section](#2b-create-veos-nodes-for-virtualbox-windows)

1. Retrieve the packer-veos configuration files [here](https://github.com/arista-eosplus/packer-veos/archive/master.zip) or use:
<pre>
git clone https://github.com/arista-eosplus/packer-veos.git
</pre>
2. Move into location
<pre>
cd packer-veos/Virtualbox
</pre>
3. Place the files mentioned above into the correct directories. Your directory should look like:

    ```
    packer-veos
       /VirtualBox
          - vEOS.json
          - vEOS-windows.json
          /source
              - vEOS.ovf
              - vEOS.vmdk
              - Aboot-vEOS.iso
    ```
The vEOS.json file contains unique configuration for four vEOS nodes - vEOS-1/2/3/4 as depicted above.
  * There are two command-line options that you can use to customize the build.
    * **ram** ```-var 'ram=[ram-in-MB]'``` or . The default ram is set to 2048MB.
    * **boot_time** ```-var 'boot_time=90s'```. The default ```boot_time``` is 2m30s.
    * eg:
    <pre>packer build --parallel=false -var 'ram=1800' -var 'boot_time=90s' vEOS.json</pre>

4. If you would like to build your VMs with the default values, run:
<pre>packer build --parallel=false vEOS.json</pre>
  * If you would like to build only select nodes, run:
      * ```packer build --only=vEOS1 vEOS.json```
      * ```packer build --only=vEOS2 vEOS.json```
      * ```packer build --only=vEOS3 vEOS.json```
      * ```packer build --only=vEOS4 vEOS.json```
5. You will see new directories created (vEOS1/2/3/4) each containing an .ovf, .vmdk and .iso (Aboot). Double-click on the OVF to import the VM into VirtualBox.

>**NOTE:** There are times that the vEOS node does not boot properly and gets stuck at the 'starting udev.'  If this occurs, it is best to cancel (ctrl-c) the build and start again.


##2b. Create vEOS Nodes for VirtualBox (Windows)
1. Retrieve the packer-veos configuration files [here](https://github.com/arista-eosplus/packer-veos/archive/master.zip) or use:
<pre>
git clone https://github.com/arista-eosplus/packer-veos.git
</pre>
2. Move into location
<pre>
cd packer-veos/Virtualbox
</pre>
3. Place the files mentioned above into the correct directories. Your directory should look like:

    ```
    packer-veos
       /VirtualBox
          - vEOS.json
          - vEOS-windows.json
          /source
              - vEOS.ovf
              - vEOS.vmdk
              - Aboot-vEOS.iso
    ```
The vEOS-windows.json file contains unique configuration for four vEOS nodes - vEOS-1/2/3/4 as depicted above.
  * There are two command-line options that you can use to customize the build.
    * **ram** ```-var 'ram=[ram-in-MB]'``` or . The default ram is set to 2048MB.
    * **boot_time** ```-var 'boot_time=90s'```. The default ```boot_time``` is 2m30s.
    * eg:
    <pre>packer build --parallel=false -var 'ram=1800' -var 'boot_time=90s' vEOS-windows.json</pre>

4. If you would like to build your VMs with the default values, run:
<pre>packer build --parallel=false vEOS-windows.json</pre>
  * If you would like to build only select nodes, run:
      * ```packer build --only=vEOS1 vEOS-windows.json```
      * ```packer build --only=vEOS2 vEOS-windows.json```
      * ```packer build --only=vEOS3 vEOS-windows.json```
      * ```packer build --only=vEOS4 vEOS-windows.json```
5. You will see new directories created, vEOS{1,2,3,4}, each containing an .ovf, .vmdk and .iso (Aboot). Double-click on the OVF to import the VM into VirtualBox.

>**NOTE:** There are times that the vEOS node does not boot properly and gets stuck at the 'starting udev.'  If this occurs, it is best to cancel (ctrl-c) the build and start again.
