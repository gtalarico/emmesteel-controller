# Emmesteel

Library for connecting to Emmesteel Digital Heat Controller

## Network Setup

Use a raspberry pi as a proxy. Theor towel warmer device AP is very weak so I placed the pi in the bathroom (it's inside a metal box :face-palm:).

This makes the device more reachable from my entire home network

#### Setup Network Manager
```
sudo nmcli connection add type wifi ifname wlan1 con-name EMMESTEEL_<SERIAL> ssid EMMESTEEL_<SERIAL>
sudo nmcli connection modify EMMESTEEL_<SERIAL> wifi-sec.key-mgmt wpa-psk
sudo nmcli connection modify EMMESTEEL_<SERIAL> wifi-sec.psk "<PWD>"
sudo nmcli connection up EMMESTEEL_<SERIAL>
```

#### Setup Iptables

Setup Ip Forwarding
```
sudo sysctl net.ipv4.ip_forward
```
If not 1 use `sudo sysctl -w net.ipv4.ip_forward=1` and uncomment line in `/etc/sysctl.conf` to make it permanent`

```
sudo iptables -t nat -A PREROUTING -i wlan0 -p tcp --dport 80 -j DNAT --to-destination 192.168.X.X:80
sudo iptables -t nat -A POSTROUTING -o wlan1 -j MASQUERADE

sudo apt install iptables-persistent
sudo mkdir -p /etc/iptables
sudo iptables-save | sudo tee /etc/iptables/rules.v4
sudo nano /etc/rc.local
sudo iptables-restore < /etc/iptables/rules.v4
sudo chmod +x /etc/rc.local
sudo iptables-save > /etc/iptables/rules.v4
sudo reboot
```


## Checks & Debugging
1. Laptop can ping pi proxy
2. Pi is connected to `EMMESTEEL_` (iwconfig)
3. Pi can curl `192.168.1.1` which is `EMMESTEEL_` router ip.
4. Assuming the above is working and iptables routing is correct,
5. curl `<pi-ip>/` should return the emmesteel UI.
