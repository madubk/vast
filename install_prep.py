cnode_prefix="cnode"
dnode_prefix="dnode"

subnet='10.30.10.'
starting_ip = 82
vmsip = subnet + str(starting_ip)
dns1 = "10.10.0.13"
dns2 = "10.10.0.14"
ntp1 = "10.10.0.100"
ntp2 = "10.10.0.101"
mgw = "10.30.8.1"
internalmtu = "9000"
ibmtu = "4200"
mnetmask = "255.255.252.0"

docker_subnet = "172.21.0.0\/24" # forward slash for CIDR subnet must be escaped with backslash

cnodes = 8
dnodes = 4

incr = 0

for cnode in range(cnodes):
	incr+=1
	node = cnode + 1
	hostname = cnode_prefix + str(f'{node:02}')
	cn=str(cnode+1)
	cnip=subnet + str(incr + starting_ip)
	incr+=1
	cnipmi=subnet + str(incr + starting_ip)
	vmsip = subnet + str(starting_ip)
	string0 = f"#cn {cn}" #comment line for node number
	string1 = f"CN='{cnip}' CNIPMI='{cnipmi}' NODE='{cn}' HOSTNAME='{hostname}'" #dynamic variable definition line
	string2 = f"MNETMASK='{mnetmask}' DNS1='{dns1}' DNS2='{dns2}' NTP1='{ntp1}' NTP2='{ntp2}' MGW='{mgw}' VMSIP='{vmsip}' INTERNALMTU='{internalmtu} IBMTU='{ibmtu}'" #static variable definition line
	string3 = "sudo configure_network.py $NODE --ext-interface eno1 --ext-ip $CN --ext-netmask $MNETMASK --ext-dns $DNS1 $DNS2 --ntp $NTP1 $NTP2 --ext-gateway $MGW --hostname $HOSTNAME --mgmt-vip $VMSIP --eth-mtu $INTERNALMTU --technician-interface eno2 --ipmi-ip $CNIPMI --ipmi-netmask $MNETMASK --ipmi-gateway $MGW --template '172.20.{network}.{node} --mgmt-inner-vip 172.20.4.254" #config line
	dockermod1 = "sudo cp /etc/docker/daemon.json /home/vastdata/daemon.json.bak"
	dockermod2 = "sudo sed -ie '/insecure-registries/ s/{/{\"bip\": \"172.21.0.0\/16\", /' /etc/docker/daemon.json"
	print(string0)
	print(string1)
	print(string2)
	print(string3)
	print(dockermod1)
	print(dockermod2)
	print()


print()

for dnode in range(dnodes):
	incr+=1
	node = dnode + 1
	hostname = dnode_prefix + str(f'{node:02}')
	dn=str(dnode+1)
	dnip=subnet + str(incr + starting_ip)
	incr+=1
	dnipmi=subnet + str(incr + starting_ip)
	string0 = f"#dn {dn}" #comment line for node number
	string1 = f"CN='{dnip}' CNIPMI='{dnipmi}' NODE='{dn}' HOSTNAME='{hostname}'" #dynamic variable definition line
	string2 = f"MNETMASK='{mnetmask}' DNS1='{dns1}' DNS2='{dns2}' NTP1='{ntp1}' NTP2='{ntp2}' MGW='{mgw}' VMSIP='{vmsip}' INTERNALMTU='{internalmtu}'" #static variable definition line
	string3 = "sudo configure_network.py $NODE --ext-interface eno1 --ext-ip $CN --ext-netmask $MNETMASK --ext-dns $DNS1 $DNS2 --ntp $NTP1 $NTP2 --ext-gateway $MGW --hostname $HOSTNAME --mgmt-vip $VMSIP --eth-mtu $INTERNALMTU  --technician-interface eno2 --ipmi-ip $CNIPMI --ipmi-netmask $MNETMASK --ipmi-gateway $MGW" #config line
	dockermod1 = "sudo cp /etc/docker/daemon.json /home/vastdata/daemon.json.bak"
	dockermod2 = "sudo sed -ie '/insecure-registries/ s/{/{\"bip\": \"172.21.0.0\/16\", /' /etc/docker/daemon.json"
	print(string0)
	print(string1)
	print(string2)
	print(string3)
	print(dockermod1)
	print(dockermod2)
	print()




