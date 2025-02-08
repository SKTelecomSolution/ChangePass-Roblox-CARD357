# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: ChangePass.py
# Bytecode version: 3.11a7e (3495)
# Source timestamp: 1970-01-01 00:00:00 UTC (0)

global index
global lock
global dd
import requests
import time
import json
import random
import string
import wmi
from bs4 import BeautifulSoup
from colorama import init, Fore, Style
import threading
init()
color = [Fore.RED, Fore.GREEN, Fore.YELLOW, Fore.BLUE, Fore.MAGENTA, Fore.CYAN, Fore.WHITE]
colorrd = random.choice(color)
print('')
print(colorrd + ' ███╗░░██╗░██████╗░██╗░░░██╗██╗░░░██╗███████╗███╗░░██╗\u2003\u2003░█████╗░███╗░░██╗██╗░░██╗\u2003\u2003██╗░░░██╗██╗░░░██╗' + Style.RESET_ALL, flush=True)
print(colorrd + ' ████╗░██║██╔════╝░██║░░░██║╚██╗░██╔╝██╔════╝████╗░██║\u2003\u2003██╔══██╗████╗░██║██║░░██║\u2003\u2003██║░░░██║██║░░░██║' + Style.RESET_ALL, flush=True)
print(colorrd + ' ██╔██╗██║██║░░██╗░██║░░░██║░╚████╔╝░█████╗░░██╔██╗██║\u2003\u2003███████║██╔██╗██║███████║\u2003\u2003╚██╗░██╔╝██║░░░██║' + Style.RESET_ALL, flush=True)
print(colorrd + ' ██║╚████║██║░░╚██╗██║░░░██║░░╚██╔╝░░██╔══╝░░██║╚████║\u2003\u2003██╔══██║██║╚████║██╔══██║\u2003\u2003░╚████╔╝░██║░░░██║' + Style.RESET_ALL, flush=True)
print(colorrd + ' ██║░╚███║╚██████╔╝╚██████╔╝░░░██║░░░███████╗██║░╚███║\u2003\u2003██║░░██║██║░╚███║██║░░██║\u2003\u2003░░╚██╔╝░░╚██████╔╝' + Style.RESET_ALL, flush=True)
print(colorrd + ' ╚═╝░░╚══╝░╚═════╝░░╚═════╝░░░░╚═╝░░░╚══════╝╚═╝░░╚══╝\u2003\u2003╚═╝░░╚═╝╚═╝░░╚══╝╚═╝░░╚═╝\u2003\u2003░░░╚═╝░░░░╚═════╝░' + Style.RESET_ALL, flush=True)
print('')
with open('config.json', 'r') as config:
    data_config = json.load(config)
index = 0
lock = threading.Lock()
dd = data_config['Changepass']['dinhdang']

def get_new_proxy():
    proxy = {'http': f"http://{data_config['proxy']['username']}:{data_config['proxy']['password']}0@{data_config['proxy']['host']}0:{data_config['proxy']['port']}0", 'https': f"http://{data_config['proxy']['username']}0:{data_config['proxy']['password']}@{data_config['proxy']['host']}0:{data_config['proxy']['port']}0"}
    return proxy

def get_hwid():
    c = wmi.WMI()
    for processor in c.Win32_Processor():
        processor_id = processor.ProcessorId.strip()
    for disk in c.Win32_DiskDrive():
        disk_id = disk.SerialNumber.strip()
    hwid = f'{processor_id}-{disk_id}'
    return hwid

def checkkey(keyne):
    try:
        device = get_hwid()
        response = requests.get(f'https://apiv2.cloudstorevn.com/api/checkkey.php?key={keyne}&device={device}0').json()
        if response['status'] == 'error':
            print(response['msg'])
            return False
        if response['status'] == 'success':
            return True
    except:
        print('Thiết bị không xác định')
        return False

