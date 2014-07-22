#vEOS Setup - Packer.io Automation
##Introduction
It can be time-consuming to get all of the vEOS VMs up, running and configured.
Here is a way to automate that procedure so that you can start testing ZTPServer even faster.
If you used [packer-ztpserver](https://github.com/arista-eosplus/packer-ztpserver) to create your ztpserver, you will have a set of demo files already on your server that complement the setup below.

The following procedure will create five vEOS nodes,
and setup the virtual networks as depicted in the diagram below.

![vEOS Networks](https://raw.githubusercontent.com/arista-eosplus/packer-veos/master/gh-pages/images/vEOS-spine-leaf-vmware.jpg)

###Prerequisites

 * **VMware Fusion Professional** - These packer scripts utilize functions that are only available in VMware Fusion Professional.
 * **Packer** - If you do not have packer installed, follow the directions below:
    1. Download the appropriate binaries - http://www.packer.io/downloads.html
    2. Unzip and move to desired location eg ~/packer or /usr/local/share/ or /usr/local/bin/
    3. Set ENV variable (or just put Packer somewhere the ```PATH``` is already pointing - ```echo $PATH```)
        * EG: in ~/.bash_login, add ```PATH=$PATH:/path/to/packer/files```
    4. Run ```packer``` to make sure ```PATH``` is updated.
 * **vEOS Packer plugin**
    1. Download the custom vEOS-packer plugin for your platform
        * Linux [amd64](https://www.dropbox.com/s/jbzggphvtnyivh4/builder-vmware-veos_linux_amd64.tar.gz) | [386](https://www.dropbox.com/s/idvjnccerlyzhyg/builder-vmware-veos_linux_386.tar.gz) | [arm](https://www.dropbox.com/s/ahn9rolkm1quaur/builder-vmware-veos_linux_arm.tar.gz)
        * MacOSX [amd64](https://www.dropbox.com/s/n6jntdm5cdfjlup/builder-vmware-veos_darwin_amd64.zip) | [386](https://www.dropbox.com/s/x8yd388jtk5tm9r/builder-vmware-veos_darwin_386.zip)
        * Windows [amd64](https://www.dropbox.com/s/icexa67o1uq6byn/builder-vmware-veos_windows_amd64.zip) | [386](https://www.dropbox.com/s/pm58fsf43106lnx/builder-vmware-veos_windows_386.zip)
    2. Put this plugin with all of the standard Packer executables.
    3. Make this plugin executable: ```chmod +x builder-vmware-veos```
    4. Modify the ```.packerconfig```(linux/OSX) or ```packer.config```(Windows) file to add this plugin.  If this file does not exist, create it in ```$HOME/.packerconfig``` or ```%APPDATA%/packer.config``` (this is a location Packer will look for it). Add the following config to that file:
    ```
    {
        "builders": {
          "vmware-veos": "builder-vmware-veos"
        }
    }
    ```
 * You will need to log into your Arista.com account to obtain the following files from https://www.arista.com/en/support/software-download:
     * Aboot-veos-2.0.8.iso
     * vEOS.vmdk (This can be any release of your choice, rename it to vEOS.vmdk)
 * **Virtual Networks**
     If you have not configured the vmnets described in the diagram above, you can run ```sudo ./setup-fusion.sh``` to do this for you.  You can modify the script to only modify/create certain vmnets.
     EG ```VMNETS=(2 3 4 5 6 7 9 10 11)```

##Creating vEOS Nodes for VMware
1. Retrieve the packer-veos files [here](https://github.com/arista-eosplus/packer-veos/archive/master.zip) or use ```git clone https://github.com/arista-eosplus/packer-veos.git```
    1. ```cd packer-veos/VMware```
2. Place the files mentioned above into the correct directories. Your directory should look like:

    ```
    vEOS
       /VMware
          - vEOS.json
          /source
              - vEOS.vmx
              - vEOS.vmdk
              - Aboot-veos-2.0.8.iso
    ```
3. The vEOS.json file contains unique configuration for four vEOS nodes - vEOS-1/2/3/4/cvx as depicted above.
    * It requires a non-trivial amount of CPU/memory to turn up all five at the same time.  If you're feeling daring, run:
        * ```packer build vEOS.json```
    * If you would like to build all nodes sequentially, run:
        * ```packer build --parallel=false vEOS.json```
    * If you would like to build only select nodes, run:
        * ```packer build --only=vEOS1 vEOS.json```
        * ```packer build --only=vEOS2 vEOS.json```
        * ```packer build --only=vEOS3 vEOS.json```
        * ```packer build --only=vEOS4 vEOS.json```
        * ```packer build --only=vEOS-cvx vEOS.json```
