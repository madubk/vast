import os
from netmiko import ConnectHandler
import time
import subprocess
import paramiko



def getMacTableFromFile(filename):
    print("Starting function: getMacsFromFile")
    f = open(filename, 'r')
    result = f.read() #get mac table from text file
    f.close()
    lines = result.split("\n")
    #maclines = macFormat(lines)
    #macs = macFormatString(result)
    #print(macs)
    return(lines)
    #return(macs)

def getMacTableFromSwitch(device):
    print("Starting function: getMacsFromSwitch")
    ssh_connect = ConnectHandler (**device)
    ssh_connect.enable()
    #ssh_connect.send_command('skip')
    #print("skip")
    #result = ssh_connect.send_command('show mac-address') #get mac table from switch
    result = ssh_connect.send_command('show mac address-table dynamic') #get mac table from switch
    lines = result.split("\n")
    #for line in lines:
    #    print(line)
    #maclines = macFormat(lines)
    macs = []
    #for mac in maclines:
    #    macs.append(mac[0])
    return(lines)
    #return(macs)

def macFormatString(lines):
    import re
    #macs = re.findall("[a-zA-Z0-9_]{4}\.[a-zA-Z0-9_]{4}\.[a-zA-Z0-9_]{4}", result)
    #print(macs)
    #port_filter = '1/1/' #brocade interface filter
    port_filter = 'Gi' #cisco interface filter
    for line in lines:
        if port_filter in line:
            macEntry = line.split()
            mac = macEntry[1] #cisco
            #mac = macEntry[0] #brocade
            port = macEntry[3] #cisco
            #port = macEntry[1] #brocade
            mac = mac[:2] + '.' + mac[2:7] + '.' + mac[7:12] + '.' + mac[12:]
            mac = mac.replace('.', ':')
            maclines.append((mac, port))
    #maclines.sort(key=lambda y: y[1])
    return(maclines)


def macFormat(lines):
    #print(lines)
    import re
    mymacs = []
    themacs = {}
    for line in lines:
        macaddr = ""
        macaddr = re.findall("[a-zA-Z0-9]{4}\.[a-zA-Z0-9_]{4}\.[a-zA-Z0-9_]{4}", line)
        #if not macaddr:
        #    re.findall("[a-zA-Z0-9:-]{2}{6}", line)
        #interface = re.findall("Gi[0-9]\/[0-9]\/[0-9]", line)
        interface = re.findall("Gi[0-9]\/[0-9]\/[0-9]+", line)
        #macaddr = re.match("[a-zA-Z0-9_]{4}\.[a-zA-Z0-9_]{4}\.[a-zA-Z0-9_]{4}", line)
        #interface = re.match("Gi[0-9]\/[0-9]", line)
        if macaddr:
            #mymacs.append({"macaddr": macaddr.group(), "interface": interface.group()})
            mac = macaddr[0]
            mac = mac[:2] + '.' + mac[2:7] + '.' + mac[7:12] + '.' + mac[12:]
            mac = mac.replace('.', ':')
            #maclines.append((mac, port))
            #mymacs.append({"macaddr": macaddr[0], "interface": interface[0]})
            ###only taking first mac entry
            if not any(d['interface'] == interface[0] for d in mymacs):
                ipv6 = macToIpv6(mac)
                mymacs.append({"macaddr": mac, "interface": interface[0], 'ipv6': ipv6})
            #mymacs.append({"macaddr": mac, "interface": interface[0]})
            #print("interface:", interface.group())
            pass
    maclines=[]
    #port_filter = '1/1/' #brocade interface filter
    port_filter = 'Gi' #cisco interface filter
    for line in lines:
        if port_filter in line:
            macEntry = line.split()
            mac = macEntry[1] #cisco
            #mac = macEntry[0] #brocade
            port = macEntry[3] #cisco
            #port = macEntry[1] #brocade
            mac = mac[:2] + '.' + mac[2:7] + '.' + mac[7:12] + '.' + mac[12:]
            mac = mac.replace('.', ':')
            maclines.append((mac, port))
    #maclines.sort(key=lambda y: y[1])
    mymacs.sort(key=lambda y: y['interface'])
    #print("mymacs:", str(mymacs))
    #return(maclines)
    return(mymacs)