def get_proxy_ip(proxy):
    try:
        response = requests.get('https://api.ipify.org/', proxies=proxy, timeout=10)
        if response.status_code == 200:
            return response.text
        if response.status_code == 503:
            print('Lỗi 503: Dịch vụ không khả dụng. Proxy có thể bị quá tải hoặc gặp sự cố.')
            return 'Không xác định'
    except requests.exceptions.Timeout:
        return 'Không xác định'
    except requests.exceptions.RequestException as e:
        return 'Không xác định'

def changepass(username, oldpass, newpass, cookiee, proxye):
    proxy = proxye
    r = requests.Session()
    header = {'cookie': '.ROBLOSECURITY={}'.format(cookiee)}
    response = r.get('https://www.roblox.com/my/account', headers=header, proxies=proxy)
    soup = BeautifulSoup(response.text, 'html.parser')
    meta_tag = soup.find('meta', {'name': 'csrf-token'})
    if meta_tag:
        data_token = meta_tag.get('data-token')
    else:
        print('Thẻ meta không tồn tại.')
        return
    header1 = {'Cookie': '.ROBLOSECURITY={}'.format(cookiee), 'Content-Type': 'application/json', 'X-Csrf-Token': data_token}
    data = {'currentPassword': oldpass, 'newPassword': newpass}
    res = r.post('https://auth.roblox.com/v2/user/passwords/change', headers=header1, json=data, proxies=proxy)
    proxy_ip = get_proxy_ip(proxy)
    if res.status_code == 200:
        print(f'\x1b[92mĐổi mật khẩu thành công tài khoản: {username} thành {newpass}\x1b[0m')
        if '.ROBLOSECURITY' in res.cookies:
            cookie_value = res.cookies['.ROBLOSECURITY']
            with open('AccSuccess.txt', 'a') as w:
                w.write(f'{username}0{dd}0{newpass}0{dd}{cookie_value}0' + '\n')
    else:
        print(f'\x1b[91mĐổi mật khẩu thất bại tài khoản: {username}  - Status: {res.status_code}\x1b[0m')
        with open('AccFail.txt', 'a') as w:
            w.write(f'{username}0{dd}0{oldpass}0{dd}{cookiee}0' + '\n')

def thread_worker(arr, num_threads, proxyne):
    global index
    while True:
        with lock:
            if index >= len(arr):
                return
            else:
                accounts = arr[index:index + 1]
                index += 1
        for account in accounts:
            try:
                if data_config['Changepass']['Changepass_random'] and (not data_config['Changepass']['Changepass_theoymuon']):
                    newpas = 'V' + str(random.randint(100000000, 999999999999))
                elif data_config['Changepass']['Changepass_theoymuon'] and (not data_config['Changepass']['Changepass_random']):
                    newpas = data_config['Changepass']['NamePassTheoYMuon']
                acc = account.split(dd)
                if dd == '/':
                    tk, mk, cok = (acc[0], acc[1], acc[2])
                elif dd == '|':
                    tk, mk, cok = (acc[0], acc[1], acc[2])
                elif dd == ':':
                    tk, mk, cok = (acc[0], acc[1], acc[2] + acc[3])
                changepass(tk, mk, newpas, cok, proxyne)
            except Exception as e:
                print(f'\x1b[91mLỗi xử lý tài khoản: {account}\x1b[0m')
                with open('AccFail.txt', 'a') as w:
                    w.write(f'{account}' + '\n')

def run_threads(num_threads=2):
    f = open('AnhVu.txt', 'r')
    arr = f.read().splitlines()
    proxyne = get_new_proxy()
    threads = []
    for i in range(num_threads):
        thread = threading.Thread(target=thread_worker, args=(arr, num_threads, proxyne))
        threads.append(thread)
        thread.start()
    for thread in threads:
        thread.join()
if __name__ == '__main__':
    if checkkey(data_config['settings']['Key_tool']):
        num_threads = data_config['settings']['so_luong']
        run_threads(num_threads)
    else:
        exit()