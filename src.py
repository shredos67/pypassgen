#dräng code har error man kan ignorera
import string
import argparse
import os
import pathlib
import time
import secrets
import sys
from cryptography.fernet import Fernet

purple      = "\033[38;2;203;166;247m"
green       = "\033[38;2;166;227;161m"
reset       = "\033[0m"
red         = "\033[38;5;196m"
yellow      = "\033[38;5;220m"
blue        = "\033[38;2;137;180;250m"
blue2       = "\033[38;2;116;199;236m"


BASE_DIR = os.path.expanduser("~/.datapw")
PATH = os.path.join(BASE_DIR, "verysecretlist")
KEY_FILE = os.path.join(BASE_DIR, "verysecret.key")

def skapaKey():
    if os.path.exists(KEY_FILE):
        with open(KEY_FILE, "rb") as f:
            return f.read()
    else:
        os.makedirs(os.path.dirname(KEY_FILE), exist_ok=True)
    key = Fernet.generate_key()
    with open(KEY_FILE, "wb") as f:
        f.write(key)
    return key

def sparaPassword(name, password, fernet):
    encrypted = fernet.encrypt(password.encode())
    with open(PATH, "a") as f:
        f.write(f"{name} = {encrypted.decode()}\n")

def listPasswords(fernet):
    with open(PATH, "r") as f:
        for line in f:
            if " = " not in line:
                print(f"Invalid line format: {line.strip()}")
                continue
            name, encrypted = line.strip().split(" = ", 1)
            try:
                decrypted = fernet.decrypt(encrypted.encode()).decode()
                print(f"{name} = {decrypted}")
            except Exception as e:
                print(f"Error decrypting {name}: {e}")






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
    if not os.path.exists(PATH):
        print(red + "no stored passwords" + reset)
        sys.exit(0)
    else:
        key = skapaKey()
        fernet = Fernet(key)
        listPasswords(fernet)
        sys.exit(0)


input(green + "generation complete, press enter to show results \n" + reset)

generatedPassword =''.join(secrets.choice(characterpool) for _ in range(args.length))

print(generatedPassword)



#passwPath = "data/passw"



while True:
    saveAsk = input(purple + "save password? y/n\n-> " + reset)
    if str(saveAsk) == "" :
        print("nothing entered")
        sys.exit(0)
        
    elif saveAsk[0] == "N" or saveAsk[0] == "n":
        print("ok")
        sys.exit(0)
        
    elif saveAsk[0] == "y" or saveAsk[0] == "Y":
        passwName = input(green + "name for password\n-> " + reset)
        
        with open(PATH, "a") as f:
            key = skapaKey()
            fernet = Fernet(key)
            sparaPassword(passwName, generatedPassword, fernet)
            print(blue + "\npassword saved in data/verysecretlist" + reset)
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
