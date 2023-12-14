# pwnagotchi-scripts

#### Needless to say, this project is for EDUCATIONAL use only and is not intended for any illegal usage.

Basically a linux version of [pwnagotchi-tools](https://github.com/mtagius/pwnagotchi-tools). These scripts will do the following:
- SSH into pwnagotchi & pull .pcap handshakes 
- Convert pcap to hc22000 format for hashcat




Required:
- [hcxtools](https://launchpad.net/ubuntu/+source/hcxtools) `sudo apt-get -y install hcxtools` 
- [7z](https://www.7-zip.org/download.html) `sudo apt-get -y install p7zip-full`
- [Hashcat 6.2+](https://hashcat.net/hashcat/) 
- [Cuda Toolkit (For GPU)](https://linuxconfig.org/how-to-install-cuda-on-ubuntu-20-04-focal-fossa-linux)
- [Nvidia Drivers (For GPU)](https://linuxconfig.org/how-to-install-the-nvidia-drivers-on-ubuntu-20-04-focal-fossa-linux)

 ```
wget https://hashcat.net/files/hashcat-6.2.6.7z
```
Extract contents

```
7z x hashcat*
```
Move to pwnagotchi-scripts hashcat directory

```
sudo mv hashcat-6.2.6 /path/to/pwnagotchi-scripts/hashcat/hashcat
```

### Wordlists

You will need to download the following wordlists. Move them to /pwnagotchi-scripts/wordlists directory
* known-wpa-passwords.txt - This is your own personal list of your cracked wifi passwords.
* [netgear-spectrum.txt](https://raw.githubusercontent.com/soxrok2212/PSKracker/master/dicts/netgear-spectrum/netgear-spectrum.txt) - The repo for this list is [here](https://github.com/soxrok2212/PSKracker)
* [NAMES.DIC](https://www.outpost9.com/files/wordlists/names.zip)-  Any list of all lowercase first names can replace this.
* [words_alpha.txt](https://raw.githubusercontent.com/dwyl/english-words/master/words_alpha.txt) - Any list of all lowercase common words can replace this.
* [hashesorg2019](https://weakpass.com/wordlist/1851)
* [openwall.net-all.txt](https://raw.githubusercontent.com/danielmiessler/SecLists/master/Passwords/openwall.net-all.txt)
* [rockyou](https://github.com/praetorian-code/Hob0Rules/blob/master/wordlists/rockyou.txt.gz) - The famous rockyou list. 
* [Top24Million-WPA-probable-v2.txt](https://github.com/berzerk0/Probable-Wordlists/blob/master/Real-Passwords/WPA-Length/Real-Password-WPA-MegaLinks.md)
* [Top1pt8Billion-WPA-probable-v2.txt](https://github.com/berzerk0/Probable-Wordlists/blob/master/Real-Passwords/WPA-Length/Real-Password-WPA-MegaLinks.md)
* [passphrases.txt](https://initstring.keybase.pub/passphrase-wordlist/passphrases.txt?dl=1) - The repo for this list is [here](https://github.com/initstring/passphrase-wordlist).
* [Custom-WPA](https://weakpass.com/wordlist/490)
* [Super-WPA](https://weakpass.com/wordlist/500)

### Configuration

Configuration is very simple. You actually do not need to change anything if you extract hashcat and the wordlists to the configured directories. If you wish to change them however, you can modify the following in `grab_and_convert.sh`

```
SSHKEY=
HASHCAT_LOCATION=
WORDLIST_LOCATION=
```
# Running 

- Pull files from pwnagotchi, convert to hc2000 and create attack script.

```
sudo sh grab_and_convert.sh
```

- Crack with Hashcat

```
cd hashcat/scripts && sh hash.sh
```

