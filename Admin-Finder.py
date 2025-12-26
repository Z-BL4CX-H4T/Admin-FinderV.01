import requests
import threading
from queue import Queue
from colorama import Fore, Style, init
import random
import time

init(autoreset=True)

ascii_art = r"""
 █████  ██████  ███    ███ ██ ███    ██       ███████ ██ ███    ██ ██████  ███████ ██████
██   ██ ██   ██ ████  ████ ██ ████   ██       ██      ██ ████   ██ ██   ██ ██      ██   ██
███████ ██   ██ ██ ████ ██ ██ ██ ██  ██ █████ █████   ██ ██ ██  ██ ██   ██ █████   ██████
██   ██ ██   ██ ██  ██  ██ ██ ██  ██ ██       ██      ██ ██  ██ ██ ██   ██ ██      ██   ██
██   ██ ██████  ██      ██ ██ ██   ████       ██      ██ ██   ████ ██████  ███████ ██   ██

    Admin Finder v2 by ayiut Z-SH4DOWSPEECH
"""

admin_paths = [
    # Common
    "admin", "admin/login", "administrator", "adminpanel", "admin_area", "admin1", "admin2", "admincp",
    "adm", "cpanel", "controlpanel", "admin_login", "admin-login", "adminLogon", "adminLogin",
    "administrator/login", "administratorlogin", "siteadmin", "siteadmin/login", "webadmin",
    "webmaster", "moderator", "moderator/login", "panel", "dashboard", "auth/login", "login",
    "logon", "signin", "admin-signin", "admin-signin.php",

    # CMS-specific
    "wp-admin", "wp-login.php", "wp-admin/admin-ajax.php", "wp-admin/admin.php",
    "administrator/index.php?option=com_login", "administrator/index.php",
    "admin.php", "admin.html", "admin.asp", "admin.aspx", "admin.jsp",
    "login.php", "login.html", "login.asp", "login.jsp",

    # Frameworks & misc
    "user", "usuarios", "usuario", "memberadmin", "vue-element-admin", "processwire", "admin/dashboard",
    "adminarea", "admincontrol", "adminmaster", "adminmodule", "adminmanager", "adminmenu", "admin_media",
    "admin_messages", "admin_messages.php", "admin_news", "admin_news.php", "admin_new", "admin_log",
    "adminlist", "adminsignin", "admin_login.jsp", "admin_login.aspx", "admin_login.html",

    # International
    "acceso", "adminka", "administração", "administração/login", "administratorr", "adminpanel/login",
    "yonetici", "yonetici.php", "painel", "panel-administracion", "pan-admon", "beheer", "beheerder",
    "logowanie", "zaloguj", "dangnhap", "giris", "admin/giris",

    # Hosting/CPanel
    "webcp", "webadmin", "admincp/login", "cpanel/login", "hostadmin", "cpaneladmin",

    # Hidden/obscure
    "admin123", "secretadmin", "hiddenadmin", "adminaccess", "secureadmin", "privateadmin",
    "portal/admin", "secure/login", "dashboardadmin", "admin-console", "adminpanelv2",
    "manage/admin", "management", "manage", "backend", "securearea", "securelogin"
]

user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0)",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)",
    "Mozilla/5.0 (Windows NT 6.1; WOW64)"
]

queue = Queue()
results = []

def detect_cms(url):
    try:
        wp = requests.get(url + "/wp-login.php", timeout=5)
        if wp.status_code == 200:
            return "wordpress"
        joomla = requests.get(url + "/administrator", timeout=5)
        if joomla.status_code == 200:
            return "joomla"
    except:
        pass
    return "generic"

def scan_path(base_url, path):
    full_url = f"{base_url.rstrip('/')}/{path.lstrip('/')}"
    headers = {
        'User-Agent': random.choice(user_agents)
    }

    try:
        res = requests.get(full_url, headers=headers, timeout=7, allow_redirects=True)
        content_lower = res.text.lower()

        if res.status_code == 200 and any(keyword in content_lower for keyword in ['login', 'admin', 'dashboard']):
            print(f"{Fore.GREEN}[✓] Found: {full_url}")
            results.append(full_url)
        else:
            print(f"{Fore.RED}[✗] Not found: {full_url}")
    except Exception as e:
        print(f"{Fore.RED}[!] Error: {full_url} - {str(e)}")

def worker(base_url):
    while not queue.empty():
        path = queue.get()
        scan_path(base_url, path)
        queue.task_done()

def main():
    print(ascii_art)
    base = input("Enter target URL (example: http://example.com): ").strip()
    if not base.startswith("http"):
        base = "http://" + base

    print(f"\n{Fore.YELLOW}[INFO] Detecting CMS...")
    cms = detect_cms(base)
    print(f"{Fore.CYAN}[INFO] CMS detected: {cms}\n")

    for path in set(admin_paths):
        queue.put(path)

    thread_count = 10
    threads = []

    print(f"{Fore.YELLOW}[INFO] Scanning with {thread_count} threads...\n")
    for _ in range(thread_count):
        t = threading.Thread(target=worker, args=(base,))
        t.start()
        threads.append(t)

    queue.join()
    for t in threads:
        t.join()

    print(f"\n{Fore.GREEN if results else Fore.RED}[+] Scan Complete! {len(results)} admin page(s) found.")
    if results:
        with open("results.txt", "w") as f:
            for url in results:
                f.write(url + "\n")
        print(f"{Fore.BLUE}[✓] Results saved to results.txt")

if __name__ == "__main__":
    main()
