#!/usr/bin/env python3
"""
Simple extraction test for Ken's frame data
"""

import json
import re
from bs4 import BeautifulSoup

def extract_ken_data():
    """Test extraction for Ken specifically."""
    
    with open('/Users/yutayokota/Downloads/sf_frame_html/ken.html', 'r', encoding='utf-8') as f:
        html_content = f.read()
    
    print("HTML file loaded, size:", len(html_content))
    
    soup = BeautifulSoup(html_content, 'html.parser')
    script_tags = soup.find_all('script')
    
    print("Found", len(script_tags), "script tags")
    
    # First pass - find __NEXT_DATA__
    next_data_script = None
    for i, script in enumerate(script_tags):
        if script.string and '__NEXT_DATA__' in script.string:
            print(f"\nFound __NEXT_DATA__ in script {i}! ({len(script.string)} characters)")
            next_data_script = script.string
            break
    
    if not next_data_script:
        print("__NEXT_DATA__ not found in any script tag")
        return None
    
    # Extract the JSON data
    print("Attempting to extract JSON from __NEXT_DATA__...")
    
    # Try multiple regex patterns to extract the JSON
    patterns = [
        r'__NEXT_DATA__\s*=\s*({.*?});?\s*$',
        r'__NEXT_DATA__\s*=\s*({.*?});',
        r'__NEXT_DATA__\s*=\s*({.*})(?=\s*</script>)',
        r'__NEXT_DATA__\s*=\s*({.*})(?=\s*$)',
    ]
    
    for pattern in patterns:
        match = re.search(pattern, next_data_script, re.DOTALL | re.MULTILINE)
        if match:
            try:
                json_str = match.group(1)
                print(f"Matched with pattern: {pattern}")
                print(f"JSON string length: {len(json_str)}")
                
                # Try to find the proper end of the JSON object
                brace_count = 0
                end_pos = 0
                for pos, char in enumerate(json_str):
                    if char == '{':
                        brace_count += 1
                    elif char == '}':
                        brace_count -= 1
                        if brace_count == 0:
                            end_pos = pos + 1
                            break
                
                if end_pos > 0 and end_pos < len(json_str):
                    json_str = json_str[:end_pos]
                    print(f"Trimmed to {len(json_str)} characters")
                
                data = json.loads(json_str)
                print("Successfully parsed __NEXT_DATA__!")
                
                # Explore the structure
                print("Top level keys:", list(data.keys()))
                
                if 'props' in data:
                    props = data['props']
                    print("Props keys:", list(props.keys()))
                    
                    if 'pageProps' in props:
                        page_props = props['pageProps']
                        print("PageProps keys:", list(page_props.keys()))
                        
                        # Look for any data that might contain frame information
                        for key, value in page_props.items():
                            if isinstance(value, (list, dict)):
                                print(f"  {key}: {type(value).__name__}")
                                if isinstance(value, list) and len(value) > 0:
                                    print(f"    - Length: {len(value)}")
                                    print(f"    - First item type: {type(value[0]).__name__}")
                                    if isinstance(value[0], dict):
                                        first_keys = list(value[0].keys())[:10]
                                        print(f"    - First item keys: {first_keys}")
                                elif isinstance(value, dict):
                                    dict_keys = list(value.keys())[:10]
                                    print(f"    - Dict keys: {dict_keys}")
                        
                        # Save the pageProps data for inspection
                        with open('/Users/yutayokota/projects/sf-frame/ken_pageprops.json', 'w', encoding='utf-8') as f:
                            json.dump(page_props, f, indent=2, ensure_ascii=False)
                        print("Saved pageProps to ken_pageprops.json for inspection")
                        
                        return page_props
                
            except json.JSONDecodeError as e:
                print(f"JSON decode error with pattern {pattern}: {e}")
                # Show first part of problematic JSON
                print(f"First 200 chars: {json_str[:200]}")
                continue
    
    print("Could not extract valid JSON from __NEXT_DATA__")
    return None

if __name__ == '__main__':
    result = extract_ken_data()
    if result:
        print("Extraction completed successfully!")
    else:
        print("Extraction failed")