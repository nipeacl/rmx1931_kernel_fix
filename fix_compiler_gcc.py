#!/usr/bin/env python3
"""Fix GCC 4.9 __compiletime_object_size for __bad_copy_to errors"""
import sys

path = sys.argv[1] if len(sys.argv) > 1 else 'include/linux/compiler-gcc.h'

with open(path, 'r') as f:
    content = f.read()

fix = '''
/* GCC 4.9 compat: disable __compiletime_object_size (unreliable __builtin_object_size) */
#if GCC_VERSION < 50000
# undef __compiletime_object_size
# define __compiletime_object_size(obj, type) ((size_t)-1)
#endif
'''

# Only append if not already present
if 'GCC_VERSION < 50000' not in content:
    with open(path, 'a') as f:
        f.write(fix)
    print(f"Applied __compiletime_object_size fix to {path}")
else:
    print(f"Fix already present in {path}")
