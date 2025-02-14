# Emmesteel

Library for connecting to Emmesteel Digital Heat Controller.
This is the Digital Controller used in the italian-made towel warmers sold by [Amba](https://ambaproducts.com/) like the modello i, etc

## Motivation

They make nice towel warmers for sure, but for a $300 controller the "smart" side of this controller failed to deliver.

#### No Home Network
The device spins up its own Wifi AP and once connected, it launched a UI to control it using a captive portal.
It does not allow you to provide a wifi settings. To make any changes to the device settings or remotely control it,
you must always temporarily connec to the device AP.

#### No Scheduling
They only controls offered are on/off, temperature and a count down shut-off timer.
 It does not allow scheduling start/end times so you can, for example, turn it own in the morning, and off in the evening.

## Solution
This library can communicate and control the device via a short-lived websocket connection.
For the Wifi AP problem, it documents how to use RaspberryPi (Pi) as a proxy.
The Pi connects to both networks simutaneously, and then proxies home network requests to the device's own dedicated wifi.
The Pi proxy also helps solve a very low wifi signal that is caused by the controller being inside a metal junction box.

Finally, a minimal Home Assistant Integration allows to easily remotely control the device, see history and include in any desired home automation.

------

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

