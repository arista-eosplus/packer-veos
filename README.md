#Automatically Create vEOS nodes using Packer

##Introduction
The guides below will help you quickly turn up vEOS nodes running on VMware (FusionPro/Workstation) or VirtualBox. The Packer configuration files (.json) define 4 VM nodes and assign specific virtual networks to switch interfaces to simulate isolated connections. You can setup a quick demo by using [packer-veos](https://github.com/arista-eosplus/packer-veos) and [packer-ztpserver](https://github.com/arista-eosplus/packer-ztpserver). Both of these installations use the [ztpserver-demo](https://github.com/arista-eosplus/ztpserver-demo) files to create a simple test environment.

###VMware Virtual Network Setup
![vEOS Networks](https://raw.githubusercontent.com/arista-eosplus/packer-veos/master/gh-pages/images/vEOS-spine-leaf-vmware.jpg)

###VirtualBox Virtual Network Setup
![vEOS Networks](https://raw.githubusercontent.com/arista-eosplus/packer-veos/master/gh-pages/images/vEOS-spine-leaf-vbox.jpg)

##Getting Started

 * [Create vEOS nodes in VMware](https://github.com/arista-eosplus/packer-veos/tree/master/VMware)
 * [Create vEOS nodes in VirtualBox](https://github.com/arista-eosplus/packer-veos/tree/master/VirtualBox)
