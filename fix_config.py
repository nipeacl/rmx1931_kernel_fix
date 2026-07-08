#!/usr/bin/env python3
"""Fix kernel config for build compatibility"""
import re, sys

path = sys.argv[1] if len(sys.argv) > 1 else 'out/.config'

with open(path) as f:
    c = f.read()

# Disable problematic drivers only
for k in ['CONFIG_PRIMA_WLAN', 'CONFIG_QCA_CLD_WLAN',
          'CONFIG_QCA_CLD_WLAN_V2', 'CONFIG_HDCP_2X']:
    c = re.sub(k + r'=y', '# ' + k + ' is not set', c)
    c = re.sub(k + r'=m', '# ' + k + ' is not set', c)

# Stackprotector: keep GCC 4.9 compatible level (REGULAR, not STRONG)
c = c.replace('CONFIG_CC_STACKPROTECTOR_STRONG=y', 'CONFIG_CC_STACKPROTECTOR_REGULAR=y')

# Keep FORTIFY_SOURCE enabled (GCC 4.9 supports it)
# Keep gcc-wrapper removal via Makefile sed in workflow

with open(path, 'w') as f:
    f.write(c)

print('Config fixed for GCC 4.9')
