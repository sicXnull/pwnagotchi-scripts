# Modified version of generate-hashcat-scripts.py which can be found here:
# https://github.com/mtagius/pwnagotchi-tools
# Big thanks to the original author

import os
import logging
from dotenv import load_dotenv
from random import randint
from pathlib import Path

logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
sessionScripts = []

# Load .env
load_dotenv()
project_path = Path(os.getenv("PROJECT_PATH", ""))
hashcat_path = Path(os.getenv("HASHCAT_PATH", ""))
wordlist_path = Path(os.getenv("WORDLIST_PATH", ""))

if not all([project_path, hashcat_path, wordlist_path]):
    raise ValueError("Environment variables for PROJECT_PATH, HASHCAT_PATH, or WORDLIST_PATH are missing!")

# Hashcat attack settings
HASHCAT_SCRIPT_VERSION = "v1"
TEMP_ABORT = "--hwmon-temp-abort=100"
WORKLOAD_PROFILE = "-w 2"
RULE_PATH = project_path / "hashcat/rules"
WORD_NINJA_PATH = project_path / "hashcat"
HASH_TYPE = "-m 22000"
OUTPUT_FILE = project_path / "hashcat/hashcat-output.txt"
POTFILE = project_path / "hashcat/hashcat-potfile.txt"
OUTPUT_PATH = f'--potfile-path "{POTFILE}" -o "{OUTPUT_FILE}"'

# Attacks list
ATTACKS = [
    ["-a 0", "known-wpa-passwords.txt", "quick-ssid.rule", "-S"],
    ["-a 0", "known-wpa-passwords.txt", "unix-ninja-leetspeak.rule", "-S"],
    ["-a 0", "known-wpa-passwords.txt", "rockyou-30000.rule", "-S"],
    ["-a 0", "known-wpa-passwords.txt", "d3ad0ne.rule", "-S"],
    ["-a 0", "nerdlist.txt", "quick-ssid.rule"],
    ["-a 0", "nerdlist.txt", "unix-ninja-leetspeak.rule"],
    ["-a 0", "nerdlist.txt", "rockyou-30000.rule"],
    ["-a 0", "nerdlist.txt", "d3ad0ne.rule"],
    ["-a 0", "bssid.rule"],
    ["-a 0", "ssid-ninja.rule"],
    ["-a 3", "MYWIFI?d?d?d?d"],
    ["-a 3", "wifi?d?d?d?d"],
    ["-a 3", "-1 !@$??#~%^&*^^ wifi?d?d?d?1"],
    ["-a 3", "wifi?d?d?d?d?d"],
    ["-a 3", "?d?d?d?dwifi"],
    ["-a 3", "?d?d?d?d?dwifi"],
    ["-a 3", "WIFI?d?d?d?d"],
    ["-a 3", "-1 !@$??#~%^&*^^ WIFI?d?d?d?1"],
    ["-a 3", "WIFI?d?d?d?d?d"],
    ["-a 3", "?d?d?d?dWIFI"],
    ["-a 3", "?d?d?d?d?dWIFI"],
    ["-a 3", "?l?l?l?lwifi"],
    ["-a 3", "-1 !@$??#~%^&*^^ ?l?l?l?lwifi?1"],
    ["-a 3", "?l?l?l?l?lwifi"],
    ["-a 3", "wifi?l?l?l?l"],
    ["-a 3", "-1 !@$??#~%^&*^^ wifi?l?l?l?l?1"],
    ["-a 3", "wifi?l?l?l?l?l"],
    ["-a 3", "?u?l?l?lWifi"],
    ["-a 3", "?u?l?l?l?lWifi"],
    ["-a 3", "?u?u?u?uWIFI"],
    ["-a 3", "-1 !@$??#~%^&*^^ ?u?u?u?uWIFI?1"],
    ["-a 3", "?u?u?u?u?uWIFI"],
    ["-a 3", "WIFI?u?u?u?u"],
    ["-a 3", "-1 !@$??#~%^&*^^ WIFI?u?u?u?u?1"],
    ["-a 3", "WIFI?u?u?u?u?u"],
    ["-a 0", "NAMES.DIC", "names.rule"],
    ["-a 0", "words_alpha.txt", "names.rule"],
    ["-a 0", "4-digit-append.rule"],
    ["-a 3", "?d?d?d?d?d?d?d?d"],
    ["-a 6", "netgear-spectrum.txt", "?d?d?d"],
    ["-a 6", "netgear-spectrum.txt", "?d"],
    ["-a 6", "netgear-spectrum.txt", "?d?d"],
    ["-a 0", "openwall.net-all.txt", "quick-ssid.rule"],
    ["-a 0", "netgear-spectrum.txt", "quick-ssid.rule"],
    ["-a 6", "words_alpha.txt", "?d"],
    ["-a 6", "words_alpha.txt", "-1 !@$??#~%^&*^^ ?1"],
    ["-a 6", "words_alpha.txt", "-1 !@$??#~%^&*^^ ?d?1"],
    ["-a 6", "words_alpha.txt", "-1 !@$??#~%^&*^^ ?1?d"],
    ["-a 6", "words_alpha.txt", "?d?d"],
    ["-a 6", "words_alpha.txt", "-1 !@$??#~%^&*^^ ?d?d?1"],
    ["-a 6", "words_alpha.txt", "?d?d?d"],
    ["-a 3", "?l?l?l?l?l?l1!"],
    ["-a 3", "?u?l?l?l?l?l1!"],
    ["-a 3", "?u?u?u?u?u?u1!"],
    ["-a 3", "?d?d?d?d?d?d?d?d?d"],
    ["-a 0", "hashesorg2019"],
    ["-a 0", "rockyou.txt", "quick-ssid.rule"],
    ["-a 0", "NAMES.DIC", "rockyou-30000.rule"],
    ["-a 0", "netgear-spectrum.txt", "unix-ninja-leetspeak.rule"],
    ["-a 0", "Top1pt8Billion-WPA-probable-v2.txt"],
    ["-a 0", "Top24Million-WPA-probable-v2.txt", "quick-ssid.rule"],
    ["-a 0", "passphrases.txt", "passphrases.rule"],
    ["-a 0", "Custom-WPA"],
    ["-a 0", "Super-WPA"],
    ["-a 3", "?h?h?h?h?h?h?h?h"],
    ["-a 3", "?H?H?H?H?H?H?H?H"],
    ["-a 3", "?d?d?d?d?d?d?d?d?d?d"]
]

