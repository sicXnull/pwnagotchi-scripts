# pwnagotchi-scripts


-A collection of scripts to:
- SSH into pwnagotchi & pull .pcap handshakes 
- Convert pcap to hc22000 format for hashcat


-Required:
- hcxtools `sudo apt-get -y install hcxtools` 
- hashcat `sudo apt-get -y install hashcat`

# Running 

- Pull files from pwnagotchi:

```
sudo sh grab_and_convert.sh
```

