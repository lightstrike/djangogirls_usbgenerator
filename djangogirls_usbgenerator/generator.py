import requests
import re
import os
import cgi
from clint.textui import progress
import subprocess
from pyfiglet import Figlet


def download_steps():
    """Launch the different downloading function"""
    introduction()
    print("Do you want to download the tutorial?")
    yes_no(tutorial)
    print("Do you want to download Bootstrap?")
    yes_no(bootstrap)
    print("Do you want to download Lobster font?")
    yes_no(lobster)
    print("Do you want to download Python?")
    yes_no(python)
    print("Do you want to download Django?")
    yes_no(django)
    print("Do you want to download code editors?")
    yes_no(code_editors)
    print("You're done! Bye :)")


def introduction():
    f = Figlet(font='standard')
    print(f.renderText('Django Girls'))
    print("""This script will help you to download everything you need for the workshop in case there is no Internet.
Valid answers for each step: yes, y, enter or no, n.
Enter q to quit.\n""")


def download_file(address, folder):
    """Function for downloading stuff"""
    try:
        os.mkdir("downloads")
    except FileExistsError:
        pass
    r = requests.get(address, stream=True)
    if "Content-Disposition" in r.headers:
        _, params = cgi.parse_header(r.headers["Content-Disposition"])
        name = params["filename"]
    else:
        name = address.split("/")[-1]
    total_length = int(r.headers.get('content-length'))
    with open(folder+"/"+name, "wb") as f:
        for chunk in progress.bar(r.iter_content(1024), expected_size=(total_length/1024) + 1):
            if chunk:
                f.write(chunk)
                f.flush()


def yes_no(function):
    """Function to give user the choice to skip a step"""
    choice = input()
    if choice in ("yes", "y", ""):
        function()
    elif choice in ("no", "n"):
        print("Ok, let's move to the next step!")
    elif choice in ("q"):
        print("Goodbye :)")
        exit()
    else:
        print("I didn't understand your answer. Please, enter yes or no:")
        yes_no(function)


def list_tutorial_languages():
    """Create a list with all the languages available for the tutorial"""
    r = requests.get("https://www.gitbook.com/download/pdf/book/djangogirls/djangogirls-tutorial")
    tutorials = re.findall(r"\?lang=(.{2})\">([^<]*)<", r.text)
    return dict(tutorials)


def tutorial():
    """Download tutorial, multiple languages possible"""
    tutorials = list_tutorial_languages()
    print("Translations available %s. \nPlease, enter your choice (2 letters language code). If multiple choices, use space as a separator." %tutorials)
    while True:
        choice = input().split()
        if all(i in tutorials for i in choice):
            break
        else:
            print("2 letters code not recognized. Choose again in this list: %s" %tutorials)
    for i in choice:
        download_file("https://www.gitbook.com/download/pdf/book/djangogirls/djangogirls-tutorial?lang=%s" %i, "downloads/")
        print("%s tutorial downloaded" %tutorials[i])


def bootstrap():
    """Download Bootstrap"""
    r = requests.get("http://getbootstrap.com/getting-started")
    m = re.search(r'<a href="([^"]*)"[^>]*>Download Bootstrap</a>', r.text)
    if m:
        link = m.group(1)
        download_file(link, "downloads/")
        print("Bootstrap downloaded.")
    else:
        print("Failed to find download URL for Bootstrap. Falling back to hardcoded download link.")
        download_file("https://github.com/twbs/bootstrap/releases/download/v3.3.5/bootstrap-3.3.5-dist.zip", "downloads/")

def lobster():
    download_file("http://dl.dafont.com/dl/?f=lobster", "downloads/")
    print("Lobster font downloaded.")

def python():
    download_file("https://www.python.org/ftp/python/3.4.3/python-3.4.3.msi", "downloads/")
    print("Python for Windows 32bits downloaded.")
    download_file("https://www.python.org/ftp/python/3.4.3/python-3.4.3.amd64.msi", "downloads/")
    print("Python for Windows 64bits downloaded.")
    download_file("https://www.python.org/ftp/python/3.4.3/python-3.4.3-macosx10.6.pkg", "downloads/")
    print("Python for Mac downloaded.")


def django():
    subprocess.check_call("pip install django==1.8 --download downloads", shell=True)
    print("Django downloaded.")


def code_editors():
    print("Do you want to download Sublime Text 2?")
    yes_no(sublime_text)
    print("Do you want to download Atom (64bits)?")
    yes_no(atom)


def sublime_text():
    """Download multiple code editor"""
    download_file("http://c758482.r82.cf2.rackcdn.com/Sublime Text 2.0.2 Setup.exe", "downloads/")
    print("Sublime Text 2 for Windows downloaded.")
    download_file("http://c758482.r82.cf2.rackcdn.com/Sublime Text 2.0.2.dmg", "downloads/")
    print("Sublime Text 2 for Mac downloaded.")
    download_file("http://c758482.r82.cf2.rackcdn.com/Sublime Text 2.0.2.tar.bz2", "downloads/")
    print("Sublime Text 2 for Linux downloaded.")


def atom():
    """Download multiple code editor"""
    download_file("https://github.com/atom/atom/releases/download/v1.0.5/AtomSetup.exe", "downloads/")
    print("Atom for Windows downloaded.")
    download_file("https://github.com/atom/atom/releases/download/v1.0.5/atom-mac.zip", "downloads/")
    print("Atom for Mac downloaded.")
    download_file("https://github.com/atom/atom/releases/download/v1.0.5/atom-mac-symbols.zip", "downloads/")
    print("Atom-symbols for Mac downloaded.")
    download_file("https://github.com/atom/atom/releases/download/v1.0.5/atom.x86_64.rpm", "downloads/")
    print("Atom.rpm downloaded.")
    download_file("https://github.com/atom/atom/releases/download/v1.0.5/atom-amd64.deb", "downloads/")
    print("Atom.deb downloaded.")

if __name__ == '__main__':
    download_steps()
