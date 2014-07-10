#vEOS Setup - Packer.io Automation
##Introduction
Here is a way to automate vEOS node creation so that you can start testing ZTPServer even faster.
If you used [packer-ztpserver](https://github.com/arista-eosplus/packer-ztpserver) to create your ztpserver,
you will have a set of demo files already on your server that complement the setup below.

The following procedure will create four vEOS nodes,
and setup the virtual networks as depicted in the diagram below.

![vEOS Networks](https://raw.githubusercontent.com/arista-eosplus/packer-veos/master/gh-pages/images/vEOS-spine-leaf-vbox.jpg)

###Prerequisites

 * **VirtualBox**
 * **Packer** - If you do not have packer installed, follow the directions below:
    1. Download the appropriate binaries - http://www.packer.io/downloads.html
    2. Unzip and move to desired location eg ~/packer or /usr/local/share/ or /usr/local/bin/
    3. Set ENV variable (or just put Packer somewhere the ```PATH``` is already pointing - ```echo $PATH```)
        * EG: in ~/.bash_login, add ```PATH=$PATH:/path/to/packer/files```
    4. Run ```packer``` to make sure ```PATH``` is updated.
 * **vEOS Packer Plug-in**
    1. Download the custom [builder-virtualbox-veos](https://www.dropbox.com/s/pxiqtdckedevppq/builder-virtualbox-veos) plug-in.
    2. Put this plug-in with all of the standard Packer executables.
    3. Make this plug-in executable: ```chmod +x builder-vmware-veos```
    4. Modify the ```.packerconfig``` file to add this plug-in.  If this file does not exist, create it in ```$HOME/.packerconfig``` (this is a location Packer will look for it). Add the following config to that file:
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

##Creating vEOS Nodes for VirtualBox
1. ```cd``` to the ```vEOS/VirtualBox``` directory.
2. Place the files mentioned above into the correct directories. Your directory should look like:

    ```
    vEOS
       /VirtualBox
          - vEOS.json
          /source
              - vEOS.ovf
              - vEOS.vmdk
              - Aboot-veos-2.0.8.iso
    ```
3. The vEOS.json file contains unique configuration for four vEOS nodes - vEOS-1/2/3/4 as depicted above.
    * You must build the nodes one at a time since each run requires vbox to import the existing ovf/vmdk. Run:
        * ```packer build --only=vEOS1 vEOS.json```
        * ```packer build --only=vEOS2 vEOS.json```
        * ```packer build --only=vEOS3 vEOS.json```
        * ```packer build --only=vEOS4 vEOS.json```
