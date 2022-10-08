# pwnagotchi-scripts


-A collection of scripts to:
- SSH into pwnagotchi & pull .pcap handshakes 
- Convert pcap to hc22000 format for hashcat


-Required:
- hcxtools `sudo apt-get -y install hcxtools` 
- [latest hashcat](https://github.com/hashcat/hashcat) 

# Running 

- Pull files from pwnagotchi, convert to hc2000 and create attack script.

```
sudo sh grab_and_convert.sh
```

