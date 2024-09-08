#!/bin/sh
# Author: sic

# Define variables
INSTALL_LOCATION="$(pwd)"
SSHKEY="$INSTALL_LOCATION/ssh/id_rsa"
SSHKEY_PUB="$INSTALL_LOCATION/ssh/id_rsa.pub"
HASHCAT_LOCATION="$INSTALL_LOCATION/hashcat/hashcat"
WORDLIST_LOCATION="$INSTALL_LOCATION/wordlists"
REMOTE_HOST="10.0.0.2"
REMOTE_DIR="/root/handshakes"
LOCAL_HANDSHAKES_DIR="$INSTALL_LOCATION/handshakes/pcap"

# Create necessary directories
mkdir -p "$INSTALL_LOCATION/handshakes/pcap" \
         "$INSTALL_LOCATION/handshakes/hash" \
         "$INSTALL_LOCATION/hashcat/scripts" \
         "$INSTALL_LOCATION/ssh"
         
cat <<EOT > .env
PROJECT_PATH="$INSTALL_LOCATION/"
HASHCAT_PATH="$HASHCAT_LOCATION"
WORDLIST_PATH="$WORDLIST_LOCATION/"
EOT

# Generate SSH key if not already present
if [ ! -f "$SSHKEY" ]; then
  echo "*** Generating SSH Key ***"
  ssh-keygen -t rsa -f "$SSHKEY" -N ""
  chmod 600 "$SSHKEY"
  chmod 644 "$SSHKEY_PUB"
  ssh-copy-id -i "$SSHKEY_PUB" root@"$REMOTE_HOST"
fi

# Set proper permissions on the SSH key
chmod 600 "$SSHKEY"
chmod 644 "$SSHKEY_PUB"

# Verify SSH key has been copied correctly
echo "*** Verifying SSH Key ***"
ssh -i "$SSHKEY" root@"$REMOTE_HOST" exit
if [ $? -ne 0 ]; then
  echo "SSH key authentication failed. Please check the SSH key and remote server settings."
  exit 1
fi

# Copy pcap files from remote host
echo "*** Copying pcap files from remote host ***"
scp -i "$SSHKEY" root@"$REMOTE_HOST":"$REMOTE_DIR/*.pcap" "$LOCAL_HANDSHAKES_DIR"

# Remove any public key files if present
rm -f "$LOCAL_HANDSHAKES_DIR/*.pub"

# Convert pcap files to hc22000 format
echo "*** Converting to hc22000 format ***"
cd "$LOCAL_HANDSHAKES_DIR" || {
  echo "Failed to change directory to $LOCAL_HANDSHAKES_DIR"
  exit 1
}
hcxpcapngtool -o hash.hc22000 -E "$INSTALL_LOCATION/network-list.txt" *.pcap
mv hash.hc22000 "$INSTALL_LOCATION/handshakes/hash"

# Set permissions
chmod -R a+rwx "$INSTALL_LOCATION"

# Generate Hashcat attacks
echo "*** Generating Hashcat Attacks ***"
cd "$INSTALL_LOCATION" || {
  echo "Failed to change directory to $INSTALL_LOCATION"
  exit 1
}
python3 generate-attacks.py || {
  echo "Failed to generate Hashcat attacks"
  exit 1
}

echo "*** Script completed successfully ***"
