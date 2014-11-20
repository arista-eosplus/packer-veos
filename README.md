#Automatically Create vEOS nodes using Packer

##Introduction
The guides below will help you quickly turn up vEOS nodes running on VMware (FusionPro/Workstation) or VirtualBox. The Packer configuration files (.json) define 4 VM nodes and assign specific virtual networks to switch interfaces to simulate isolated connections. You can setup a quick demo by using [packer-veos](https://github.com/arista-eosplus/packer-veos) and [packer-ztpserver](https://github.com/arista-eosplus/packer-ztpserver). Both of these installations use the [ztpserver-demo](https://github.com/arista-eosplus/ztpserver-demo) files to create a simple test environment.

##Memory Requirements
**Each vEOS node requires at least 2G of RAM and so does the ZTPServer VM.** While the memory for the ZTPServer could be reduced without impacting the performance much (500M RAM should also work just fine), the memory requirements for vEOS are not as flexible (1.5G per VM might work with some older vEOS instances, but it is NOT recommended to go lower than that). Hence, in order to run this demo it is recommended to use a machine which has at least 16G or RAM. If that is not possible, the demo can still be used, but the VMs should not all be started at the same time (the maximum number of VMs which could run in parallel will depend on memory size of the system, given the constraints from above).

###VMware Virtual Network Setup
![vEOS Networks](https://raw.githubusercontent.com/arista-eosplus/packer-veos/master/gh-pages/images/vEOS-spine-leaf-vmware.jpg)

###VirtualBox Virtual Network Setup
![vEOS Networks](https://raw.githubusercontent.com/arista-eosplus/packer-veos/master/gh-pages/images/vEOS-spine-leaf-vbox.jpg)

##Getting Started

 * [Create vEOS nodes in VMware](https://github.com/arista-eosplus/packer-veos/tree/master/VMware)
 * [Create vEOS nodes in VirtualBox](https://github.com/arista-eosplus/packer-veos/tree/master/VirtualBox)
