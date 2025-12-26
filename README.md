# Admin-FinderV.01

Admin Finder V.01 is a tool used to find admin pages on a website. It's like searching for a secret door in a big building.

How it works:
1. You enter the URL of the website you want to test.
2. The tool detects the CMS (like WordPress or Joomla) used by the website.
3. Then, it tries various common admin page paths.
4. If it finds an admin page, it displays it and saves it to results.txt.

Main uses:
- Testing website security by finding hidden admin pages.
- Helping security researchers find vulnerabilities.

Example use:
- Website admins can use it to ensure their admin pages are secure.
- Security researchers can use it to find weaknesses in websites.

# Installation for Linux:
```
python3 -m venv venv
source venv/bin/activate
sudo apt update -y
sudo apt upgrade -y
sudo apt install python2 -y
git clone https://github.com/Z-BL4CX-H4T/Admin-FinderV.01.git
cd Admin-FinderV.01
python3 Admin-Finder.py
```

# Installation for Termux:
```
pkg update && pkg upgrade -y
pkg install git -y
pkg install python2 -y
pkg install python -y
git clone https://github.com/Z-BL4CX-H4T/Admin-FinderV.01.git
cd Admin-FinderV.01
python2 Admin-Finder.py
```
