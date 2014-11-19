#Automatically Create vEOS Nodes with Packer
##Introduction
It can be a time-consuming and tedious task to turn up a handful of vEOS nodes up, especially when you want to simulate dedicated links between nodes. Here is a way to automate that procedure so that you can start testing ZTPServer even faster.
If you used [packer-ztpserver](https://github.com/arista-eosplus/packer-ztpserver) to create your ztpserver, you will have a set of demo files already on your server that complement the topology below.

The following procedure will create four vEOS nodes,
and assign the virtual networks as depicted in the diagram below.

![vEOS Networks](https://raw.githubusercontent.com/arista-eosplus/packer-veos/master/gh-pages/images/vEOS-spine-leaf-vmware.jpg)

###Prerequisites

 * **VMware Fusion Professional** - These packer scripts utilize functions that are only available in VMware Fusion Professional.
 * You will need to log into your Arista.com account to obtain the following files from https://www.arista.com/en/support/software-download:
     * Aboot-vEOS.iso
     * vEOS-[release].vmdk (This can be any release of your choice. **Rename it vEOS.vmdk**
 * **Virtual Networks**
     If you have not configured the vmnets described in the diagram above, you can run ```sudo ./setup-fusion.sh``` to do this for you. Note that VMWare should be started when you run this command.  You can modify the script to only modify/create certain vmnets.
     EG ```VMNETS=(2 3 4 5 6 7 9 10 11)```.  If you are using VMware Workstation, you can quickly create these vmnets using the vmnetcfg utility.



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



##2. Create vEOS Nodes for VMware
1. Retrieve the packer-veos configuration files [here](https://github.com/arista-eosplus/packer-veos/archive/master.zip) or use:
<pre>
git clone https://github.com/arista-eosplus/packer-veos.git
</pre>
2. Move into location
<pre>
cd packer-veos/VMware
</pre>
3. Place the files mentioned above into the correct directories. Your directory should look like:

    ```
    packer-veos
       /VMware
          - vEOS.json
          /source
              - vEOS.vmx
              - vEOS.vmdk
              - Aboot-vEOS.iso
    ```
4. The vEOS.json file contains unique configuration for four vEOS nodes - vEOS-1/2/3/4 as depicted above.
  * There are two command-line options that you can use to customize the build.
    * **ram** ```-var 'ram=[ram-in-MB]'``` or . The default ram is set to 2048MB.
    * **boot_time** ```-var 'boot_time=90s'```. The default ```boot_time``` is 2m30s.
    * eg:
    <pre>packer build --parallel=false -var 'ram=1800' -var 'boot_time=90s' vEOS.json</pre>
  2. If you would like to build your VMs with the default values, run:
  <pre>packer build --parallel=false vEOS.json</pre>
    * If you would like to build only select nodes, run:
        * ```packer build --only=vEOS1 vEOS.json```
        * ```packer build --only=vEOS2 vEOS.json```
        * ```packer build --only=vEOS3 vEOS.json```
        * ```packer build --only=vEOS4 vEOS.json```
