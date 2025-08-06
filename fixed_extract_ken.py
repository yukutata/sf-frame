#!/usr/bin/env python3
"""
Fixed extraction test for Ken's frame data using direct HTML script tag parsing
"""

import json
import re
from bs4 import BeautifulSoup

def extract_ken_data():
    """Extract Ken's frame data from HTML file."""
    
    with open('/Users/yutayokota/Downloads/sf_frame_html/ken.html', 'r', encoding='utf-8') as f:
        html_content = f.read()
    
    print("HTML file loaded, size:", len(html_content))
    
    # Find the script tag with id="__NEXT_DATA__"
    soup = BeautifulSoup(html_content, 'html.parser')
    next_data_script = soup.find('script', {'id': '__NEXT_DATA__'})
    
    if not next_data_script:
        print("Could not find script tag with id='__NEXT_DATA__'")
        return None
    
    print("Found __NEXT_DATA__ script tag!")
    
    # Extract the JSON content from the script tag
    json_content = next_data_script.string
    if not json_content:
        print("Script tag is empty")
        return None
    
    try:
        data = json.loads(json_content)
        print("Successfully parsed __NEXT_DATA__ JSON!")
        
        # Save the raw data for inspection
        with open('/Users/yutayokota/projects/sf-frame/ken_raw_next_data.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        print("Saved raw data to ken_raw_next_data.json")
        
        # Navigate through the structure
        if 'props' in data and 'pageProps' in data['props']:
            page_props = data['props']['pageProps']
            print("Found pageProps!")
            
            # Look for frame data - check for common patterns
            frame_data_keys = ['frameData', 'characterData', 'data', 'moves', 'character', 'ken']
            for key in frame_data_keys:
                if key in page_props:
                    print(f"Found potential frame data under key: {key}")
                    if isinstance(page_props[key], dict):
                        subkeys = list(page_props[key].keys())[:10]  # First 10 keys
                        print(f"  Type: dict, keys: {subkeys}")
                    elif isinstance(page_props[key], list):
                        print(f"  Type: list, length: {len(page_props[key])}")
                        if page_props[key]:
                            print(f"  First item type: {type(page_props[key][0])}")
            
            # Look for character-specific data
            for key, value in page_props.items():
                if 'ken' in key.lower():
                    print(f"Found Ken-related key: {key}")
                    print(f"  Type: {type(value)}")
                    if isinstance(value, dict):
                        print(f"  Dict keys: {list(value.keys())[:10]}")
                elif 'frame' in key.lower():
                    print(f"Found frame-related key: {key}")
                    print(f"  Type: {type(value)}")
                    if isinstance(value, dict):
                        print(f"  Dict keys: {list(value.keys())[:10]}")
                elif isinstance(value, list) and len(value) > 10:  # Likely move data
                    print(f"Found large list under key: {key} (length: {len(value)})")
                    if value and isinstance(value[0], dict):
                        first_item_keys = list(value[0].keys())[:10]
                        print(f"  First item keys: {first_item_keys}")
            
            # Save pageProps for detailed inspection
            with open('/Users/yutayokota/projects/sf-frame/ken_pageprops.json', 'w', encoding='utf-8') as f:
                json.dump(page_props, f, indent=2, ensure_ascii=False)
            print("Saved pageProps to ken_pageprops.json for detailed inspection")
            
            return page_props
        
        print("Could not find props.pageProps in data structure")
        return None
    
    except json.JSONDecodeError as e:
        print(f"JSON decode error: {e}")
        return None

if __name__ == '__main__':
    result = extract_ken_data()
    if result:
        print("Extraction completed successfully!")
        print("Check the generated JSON files for detailed data structure.")
    else:
        print("Extraction failed")