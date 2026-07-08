#!/usr/bin/env python3
"""Fix sde_hdcp_2x.c for GCC 4.9 - replace 'const' vars with #defines for case labels"""
import sys, os

path = sys.argv[1] if len(sys.argv) > 1 else 'drivers/gpu/drm/msm/sde_hdcp_2x.c'
if not os.path.exists(path):
    print(f"File not found: {path}")
    sys.exit(0)

with open(path) as f:
    c = f.read()

changes = 0
old = 'u8 const hdcp_min_enc_level_0 = 0, hdcp_min_enc_level_1 = 1,'
new = '#define hdcp_min_enc_level_0 0\n#define hdcp_min_enc_level_1 1'
if old in c:
    c = c.replace(old, new)
    changes += 1

old2 = '   hdcp_min_enc_level_2 = 2;'
new2 = '#define hdcp_min_enc_level_2 2'
if old2 in c:
    c = c.replace(old2, new2)
    changes += 1

old3 = 'u8 const stream_type_0 = 0, stream_type_1 = 1;'
new3 = '#define stream_type_0 0\n#define stream_type_1 1'
if old3 in c:
    c = c.replace(old3, new3)
    changes += 1

with open(path, 'w') as f:
    f.write(c)

print(f'Patched {path}: {changes} replacements done')
