#!/usr/bin/env python3
"""Fix kernel config for GCC 9+ compatibility"""
import re, sys

path = sys.argv[1] if len(sys.argv) > 1 else 'out/.config'

with open(path) as f:
    c = f.read()

# Disable problematic features
for k in ['CONFIG_FORTIFY_SOURCE', 'CONFIG_PRIMA_WLAN',
          'CONFIG_QCA_CLD_WLAN', 'CONFIG_QCA_CLD_WLAN_V2',
          'CONFIG_HDCP_2X', 'CONFIG_CC_STACKPROTECTOR']:
    c = re.sub(k + r'=y', '# ' + k + ' is not set', c)
    c = re.sub(k + r'=m', '# ' + k + ' is not set', c)

with open(path, 'w') as f:
    f.write(c)

print('Config fixed - stackprotector disabled')
