#dräng code har error MÅSTE FIXAS
import string
import secrets
import argparse
import os.path
import base64
import getpass
import json
import pathlib
import time
import sys
from cryptography.fernet import Fernet
purple      = "\033[38;2;203;166;247m"
green       = "\033[38;2;166;227;161m"
reset       = "\033[0m"
red         = "\033[38;5;196m"
yellow      = "\033[38;5;220m"
blue        = "\033[38;2;137;180;250m"
blue2       = "\033[38;2;116;199;236m"

path = "~/.datapw/data/passw"
configpath = "~/.datapw/data/config.json"

fullPath = os.path.expanduser(path)
fullconfigPath = pathlib.Path(os.path.expanduser(configpath))


def firsttimesetup():
    print(blue + "first time setup, make a password for stored passwords" + reset)
    time.sleep(1)
    
    password = getpass.getpass(yellow + "enter password" + reset)
    confirm = getpass.getpass(yellow + "confirm password" + reset)
    
    if password != confirm:
        print(red + "passwords dont match" + reset)
        sys.exit(1)
        
    fullconfigPath.parent.mkdir(parents=True, exist_ok=True)
    
    configstoredPassword = base64.b64encode(password.encode()).decode()
    
    with open(fullconfigPath, "w") as f:
        json.dump({"password": configstoredPassword}, f)

def verifyPassword():
    with open(fullconfigPath, "r") as f:
        config = json.load(f)
    stored = base64.b64decode(config["password"]).decode()
    entered = getpass.getpass(yellow + "enter master password" + reset)
    if entered != stored:
        print(red + "incorrect" + reset)
        sys.exit(1)
    else:
        print("")


parser = argparse.ArgumentParser(description="adrians password generator")

parser.add_argument("-l", "--length", type=int, default=12,
                    help="define length of password, default = 12")

parser.add_argument("-i", "--integers", action="store_true",
                    help="include integers in password")

parser.add_argument("-b", "--symbolsBasic", action="store_true",
                    help="include symbols")

parser.add_argument("-a", "--symbolsExtra", action="store_true",
                    help="include more symbols, these are usually not allowed")
parser.add_argument("--showlist", action="store_true",
                    help = "decode stored and print to terminal")

args=parser.parse_args()

characterpool = string.ascii_letters

if args.symbolsBasic:
    characterpool += "!@#$%^&*-_"
    
if args.symbolsExtra:
    characterpool += "<>{}[]()\\//|`';"
    
if args.integers:
    characterpool += string.digits
    
if args.showlist:
    if not fullconfigPath.exists():
        firsttimesetup()
    else:
        verifyPassword()

    passwPath = os.path.expanduser(path)
    if not os.path.exists(passwPath):
        print(red + "no stored passwords" + reset)
        sys.exit(0)
    with open(passwPath, "r") as f:
        for eachLine in f:
            if "=" in eachLine:
                name, encodedpw = eachLine.strip().split(" = ")
                try:
                    decodedpw = base64.b64decode(encodedpw).decode()
                    print(f"{name} = " + green + f"{decodedpw}" + reset)
                except Exception as e:
                    print(f"{name} = " + red + f"invalid base64" + reset)
    sys.exit(0)


ask = input(green + "generation complete, press enter to show results \n" + reset)

generatedPassword =''.join(secrets.choice(characterpool) for _ in range(args.length))
storedPassword = base64.b64encode(generatedPassword.encode()).decode()

print(f"{generatedPassword}\n")


#passwPath = "data/passw"


while True:
    saveAsk = input(purple + "save password? y/n\n-> " + reset)
    if str(saveAsk) == "" :
        print("nothing entered")
        sys.exit(0)
        
    elif saveAsk[0] == "N" or saveAsk == "n":
        print("ok")
        sys.exit(0)
        
    elif saveAsk[0] == "y" or saveAsk[0] == "Y":
        print("")
        passwName = input(blue2 + "enter password name\n-> " + reset)

        path = "~/.datapw/data/passw"
        fullPath = os.path.expanduser(path)

        if not os.path.exists(fullPath):
          os.makedirs(os.path.dirname(fullPath))

        with open(fullPath, "a") as f:
               encodedPassword = base64.b64encode(generatedPassword.encode()).decode()
               f.write(f"(ENCODED) {passwName} = {encodedPassword}\n")
               break

#GAMMAL KOD

#with open(os.path.expanduser(os.path.join('~/.datapw/data/passw')), "a") as f:
#    f.write(f"{passwName} = {generatedPassword}\n")
#    print(blue + "\npassword saved in data/passw" + reset)


#with open("data/passw", "a") as f:
    #f.write(f"{passwName} = {generatedPassword}\n")
    #print(blue + "\npassword saved in data/passw" + reset)

#! @ # $ % ^ & * - _

#< > { } [ ] ( )
#\ / | `
#" '
#;