def macToIpv6(mac):
    macsplit = mac.split(':')
    macsplit.insert(3, "fe")
    macsplit.insert(3, "ff")

    aug = hex(int('0x' + macsplit[0], 16))[2:]
    #print()
    #print("macsplit[0]", macsplit[0])
    #print("aug", aug)
    test = int(aug,16)%4
    #print("test", test)
    if test < 2:
        new = hex(int (macsplit[0], 16)+2)[2:]
        #print(aug + ": " + str(test) + " + 2 >> " + new)
    else:
        new = hex(int (macsplit[0], 16)-2)[2:]
        #print(aug + ": " + str(test) + " - 2 >> " + new)
    macsplit[0] = new
    v6array = []
    for i in range(len(macsplit)):
        if i%2 == 0 and i+1%(len(macsplit))>0:
            v6array.append(macsplit[i] + macsplit[i+1])

    v6array.insert(0, '')
    v6array.insert(0, 'fe80')
    v6 = ":".join(v6array)
    #print(v6)
    return(v6)


def setIpFromTech():
    username = 'madu'  #should be 'vastdata' when on cnode or dnode
    password = 'pass'  #should be 'vastdata' when on cnode or dnode

    tech = '192.168.2.2'
    prefix = '192.168.2.'

    for m in range(len(macs)):
        mac = macs[m]['macaddr']
        #ip = prefix + str(m+20)
        ip = macToIpv6(mac)
        #print(f"{ip} > {mac}")
        #arp = subprocess.check_output(f"arp -ane {tech}", shell=True).decode()
        #if tech in arp: os.system(f"sudo arp -d {tech}")
        #os.system(f"sudo arp -s {tech} {mac}")

        hostname='XXXXXXXXX'
        subsystem = '8888'
        mgmt = '2.2.2.2'
        ipmi='1.1.1.1'


        #command = f"sudo configure_network.py 1 --subsystem {subsystem} --ext-interface eno2 --ext-ip {mgmt} --ext-gateway 10.25.255.254 --ext-dns 10.2.100.34 10.2.100.35 --ntp clock1.tgsw clock2.tgsw --ext-netmask 255.255.0.0 --hostname {hostname} --mgmt-vip 10.25.30.1  --internal-interfaces ib0,ib1 --internal-virtual-interfaces ib2,ib3 --external-interfaces enp59s0f0,enp59s0f1 --ib-mode connected --ipmi-ip {ipmi} --ipmi-netmask 255.255.0.0 --ipmi-gateway 10.23.255.254 --skip-fw --ext-rp-filter=2"
        command = f'--subsystem {subsystem} --ext-ip {mgmt} --hostname {hostname} --ipmi-ip {ipmi}'
        print(command)


        try:
            client = paramiko.SSHClient()
            client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            #client.connect(tech, 22, username, password)
            client.connect(ip, 22, username, password)
            stdin, stdout, stderr = client.exec_command('hostname')
            print(stdout.read().decode('utf-8'))
            #stdin, stdout, stderr = client.exec_command(f'python3 configure_network.py ')
            stdin, stdout, stderr = client.exec_command(f'echo {command}')
            print(stderr.read().decode('utf-8'))
            client.close()
        except TypeError as e:
            print(e)
    #time.sleep(3)
    #for i in range(len(macs)):
    #    m = i+20
    #    print(f'192.168.2.{m}')
    #    os.system(f'ping -c 1 -i 0.2 -M do -s 1000 192.168.2.{m}|grep loss')


