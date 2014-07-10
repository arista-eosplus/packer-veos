#!/bin/bash

#Check the current status
printf "Starting the VirtualBox network setup....\n\nCurrent Vbox hostonlyifs\n-------------------------------------\n"
vboxmanage list hostonlyifs

printf "\nCreating vboxnets\n-------------------------------------\n"
for i in {0..10}; do
  vboxmanage hostonlyif create
done

printf "\nConfigure vboxnets\n-------------------------------------\n"
for i in {0..10}; do
  NET=$(($i+128))
  printf "Assigning vboxnet${i} to 172.16.${NET}.1/24\n"
  vboxmanage hostonlyif ipconfig vboxnet${i} -ip 172.16.${NET}.1 -netmask 255.255.255.0
done
