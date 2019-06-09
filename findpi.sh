sudo nmap -sP 192.168.0.*/24 | awk '/^Nmap/{ip=$NF}/B8:27:EB/{print ip}'
