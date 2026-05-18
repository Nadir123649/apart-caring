import os
import re
from bs4 import BeautifulSoup # bs4 might not be installed, so we can use regex to be safe and robust!

# Let's use pure Python regex so we don't depend on external libraries
files = [
    "index.html",
    "different-care.html",
    "time-for-care.html",
    "caregiving-hard.html",
    "families-saying.html",
    "still-thinking.html"
]

for filename in files:
    if not os.path.exists(filename):
        continue
        
    print(f"\n==========================================")
    print(f"AUDITING: {filename}")
    print(f"==========================================")
    
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()
        
    # 1. Check mc:edit tags uniqueness
    mc_edits = re.findall(r'mc:edit=["\']([^"\']+)["\']', content)
    duplicates = set([x for x in mc_edits if mc_edits.count(x) > 1])
    
    print(f"- Total mc:edit tags found: {len(mc_edits)}")
    if duplicates:
        print(f"  ⚠️ WARNING: Duplicate mc:edit tags found: {list(duplicates)}")
    else:
        print(f"  ✅ SUCCESS: All mc:edit tags are unique.")
        
    # 2. Check Unsubscribe Link href
    # Let's find links containing "Unsubscribe" in text or styling
    # We will search for the anchor around "Unsubscribe" text
    unsub_pattern = r'<a\s+[^>]*href=["\']([^"\']+)["\'][^>]*>(?:.|\n)*?Unsubscribe'
    matches = re.findall(unsub_pattern, content, re.IGNORECASE)
    
    if matches:
        for href in matches:
            if href == "*|UNSUB|*":
                print(f"  ✅ SUCCESS: Unsubscribe link is correctly set to '*|UNSUB|*'.")
            else:
                print(f"  ⚠️ WARNING: Unsubscribe link is set to '{href}' instead of '*|UNSUB|*'.")
    else:
        # Fallback check
        if "unsubscribe" in content.lower():
            print(f"  ⚠️ WARNING: 'Unsubscribe' text found, but could not parse the link href. Please check manually.")
        else:
            print(f"  ❌ ERROR: No 'Unsubscribe' text found in the email footer!")
