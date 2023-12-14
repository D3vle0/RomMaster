import sys
import os
import time
import subprocess
from colorama import init as colorama_init
from colorama import Fore
from colorama import Style
colorama_init()


print(f"[*] Drag {Fore.YELLOW}TWRP recovery file {Style.RESET_ALL}into the terminal: ")
recovery = input().replace('\\ ', ' ').replace("'", ' ').strip()
if not os.path.exists(recovery):
    print(f"{Fore.RED}[-] Not existing file.")
    sys.exit(1)
print(f"[*] Drag {Fore.YELLOW}firmware file {Style.RESET_ALL}into the terminal: ")
firmware = input().replace('\\ ', ' ').replace("'", ' ').strip()
res=str(subprocess.check_output(['adb', 'devices']))
try:
    if len(res.split('attached\\n')[1]) > 8:
        device = res.split('attached\\n')[1][:8]
        print(f"{Fore.GREEN}[+] Device found:{Style.RESET_ALL}", device)
except:
    print(f"{Fore.RED}[-] An error occurred.")
    sys.exit(1)

os.system("adb reboot-bootloader > /dev/null")
while 1:
    time.sleep(3)
    if bytes(device, 'utf-8') in subprocess.check_output(['fastboot', 'devices']):
        os.system(f"fastboot boot {recovery} > /dev/null")
        break
print(f"{Fore.GREEN}[+] Booted into recovery.{Style.RESET_ALL}")

while 1:
    time.sleep(3)
    res=str(subprocess.check_output(['adb', 'devices']))
    try:
        if len(res.split('attached\\n')[1]) > 8:
            break
    except:
        print(f"{Fore.RED}[-] An error occurred.")
        sys.exit(1)

print("[*] Wiping cache...")
os.system("adb shell twrp wipe cache > /dev/null")
time.sleep(1)
print("[*] Wiping dalvik...")
os.system("adb shell twrp wipe dalvik > /dev/null")
time.sleep(1)
print("[*] Wiping system...")
os.system("adb shell twrp wipe system > /dev/null")
time.sleep(1)
print("[*] Wiping data...")
os.system("adb shell twrp wipe data > /dev/null")
time.sleep(1)
p = subprocess.Popen("adb shell twrp format data > /dev/null", shell=True, stdout=subprocess.PIPE)
p.wait()
print("[*] Copying firmware...")
p = subprocess.Popen(f"adb push {firmware} /data/rom.zip", shell=True, stdout=subprocess.PIPE)
p.wait()
print("[*] Flashing firmware...")
p = subprocess.Popen("adb shell twrp install /data/rom.zip", shell=True, stdout=subprocess.PIPE)
p.wait()
os.system("adb reboot > /dev/null")
print(f"{Fore.GREEN}[+] Done!")