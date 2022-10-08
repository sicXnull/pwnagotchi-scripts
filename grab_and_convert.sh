#!/bin/sh
# Author: sic
INSTALL_LOCATION="$(pwd)"

echo "*** MUST BE RUN AS ROOT ***"

mkdir $INSTALL_LOCATION/handshakes
mkdir $INSTALL_LOCATION/handshakes/pcap
mkdir $INSTALL_LOCATION/handshakes/hash
ssh-keygen -t rsa
ssh-copy-id root@10.0.0.2
scp -r ~/.ssh/id_rsa.pub root@10.0.0.2:/home/pi/handshakes/*.pcap $INSTALL_LOCATION/handshakes/pcap
scp -r ~/.ssh/id_rsa.pub root@10.0.0.2:/root/handshakes/*.pcap $INSTALL_LOCATION/handshakes/pcap
rm $INSTALL_LOCATION/handshakes/pcap/*.pub

cd $INSTALL_LOCATION/handshakes/pcap
hcxpcapngtool -o hash.hc22000 -E network-list.txt *
mv hash.hc22000 $INSTALL_LOCATION/handshakes/hash
chmod -R a+rwx $INSTALL_LOCATION/*