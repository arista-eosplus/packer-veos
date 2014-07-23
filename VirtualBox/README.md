#vEOS Setup - Packer.io Automation
##Introduction
Here is a way to automate vEOS node creation so that you can start testing ZTPServer even faster.
If you used [packer-ztpserver](https://github.com/arista-eosplus/packer-ztpserver) to create your ztpserver,
you will have a set of demo files already on your server that complement the setup below.

The following procedure will create five vEOS nodes,
and setup the virtual networks as depicted in the diagram below.

![vEOS Networks](https://raw.githubusercontent.com/arista-eosplus/packer-veos/master/gh-pages/images/vEOS-spine-leaf-vbox.jpg)

###Prerequisites

 * **VirtualBox**The following procedure was tested using VirtualBox 4.3.12. **This does not work on Windows with 4.3.14**.
 * **Packer** - If you do not have packer installed, follow the directions below:
    1. Download the appropriate binaries - http://www.packer.io/downloads.html
    2. Unzip and move to desired location eg ~/packer or /usr/local/share/ or /usr/local/bin/
    3. Set ENV variable (or just put Packer somewhere the ```PATH``` is already pointing - ```echo $PATH```)
        * EG: in ~/.bash_login, add ```PATH=$PATH:/path/to/packer/files```
    4. Run ```packer``` to make sure ```PATH``` is updated.
 * **vEOS Packer plugin**
    1. Download the custom vEOS-packer plugin for your platform
        * Linux [amd64](https://www.dropbox.com/s/14piuz13isgqzew/builder-virtualbox-veos_linux_amd64.tar.gz) | [386](https://www.dropbox.com/s/o6lnpo83kgmi11a/builder-virtualbox-veos_linux_386.tar.gz) | [arm](https://www.dropbox.com/s/6ounwx21li1vyb5/builder-virtualbox-veos_linux_arm.tar.gz)
        * MacOSX [amd64](https://www.dropbox.com/s/ns7o48tzjl7do1r/builder-virtualbox-veos_darwin_amd64.zip) | [386](https://www.dropbox.com/s/6zh42ogemftfjaa/builder-virtualbox-veos_darwin_386.zip)
        * Windows [amd64](https://www.dropbox.com/s/7ohxvgz0c2uozzb/builder-virtualbox-veos_windows_amd64.zip) | [386](https://www.dropbox.com/s/391da53v8hgiqo4/builder-virtualbox-veos_windows_386.zip)
    2. Put this plugin with all of the standard Packer executables.
    3. Make this plugin executable: ```chmod +x builder-virtualbox-veos```
    4. Modify the ```.packerconfig```(linux/OSX) or ```packer.config```(Windows) file to add this plugin.  If this file does not exist, create it in ```$HOME/.packerconfig``` or ```%APPDATA%/packer.config``` (this is a location Packer will look for it). Add the following config to that file:
    ```
    {
        "builders": {
          "virtualbox-veos": "builder-virtualbox-veos"
        }
    }
    ```
 * You will need to log into your Arista.com account to obtain the following files from https://www.arista.com/en/support/software-download:
     * Aboot-veos-2.0.8.iso
     * vEOS-4.13.5M.vmdk or any release of your choice.  **Rename it vEOS.vmdk**.
 * **Virtual Networks**
     If you have not configured the vboxnets described in the diagram above, you can run ```./setup-vbox.sh``` to do this for you.

##Creating vEOS Nodes for VirtualBox (Mac OSX and Linux)
1. Retrieve the packer-veos files [here](https://github.com/arista-eosplus/packer-veos/archive/master.zip) or use ```git clone https://github.com/arista-eosplus/packer-veos.git```
    1. ```cd packer-veos/Virtualbox```
2. Place the files mentioned above into the correct directories. Your directory should look like:

    ```
    vEOS
       /VirtualBox
          - vEOS.json
          - vEOS-windows.json
          /source
              - vEOS.ovf
              - vEOS.vmdk
              - Aboot-veos-2.0.8.iso
    ```
3. The vEOS.json file contains unique configuration for four vEOS nodes - vEOS-1/2/3/4/cvx as depicted above.
    * You must build the nodes one at a time since each run requires vbox to import the existing ovf/vmdk.
    >**NOTE:** There are times that the vEOS node does not boot properly and gets stuck at the 'starting udev.'  If this occurs, it is best to cancel (ctrl-c) the build and start again.
        * Either run:
            * ```packer build --parallel=false vEOS.json```
        * or run:
            * ```packer build --only=vEOS1 vEOS.json```
            * ```packer build --only=vEOS2 vEOS.json```
            * ```packer build --only=vEOS3 vEOS.json```
            * ```packer build --only=vEOS4 vEOS.json```
            * ```packer build --only=vEOS-cvx vEOS.json```

##Creating vEOS Nodes for VirtualBox (Windows)
1. Retrieve the packer-veos files [here](https://github.com/arista-eosplus/packer-veos/archive/master.zip) or use ```git clone https://github.com/arista-eosplus/packer-veos.git```
    1. ```cd packer-veos/Virtualbox```
2. Place the files mentioned above into the correct directories. Your directory should look like:

    ```
    vEOS
       /VirtualBox
          - vEOS.json
          - vEOS-windows.json
          /source
              - vEOS.ovf
              - vEOS.vmdk
              - Aboot-veos-2.0.8.iso
    ```
3. The vEOS.json file contains unique configuration for four vEOS nodes - vEOS-1/2/3/4/cvx as depicted above.
    * You must build the nodes one at a time since each run requires vbox to import the existing ovf/vmdk.
    >**NOTE:** There are times that the vEOS node does not boot properly and gets stuck at the 'starting udev.'  If this occurs, it is best to cancel (ctrl-c) the build and start again.
        * Either run:
            * ```packer build --parallel=false vEOS-windows.json```
        * or run:
            * ```packer build --only=vEOS1 vEOS-windows.json```
            * ```packer build --only=vEOS2 vEOS-windows.json```
            * ```packer build --only=vEOS3 vEOS-windows.json```
            * ```packer build --only=vEOS4 vEOS-windows.json```
            * ```packer build --only=vEOS-cvx vEOS-windows.json```
