#!/usr/bin/env python3
"""Fix kernel config for GCC 9+ compatibility"""
import re, sys

path = sys.argv[1] if len(sys.argv) > 1 else 'out/.config'

with open(path) as f:
    c = f.read()

# Disable problematic features (set to =n)
for k in ['CONFIG_FORTIFY_SOURCE', 'CONFIG_PRIMA_WLAN',
          'CONFIG_QCA_CLD_WLAN', 'CONFIG_QCA_CLD_WLAN_V2',
          'CONFIG_HDCP_2X']:
    c = re.sub(k + r'=y', '# ' + k + ' is not set', c)
    c = re.sub(k + r'=m', '# ' + k + ' is not set', c)

# Stackprotector: disable via NONE choice (not via =n which doesn't work)
c = c.replace('CONFIG_CC_STACKPROTECTOR_STRONG=y', '# CONFIG_CC_STACKPROTECTOR_STRONG is not set')
c = c.replace('CONFIG_CC_STACKPROTECTOR_REGULAR=y', '# CONFIG_CC_STACKPROTECTOR_REGULAR is not set')
# Add NONE if not present
if 'CONFIG_CC_STACKPROTECTOR_NONE=y' not in c and 'CONFIG_CC_STACKPROTECTOR_NONE' not in c:
    c = c.replace('# CONFIG_CC_STACKPROTECTOR_STRONG is not set',
                  'CONFIG_CC_STACKPROTECTOR_NONE=y\n# CONFIG_CC_STACKPROTECTOR_STRONG is not set')

with open(path, 'w') as f:
    f.write(c)

print('Config fixed for GCC 9+ compatibility')