def setIpFromIpv6(ipv6, extIp, hostname, nodeId, ipmi, subsystem):
    print("Running method: Setting IP from IPv6")
    ip = ipv6
    localIntMod = '%enp0s9'
    username = 'madu'  #should be 'vastdata' when on cnode or dnode
    password = 'pass'  #should be 'vastdata' when on cnode or dnode


    #hostname='XXXXXXXXX'
    #subsystem = '8888'
    #mgmt = '2.2.2.2'
    #ipmi='1.1.1.1'


    #old command
    #command = f"sudo configure_network.py {nodeId} --subsystem {subsystem} --ext-interface eno2 --ext-ip {extIp} --ext-gateway 10.25.255.254 --ext-dns 10.2.100.34 10.2.100.35 --ntp clock1.tgsw clock2.tgsw --ext-netmask 255.255.0.0 --hostname {hostname} --mgmt-vip 10.25.30.1  --internal-interfaces ib0,ib1 --internal-virtual-interfaces ib2,ib3 --external-interfaces enp59s0f0,enp59s0f1 --ib-mode connected --ipmi-ip {ipmi} --ipmi-netmask 255.255.0.0 --ipmi-gateway 10.23.255.254 --skip-fw --ext-rp-filter=2"
    command = f"sudo configure_network.py {nodeId} --subsystem {subsystem} --ext-interface eno2 --ext-ip {extIp} --ext-gateway 192.168.11.254 --ext-dns 192.168.9.251 192.168.9.252 --ntp clock1.tgsw clock2.tgsw --ext-netmask 255.255.254.0 --hostname {hostname} --mgmt-vip 192.168.9.253  --internal-interfaces ib0,ib1 --internal-virtual-interfaces ib2,ib3 --external-interfaces enp59s0f0,enp59s0f1 --ib-mode connected --ipmi-ip {ipmi} --ipmi-netmask 255.255.254.0 --ipmi-gateway 192.168.11.254 --skip-fw --ext-rp-filter=2"
    #command = f'$(hostname) --subsystem {subsystem} --ext-ip {mgmt} --hostname {hostname} --ipmi-ip {ipmi}'
    print("command to run: ", command)


    #try:
    #    client = paramiko.SSHClient()
    #    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    #    #client.connect(tech, 22, username, password)
    #    client.connect(ip+localIntMod, 22, username, password, timeout=10)
    #    stdin, stdout, stderr = client.exec_command('hostname')
    #    print(stdout.read().decode('utf-8'))
    #    #stdin, stdout, stderr = client.exec_command(f'python3 configure_network.py ')
    #    stdin, stdout, stderr = client.exec_command(f'echo {command}')
    #    print(stderr.read().decode('utf-8'))
    #    client.close()
    #except TypeError as e:
    #    print(e)





device = {
'device_type': 'cisco_ios',
'ip': '192.168.2.254',
'username': 'admin',
'password': 'admin',
'port' : 22,
'secret': 'admin',
}


#filename = 'cisco_mac_table.txt'
filename = 'dummy_mac_table.txt'
#macs = getMacTableFromSwitch(device)
#macs = getMacTableFromFile(filename)
macTable = getMacTableFromFile(filename)
#macTable = getMacTableFromSwitch(device)
macs = macFormat(macTable)
cnode = -1
subsystem = -1
for mac in macs:
    cnode += 1
    ip = mac['ipv6']
    ipv6 = ip
    #nodeId = int((cnode)%24+int((cnode+1)/24))
    nodeId = int(cnode%24+1)
    hostname = "cnode" + str(nodeId)
    extIp = "192.168.8." + str(nodeId)
    ipmi = "192.168.10." + str(cnode)
    if nodeId == 1:
        subsystem += 1
    ipv6, extIp, hostname, nodeId, ipmi, subsystem
    #print(mac)
    #print(ip)
    ##os.system(f'ping6 -c 1 -i 0.2 {ip}|grep loss')
    #os.system(f'ping6 -I enp0s3 -c 1 {ip}')
    ###tech = "192.168.2.2"
    ###arp = subprocess.check_output(f"arp -ane {tech}", shell=True).decode()
    ###if tech in arp: os.system(f"sudo arp -d {tech}")
    ###os.system(f'ping -c 1 -i 0.2 -M do -s 1000 192.168.2.2|grep loss')
    #os.system(f'ping6 -I enp0s9 -c 1 {ip}')
    #setIpFromIpv6(ip)
    setIpFromIpv6(ipv6, extIp, hostname, nodeId, ipmi, subsystem)



#setIpFromTech()


