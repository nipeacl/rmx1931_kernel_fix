#!/usr/bin/env python3
"""Fix kernel config for GCC 9+ compatibility"""
import re, sys

path = sys.argv[1] if len(sys.argv) > 1 else 'out/.config'

with open(path) as f:
    c = f.read()

fixes = {
    'CONFIG_FORTIFY_SOURCE': 'n',
    'CONFIG_PRIMA_WLAN': 'n',
    'CONFIG_QCA_CLD_WLAN': 'n',
    'CONFIG_QCA_CLD_WLAN_V2': 'n',
    'CONFIG_HDCP_2X': 'n',
}
for k, v in fixes.items():
    c = re.sub(k + r'=y', k + '=n', c)

# STACKPROTECTOR: downgrade STRONG to REGULAR
c = c.replace(
    'CONFIG_CC_STACKPROTECTOR_STRONG=y',
    'CONFIG_CC_STACKPROTECTOR_REGULAR=y'
)

with open(path, 'w') as f:
    f.write(c)

print('Config fixed for GCC 9+')