# Generate the hashcat script
def generate_hashcat_script(filename: str):
    ssid = filename.split("_")[0]
    file_id = filename.split(".hc22000")[0]
    hash_path = project_path / "handshakes/hash" / filename
    session = f"--session {file_id}_{randint(1000, 9999)}"
    script_path = project_path / "hashcat/scripts" / f"{file_id}.sh"

    logging.info(f"Creating script: {script_path}")
    with script_path.open("w") as script_file:
        script_file.write(f"# {HASHCAT_SCRIPT_VERSION}\n")
        script_file.write(f'cd "{hashcat_path}"\n')

        for attack in ATTACKS:
            command = build_attack_command(attack, hash_path, session, ssid)
            script_file.write(f"{command}\n")

    sessionScripts.append(f"{file_id}.sh")

# Build hashcat commands
def build_attack_command(attack, hash_path, session, ssid):
    command = f'./hashcat.bin {attack[0]} {HASH_TYPE} {session} {TEMP_ABORT} {WORKLOAD_PROFILE} {OUTPUT_PATH} "{hash_path}"'

    if attack[0] == "-a 0":  # Dictionary attack
        command = handle_dict_attack(attack, command, ssid)
    elif attack[0] == "-a 3":  # Mask attack
        command += f" {attack[1]}"
    elif attack[0] == "-a 6":  # Hybrid attack
        command += f' "{wordlist_path / attack[1]}" {attack[2]}'

    return command

# Handle dictionary attacks
def handle_dict_attack(attack, command, ssid):
    if "bssid.rule" in attack[1]:
        return f'{command} -r "{RULE_PATH / attack[1]}"'
    if "ssid-ninja.rule" in attack[1]:
        return f'python "{WORD_NINJA_PATH / "wordNinjaGenerator.py"}" {ssid} | {command} -r "{RULE_PATH / attack[1]}"'
    command += f' "{wordlist_path / attack[1]}"'
    if len(attack) > 2:
        command += f' -r "{RULE_PATH / attack[2]}"'
    return command

# Generate scripts for handshakes
def generate_scripts_for_hcs():
    handshake_dir = project_path / "handshakes/hash"
    if not handshake_dir.exists():
        logging.error(f"Handshake directory {handshake_dir} not found!")
        return

    for filename in handshake_dir.iterdir():
        if filename.suffix == ".hc22000":
            logging.info(f"Generating attacks for {filename.name}")
            generate_hashcat_script(filename.name)

def print_logo():
    logo = '''
██████  ███████  █████  ██████  ██    ██     ██████      ██████  ██     ██ ███    ██ 
██   ██ ██      ██   ██ ██   ██  ██  ██           ██     ██   ██ ██     ██ ████   ██ 
██████  █████   ███████ ██   ██   ████        █████      ██████  ██  █  ██ ██ ██  ██ 
██   ██ ██      ██   ██ ██   ██    ██        ██          ██      ██ ███ ██ ██  ██ ██ 
██   ██ ███████ ██   ██ ██████     ██        ███████     ██       ███ ███  ██   ████ 
    '''
    print(logo)

if __name__ == "__main__":
    print_logo()
    generate_scripts_for_hcs()
