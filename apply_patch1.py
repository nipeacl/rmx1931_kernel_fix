#!/usr/bin/env python3
"""Apply patch 1: Fix charger deadlock state machine
Precise text matching - only changes the right spots"""
import sys

def main():
    path = sys.argv[1]
    with open(path) as f: content = f.read()
    
    print(f"Patching: {path}")
    
    # Patch 1a: In oplus_charger_detect_check, change /*do nothing*/ 
    # in the fastchg_to_normal block to charger_resumed = false;
    old1a = '\t\t\t\t/*do nothing*/\n'
    new1a = '\t\t\t\tcharger_resumed = false;\n'
    if old1a in content:
        content = content.replace(old1a, new1a)
        print("  ✓ Patch 1a")
    else:
        # Try alternate indentation
        print("  ⚠ Patch 1a: not found")
    
    # Patch 1b: Remove && charger_resumed == false from condition
    old1b = '\t\t\t} else if (oplus_vooc_get_fastchg_started() == false\n\t\t\t\t\t&& charger_resumed == false) {'
    new1b = '\t\t\t} else if (oplus_vooc_get_fastchg_started() == false) {'
    if old1b in content:
        content = content.replace(old1b, new1b)
        print("  ✓ Patch 1b")
    else:
        print("  ⚠ Patch 1b: not found")
    
    # Patch 1c: Wrap check_charger_resume in if(!charger_resumed)
    import re
    pattern = r'(\t\t\t\tcharger_resumed = chip->chg_ops->check_charger_resume\(\);)\n(\t\t\t\toplus_chg_turn_on_charging\(chip\);)'
    replacement = r'\t\t\t\tif (!charger_resumed)\n\t\t\t\t\t\1\n\t\t\t\t\2'
    new_content = re.sub(pattern, replacement, content)
    if new_content != content:
        content = new_content
        print("  ✓ Patch 1c")
    else:
        # Try with specific text
        old1c = '\t\t\t\tcharger_resumed = chip->chg_ops->check_charger_resume();\n\t\t\t\toplus_chg_turn_on_charging(chip);'
        new1c = '\t\t\t\tif (!charger_resumed)\n\t\t\t\t\tcharger_resumed = chip->chg_ops->check_charger_resume();\n\t\t\t\toplus_chg_turn_on_charging(chip);'
        if old1c in content:
            content = content.replace(old1c, new1c)
            print("  ✓ Patch 1c (string replace)")
        else:
            print("  ⚠ Patch 1c: not found")
    
    with open(path, 'w') as f:
        f.write(content)
    print("  ✓ Saved")

if __name__ == '__main__':
    main()
