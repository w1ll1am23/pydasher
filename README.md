# pydasher

pydasher allows you to fire [Home Assistant](https://home-assistant.io) events when an Amazon Dash button is pressed.

## How it works

Dash buttons are setup in config.yaml along with your Home Assistant API password,
and IP address.

If pydasher detects the MAC address of one of the configured buttons, it will fire
the corresponding Home Assistant event.

## Configuration

You configure your buttons via the `config.yaml` file. 

Example:

```yaml
home_assistant:
  host: 192.168.1.3
  api_password: 123456
button 1:
  MAC: 74:75:48:XX:XX:XX
  HA_EVENT: "toggle_light"
button 2:
  MAC: 10:ae:60:XX:XX:XX
  HA_EVENT: "open_garage"
button 3:
  MAC: 74:c2:46:XX:XX:XX
  HA_EVENT: "set_away"
```

## Tips

* Dash buttons take ~5 seconds to trigger your action.
* Use DHCP Reservation on your Dash button to lower the latency
* Dash buttons can not be used for another ~10 seconds after they've been pressed.


### Install

This has only been tested on Ubuntu!

This script uses Scapy to detect ARP requests, so lets install it.

sudo apt-get install python-scapy

git clone git@github.com:w1ll1am23/pydasher.git

## Running It

Listening for Dash buttons requires root. So you need to launch pydasher with sudo.

    sudo python2 pydasher.py

Unfortunately scapy sometimes errors out with "IndexError: Layer [ARP] not found" on
startup. I have been unable to find a proper solution to this, so I have included 
a bash script which I have scheduled to run in cron every minute. This keeps the pydasher
running, runs it on startup, and "fixes" the above issue.
