# Emmesteel

Library for connecting to Emmesteel Digital Heat Controller.
This is the Digital Controller used in the italian-made towel warmers sold by [Amba](https://ambaproducts.com/) like the modello i, etc

## Background

### No Wifi Config Possible
The uses a dedicated Wifi AP for user-device control but it does not allow you to provide a wifi setting for the device to use.
To make any changes to the device settings or remotely control it, you must always temporarily connec to the device AP.

### No Scheduling
Furthermore, the software does not allowing scheduling start/end, only a shut-off timer.

### Solution
To get around these limitation, I developed a library that can communicate and control the device and a Home Assistant Integration to manage it.
For the Wifi AP problem, I decided to use a RaspberryPi as a proxy. The Pi connects to both wifi networks simutaneously, and then proxies home network requests to the device via the device's custome wifi network.

The Pi proxy also helps solve a very low wifi signal that is caused by the controller being inside a metal junction box.

## Network Setup - Summary
1. Setup a RaspberryPi with default OS and connect it to your home wifi
2. Use NetworkManager and a second wifi dongle to connect the pi to the towel warmer SSID (e.g. `EMMESTEEL_24TS00112`)
3. Use iptables to proxy home network requests to the device on `EMMESTEEL_24TS00112`

### Step-by-step

#### Network Manager
```
sudo nmcli connection add type wifi ifname wlan1 con-name EMMESTEEL_<SERIAL> ssid EMMESTEEL_<SERIAL>
sudo nmcli connection modify EMMESTEEL_<SERIAL> wifi-sec.key-mgmt wpa-psk
sudo nmcli connection modify EMMESTEEL_<SERIAL> wifi-sec.psk "<PWD>"
sudo nmcli connection up EMMESTEEL_<SERIAL>
```

#### Iptables

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

## Verify
1. Laptop can ping pi proxy
2. Pi is connected to `EMMESTEEL_` (iwconfig)
3. Pi can curl `192.168.1.1` which is `EMMESTEEL_` router ip.
4. Assuming the above is working and iptables routing is correct,
5. curl `<pi-ip>/` should return the emmesteel UI.

## Take Control

Finally, you can use the `home-assistant` custom integration to see the status, power on/off, adjust heating level, etc.

