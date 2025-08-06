#!/usr/bin/env python3
"""
Debug script to extract and examine JSON data from HTML files.
"""

import json
import re
from bs4 import BeautifulSoup

def debug_extract_ken():
    """Extract data from Ken's HTML file to understand structure."""
    html_file = '/Users/yutayokota/Downloads/sf_frame_html/ken.html'
    
    with open(html_file, 'r', encoding='utf-8') as f:
        html_content = f.read()
    
    print(f"File size: {len(html_content):,} characters")
    
    # Look for __NEXT_DATA__
    next_data_match = re.search(r'__NEXT_DATA__\s*=\s*({.*})', html_content, re.DOTALL)
    if next_data_match:
        json_str = next_data_match.group(1)
        
        # Clean up the JSON string
        brace_count = 0
        end_pos = 0
        for i, char in enumerate(json_str):
            if char == '{':
                brace_count += 1
            elif char == '}':
                brace_count -= 1
                if brace_count == 0:
                    end_pos = i + 1
                    break
        
        if end_pos > 0:
            json_str = json_str[:end_pos]
        
        print(f"JSON string length: {len(json_str):,}")
        
        try:
            next_data = json.loads(json_str)
            print(f"Next.js data keys: {list(next_data.keys())}")
            
            if 'props' in next_data:
                props = next_data['props']
                print(f"Props keys: {list(props.keys())}")
                
                if 'pageProps' in props:
                    page_props = props['pageProps']
                    print(f"PageProps keys: {list(page_props.keys())}")
                    
                    # Save the full data structure to examine
                    with open('/Users/yutayokota/projects/sf-frame/ken_debug.json', 'w', encoding='utf-8') as f:
                        json.dump(page_props, f, indent=2, ensure_ascii=False)
                    
                    print("Saved page props to ken_debug.json")
                    
                    # Look for frame-data-like structures
                    for key, value in page_props.items():
                        if isinstance(value, dict):
                            print(f"  {key}: dict with {len(value)} keys: {list(value.keys())[:5]}...")
                        elif isinstance(value, list):
                            print(f"  {key}: list with {len(value)} items")
                        else:
                            print(f"  {key}: {type(value).__name__}")
            
        except json.JSONDecodeError as e:
            print(f"JSON decode error: {e}")
            # Try to find the issue
            print(f"JSON string preview: {json_str[:500]}...")
    else:
        print("No __NEXT_DATA__ found")

if __name__ == '__main__':
    debug_extract_ken()