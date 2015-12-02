import logging
logging.getLogger("scapy.runtime").setLevel(logging.ERROR)
from scapy.all import *
import subprocess
import yaml
import os

# Get current working directory
path = os.path.dirname(os.path.realpath(__file__))

# Creat a log file
dashlog = open(path + '/pydasher.log', 'a')

# Place config in dict
yaml_dict = yaml.load(open(path + '/config.yaml'))

# Place HA settings in seperate dict
config = yaml_dict['home_assistant']
# Extract HA host and api password
host = config['host']
password = config['api_password']
# Remove HA settings from dict
del yaml_dict['home_assistant']

#Create empty button dict
buttons = {}

# Populate buttons dict with yaml buttons
for v in yaml_dict.itervalues():
  buttons[v['MAC']] = v['HA_EVENT']

# Look for arps
def arp_display(pkt):
  if pkt[ARP].op == 1: #who-has (request)
    if pkt[ARP].psrc == '0.0.0.0': # ARP Probe
      if pkt[ARP].hwsrc in buttons.keys(): # Found a button's MAC
        dashlog.write("Found a button\n")
        # Fire a curl POST to HA's web API
        dashlog.write("\n")
        subprocess.call(["curl", "-H", "x-ha-access: " + password, "-X", "POST", "http://" + host + ":8123/api/events/" + buttons.get(pkt[ARP].hwsrc)], stdout=dashlog)
        # Output response to log
      else:
        # Output unknown ARP's to the log as well
        dashlog.write("ARP Probe from unknown device: " + pkt[ARP].hwsrc + "\n")

# Run it
time.sleep(15)
sniff(prn=arp_display, filter="arp", store=0, count=0)
