#!/usr/bin/env python3
"""Fix kernel config for GCC 4.9 compatibility"""
import re, sys

path = sys.argv[1] if len(sys.argv) > 1 else 'out/.config'

with open(path) as f:
    c = f.read()

# Disable problematic options for GCC 4.9 CAF toolchain
fixes = {
    'CONFIG_CC_STACKPROTECTOR_STRONG': 'n',
    'CONFIG_CC_STACKPROTECTOR_REGULAR': 'n',
    'CONFIG_CC_STACKPROTECTOR_NONE': 'y',
    # FORTIFY_SOURCE uses compile-time checks that GCC 4.9 handles differently
    'CONFIG_FORTIFY_SOURCE': 'n',
    # WLAN/HDCP - not needed
    'CONFIG_PRIMA_WLAN': 'n',
    'CONFIG_WLAN': 'n',
    'CONFIG_HDCP_QSEECOM': 'n',
}

for k, v in fixes.items():
    if re.search(rf'^{k}[= ]', c, re.MULTILINE):
        c = re.sub(rf'^{k}=.*$', f'{k}={v}', c, flags=re.MULTILINE)
        print(f'  Set  {k}={v}')
    else:
        c += f'\n{k}={v}\n'
        print(f'  Added {k}={v}')

with open(path, 'w') as f:
    f.write(c)
print('Config fixed for GCC 4.9')
