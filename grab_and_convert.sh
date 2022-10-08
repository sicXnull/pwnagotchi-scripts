#!/bin/sh
# Author: sic
INSTALL_LOCATION="$(pwd)"
SSHKEY=$INSTALL_LOCATION/ssh/id_rsa
HASHCAT_LOCATION=
WORDLIST_LOCATION=


if [ "$EUID" -ne 0 ]
  then echo "Please run as root"
  exit
fi

cat <<EOT >> .env
PROJECT_PATH="$INSTALL_LOCATION/"
HASHCAT_PATH="$HASHCAT_LOCATION/"
WORDLIST_PATH="$WORDLIST_LOCATION/"
EOT

mkdir -p $INSTALL_LOCATION/handshakes $INSTALL_LOCATION/handshakes/pcap $INSTALL_LOCATION/handshakes/hash $INSTALL_LOCATION/hashcat/scripts $INSTALL_LOCATION/ssh

if [ ! -f $SSHKEY ]; then
echo "*** Generating SSH Key ***"
ssh-keygen -t rsa -f $INSTALL_LOCATION/ssh/id_rsa
ssh-copy-id -i $INSTALL_LOCATION/ssh/id_rsa root@10.0.0.2
fi
scp -r $INSTALL_LOCATION/ssh/id_rsa root@10.0.0.2:/home/pi/handshakes/*.pcap $INSTALL_LOCATION/handshakes/pcap
scp -r $INSTALL_LOCATION/ssh/id_rsa root@10.0.0.2:/root/handshakes/*.pcap $INSTALL_LOCATION/handshakes/pcap
rm $INSTALL_LOCATION/handshakes/pcap/*.pub
cd $INSTALL_LOCATION/handshakes/pcap
echo "*** Convert to hc22000 ***"
hcxpcapngtool -o hash.hc22000 -E $INSTALL_LOCATION/network-list.txt *
mv hash.hc22000 $INSTALL_LOCATION/handshakes/hash
chmod -R a+rwx $INSTALL_LOCATION/*
cd $INSTALL_LOCATION
echo "*** Generating Hashcat Attacks ***"
python3 generate-attacks.py