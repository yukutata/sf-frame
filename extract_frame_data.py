#!/usr/bin/env python3
"""
Street Fighter 6 Frame Data Extractor

This script extracts frame data from HTML files and converts them to JSON format
similar to the Ryu data structure.
"""

import os
import json
import re
from typing import Dict, List, Any, Optional
from bs4 import BeautifulSoup
import argparse

# Character name mappings (Japanese to English)
CHARACTER_NAMES = {
    'aki': {'japanese': 'A.K.I.', 'english': 'A.K.I.'},
    'blanka': {'japanese': 'ブランカ', 'english': 'Blanka'},
    'cammy': {'japanese': 'キャミィ', 'english': 'Cammy'},
    'chunli': {'japanese': '春麗', 'english': 'Chun-Li'},
    'deejay': {'japanese': 'ディージェイ', 'english': 'Dee Jay'},
    'dhalsim': {'japanese': 'ダルシム', 'english': 'Dhalsim'},
    'ed': {'japanese': 'エド', 'english': 'Ed'},
    'ehonda': {'japanese': 'E.本田', 'english': 'E. Honda'},
    'elena': {'japanese': 'エレナ', 'english': 'Elena'},
    'gouki': {'japanese': '豪鬼', 'english': 'Akuma'},
    'guile': {'japanese': 'ガイル', 'english': 'Guile'},
    'jamie': {'japanese': 'ジェイミー', 'english': 'Jamie'},
    'jp': {'japanese': 'JP', 'english': 'JP'},
    'juri': {'japanese': 'ユリ', 'english': 'Juri'},
    'ken': {'japanese': 'ケン', 'english': 'Ken'},
    'kimberly': {'japanese': 'キンバリー', 'english': 'Kimberly'},
    'lily': {'japanese': 'リリー', 'english': 'Lily'},
    'luke': {'japanese': 'ルーク', 'english': 'Luke'},
    'mai': {'japanese': '不知火舞', 'english': 'Mai Shiranui'},
    'manon': {'japanese': 'マノン', 'english': 'Manon'},
    'marisa': {'japanese': 'マリーザ', 'english': 'Marisa'},
    'rashid': {'japanese': 'ラシード', 'english': 'Rashid'},
    'ryu': {'japanese': 'リュウ', 'english': 'Ryu'},
    'sagat': {'japanese': 'サガット', 'english': 'Sagat'},
    'terry': {'japanese': 'テリー・ボガード', 'english': 'Terry Bogard'},
    'vega_mbison': {'japanese': 'ベガ', 'english': 'M. Bison'},
    'zangief': {'japanese': 'ザンギエフ', 'english': 'Zangief'}
}

# Category mappings
CATEGORY_MAPPINGS = {
    "通常技": {"japanese": "通常技", "english": "Normal Attacks"},
    "特殊技": {"japanese": "特殊技", "english": "Special Normals"},
    "必殺技": {"japanese": "必殺技", "english": "Special Moves"},
    "スーパーアーツ": {"japanese": "スーパーアーツ", "english": "Super Arts"},
    "通常投げ": {"japanese": "通常投げ", "english": "Throws"},
    "共通システム": {"japanese": "共通システム", "english": "System Mechanics"}
}

def extract_json_from_html(html_content: str) -> Optional[Dict]:
    """
    Extract JSON data from HTML content.
    This looks for embedded JSON data in script tags or data attributes.
    """
    # Try to find JSON data in script tags
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Look for script tags containing frame data
    script_tags = soup.find_all('script')
    for script in script_tags:
        if script.string:
            content = script.string
            
            # Look for Next.js style data - be more flexible with the regex
            next_data_match = re.search(r'__NEXT_DATA__\s*=\s*({.*})', content, re.DOTALL)
            if next_data_match:
                try:
                    json_str = next_data_match.group(1)
                    # Clean up the JSON string - remove everything after the closing brace
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
                    
                    next_data = json.loads(json_str)
                    print(f"Found __NEXT_DATA__ with keys: {list(next_data.keys())}")
                    
                    # Extract character data from Next.js data structure
                    if 'props' in next_data and 'pageProps' in next_data['props']:
                        page_props = next_data['props']['pageProps']
                        print(f"PageProps keys: {list(page_props.keys())}")
                        
                        # Look for frame data in various locations
                        possible_keys = ['frameData', 'characterData', 'data', 'moves', 'character']
                        for key in possible_keys:
                            if key in page_props:
                                data = page_props[key]
                                if isinstance(data, dict):
                                    return data
                        
                        # Sometimes the data is nested deeper
                        for key, value in page_props.items():
                            if isinstance(value, dict):
                                if 'moves' in value or 'character' in value or 'frameData' in value:
                                    return value
                                # Check one level deeper
                                for subkey, subvalue in value.items():
                                    if isinstance(subvalue, dict) and ('moves' in subvalue or 'character' in subvalue):
                                        return subvalue
                    
                    return next_data  # Return the whole thing if we can't find specific data
                except json.JSONDecodeError as e:
                    print(f"JSON decode error for __NEXT_DATA__: {e}")
                    continue
            
            # Look for other patterns that might contain frame data
            patterns = [
                r'frameData\s*[:=]\s*({.*?})',
                r'characterData\s*[:=]\s*({.*?})',
                r'moveData\s*[:=]\s*({.*?})',
                r'data\s*[:=]\s*({.*?"character".*?})',
                r'window\.__INITIAL_STATE__\s*=\s*({.*?})',
                r'window\.frameData\s*=\s*({.*?})'
            ]
            
            for pattern in patterns:
                matches = re.findall(pattern, content, re.DOTALL)
                for match in matches:
                    try:
                        # Try to clean up the JSON string
                        match = match.strip()
                        # Handle potential trailing commas or semicolons
                        if match.endswith((',', ';')):
                            match = match[:-1]
                        
                        data = json.loads(match)
                        if isinstance(data, dict) and ('character' in data or 'moves' in data):
                            return data
                    except json.JSONDecodeError:
                        continue
            
            # Look for large JSON objects that might contain character data
            json_objects = re.findall(r'\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\}', content)
            for obj in json_objects:
                if len(obj) > 1000:  # Only check large objects
                    try:
                        data = json.loads(obj)
                        if isinstance(data, dict) and ('character' in data or 'moves' in data):
                            return data
                    except json.JSONDecodeError:
                        continue
    
    return None

def extract_table_data(html_content: str) -> List[Dict]:
    """
    Extract frame data from HTML tables if present.
    """
    soup = BeautifulSoup(html_content, 'html.parser')
    moves = []
    
    # Look for tables containing frame data
    tables = soup.find_all('table')
    
    for table in tables:
        rows = table.find_all('tr')
        headers = []
        
        # Extract headers
        if rows:
            header_row = rows[0]
            headers = [th.get_text(strip=True) for th in header_row.find_all(['th', 'td'])]
        
        # Extract data rows
        for row in rows[1:]:
            cells = row.find_all(['td', 'th'])
            if len(cells) >= 3:  # Minimum required columns
                move_data = {}
                for i, cell in enumerate(cells):
                    if i < len(headers):
                        move_data[headers[i]] = cell.get_text(strip=True)
                
                if move_data:
                    moves.append(move_data)
    
    return moves

def parse_frame_value(value: str) -> Any:
    """
    Parse frame data values, handling special cases like 'D' for knockdown.
    """
    if not value or value == '-':
        return None
    
    value = value.strip()
    
    # Handle special cases
    if value.upper() == 'D':
        return 'D'
    
    # Try to convert to int
    try:
        return int(value)
    except ValueError:
        pass
    
    # Handle ranges like "4-6"
    if '-' in value and re.match(r'\d+-\d+', value):
        return value
    
    # Handle complex frame descriptions
    if '+' in value or '着地後' in value:
        return value
    
    return value

def convert_table_to_moves(table_data: List[Dict], character: str) -> List[Dict]:
    """
    Convert extracted table data to the standardized move format.
    """
    moves = []
    move_id = 1
    
    for row in table_data:
        move = {
            "id": move_id,
            "name": {
                "japanese": row.get('技名', row.get('Move Name', f'技{move_id}')),
                "english": row.get('技名', row.get('Move Name', f'技{move_id}')),
                "japanese_base": row.get('技名', row.get('Move Name', f'技{move_id}'))
            },
            "category": {
                "japanese": "通常技",  # Default, should be determined from context
                "english": "Normal Attacks"
            },
            "type": "normal",  # Will be determined based on category
            "frames": {
                "startup": parse_frame_value(row.get('発生', row.get('Startup', ''))),
                "active": parse_frame_value(row.get('持続', row.get('Active', ''))),
                "recovery": parse_frame_value(row.get('硬直', row.get('Recovery', ''))),
                "on_hit": parse_frame_value(row.get('ヒット', row.get('On Hit', ''))),
                "on_block": parse_frame_value(row.get('ガード', row.get('On Block', '')))
            },
            "properties": {
                "damage": parse_frame_value(row.get('ダメージ', row.get('Damage', ''))),
                "cancel": row.get('キャンセル', row.get('Cancel', '')),
                "combo_scaling": row.get('補正', row.get('Scaling', '')),
                "attribute": row.get('属性', row.get('Attribute', '')),
                "notes": row.get('備考', row.get('Notes', ''))
            },
            "drive_system": {
                "gain_on_hit": parse_frame_value(row.get('DRVゲイン(ヒット)', row.get('Drive Gain Hit', ''))),
                "loss_on_guard": parse_frame_value(row.get('DRVロス(ガード)', row.get('Drive Loss Guard', ''))),
                "loss_on_punish": parse_frame_value(row.get('DRVロス(カウンター)', row.get('Drive Loss Counter', '')))
            },
            "sa_gain": parse_frame_value(row.get('SAゲイン', row.get('SA Gain', '')))
        }
        
        moves.append(move)
        move_id += 1
    
    return moves

def determine_move_categories(moves: List[Dict]) -> Dict[str, List[int]]:
    """
    Categorize moves based on their names and properties.
    """
    categories = {
        "通常技": [],
        "特殊技": [], 
        "必殺技": [],
        "スーパーアーツ": [],
        "通常投げ": [],
        "共通システム": []
    }
    
    for move in moves:
        move_name = move["name"]["japanese"]
        move_id = move["id"]
        
        # Basic categorization based on move names
        if any(keyword in move_name for keyword in ['立ち', 'しゃがみ', 'ジャンプ']):
            categories["通常技"].append(move_id)
            move["category"] = CATEGORY_MAPPINGS["通常技"]
            move["type"] = determine_move_type(move_name)
        elif any(keyword in move_name for keyword in ['SA1', 'SA2', 'SA3', 'CA']):
            categories["スーパーアーツ"].append(move_id)
            move["category"] = CATEGORY_MAPPINGS["スーパーアーツ"]
            move["type"] = "super_art"
        elif any(keyword in move_name for keyword in ['投げ', 'スルー']):
            categories["通常投げ"].append(move_id)
            move["category"] = CATEGORY_MAPPINGS["通常投げ"]
            move["type"] = "throw"
        elif any(keyword in move_name for keyword in ['弱', '中', '強', 'OD']):
            categories["必殺技"].append(move_id)
            move["category"] = CATEGORY_MAPPINGS["必殺技"]
            move["type"] = "special_move"
        else:
            # Default to special normals for uncategorized moves
            categories["特殊技"].append(move_id)
            move["category"] = CATEGORY_MAPPINGS["特殊技"]
            move["type"] = "special_normal"
    
    return categories

def determine_move_type(move_name: str) -> str:
    """
    Determine the move type based on the move name.
    """
    if '立ち' in move_name:
        return 'standing_normal'
    elif 'しゃがみ' in move_name:
        return 'crouching_normal'
    elif 'ジャンプ' in move_name:
        return 'jumping_normal'
    elif '投げ' in move_name:
        return 'throw'
    else:
        return 'special_normal'

def create_character_data(character: str, moves: List[Dict]) -> Dict:
    """
    Create the complete character data structure.
    """
    if character not in CHARACTER_NAMES:
        character_names = {'japanese': character, 'english': character}
    else:
        character_names = CHARACTER_NAMES[character]
    
    categories = determine_move_categories(moves)
    
    # Add formatted categories
    formatted_categories = {}
    for cat_key, move_ids in categories.items():
        formatted_categories[cat_key] = {
            **CATEGORY_MAPPINGS[cat_key],
            "moves": move_ids
        }
    
    character_data = {
        "character": character,
        "character_name": character_names,
        "health": 10000,  # Default, should be adjusted per character
        "categories": formatted_categories,
        "moves": moves
    }
    
    return character_data

def extract_from_html_file(html_file_path: str) -> Optional[Dict]:
    """
    Extract frame data from an HTML file.
    """
    try:
        with open(html_file_path, 'r', encoding='utf-8') as f:
            html_content = f.read()
        
        character = os.path.basename(html_file_path).replace('.html', '')
        
        # Try to extract JSON data first
        json_data = extract_json_from_html(html_content)
        if json_data:
            return json_data
        
        # Try to extract table data
        table_data = extract_table_data(html_content)
        if table_data:
            moves = convert_table_to_moves(table_data, character)
            return create_character_data(character, moves)
        
        print(f"Warning: Could not extract frame data from {html_file_path}")
        return None
        
    except Exception as e:
        print(f"Error processing {html_file_path}: {e}")
        return None

def save_character_data(character_data: Dict, output_dir: str) -> str:
    """
    Save character data to a JSON file.
    """
    character = character_data["character"]
    output_file = os.path.join(output_dir, f"{character}_frame_data_structured.json")
    
    with open(output_file, 'w', encoding='utf-8', newline='\n') as f:
        json.dump(character_data, f, indent=2, ensure_ascii=False)
    
    return output_file

def inspect_html_structure(html_file_path: str) -> None:
    """
    Inspect HTML file structure to understand data organization.
    """
    try:
        with open(html_file_path, 'r', encoding='utf-8') as f:
            html_content = f.read()
        
        character = os.path.basename(html_file_path).replace('.html', '')
        print(f"\nInspecting {character}.html:")
        print(f"  File size: {len(html_content):,} characters")
        
        # Look for key patterns
        patterns = [
            r'__NEXT_DATA__',
            r'frameData',
            r'characterData',
            r'moveData',
            r'通常技',
            r'必殺技',
            r'startup',
            r'active',
            r'recovery'
        ]
        
        for pattern in patterns:
            matches = len(re.findall(pattern, html_content, re.IGNORECASE))
            if matches > 0:
                print(f"  Found '{pattern}': {matches} occurrences")
        
        # Check for script tags
        soup = BeautifulSoup(html_content, 'html.parser')
        script_tags = soup.find_all('script')
        print(f"  Script tags: {len(script_tags)}")
        
        for i, script in enumerate(script_tags):
            if script.string and len(script.string) > 1000:
                print(f"    Script {i}: {len(script.string):,} chars")
                # Look for JSON-like content
                if '{' in script.string and '"' in script.string:
                    print(f"    Script {i}: Contains JSON-like data")
                
    except Exception as e:
        print(f"Error inspecting {html_file_path}: {e}")

def main():
    parser = argparse.ArgumentParser(description='Extract Street Fighter 6 frame data from HTML files')
    parser.add_argument('--input-dir', default='/Users/yutayokota/Downloads/sf_frame_html/',
                        help='Directory containing HTML files')
    parser.add_argument('--output-dir', default='/Users/yutayokota/projects/sf-frame/src/data/',
                        help='Directory to save JSON files')
    parser.add_argument('--characters', nargs='+', default=['ken', 'chunli'],
                        help='Characters to process (default: ken, chunli)')
    parser.add_argument('--all', action='store_true',
                        help='Process all characters')
    parser.add_argument('--inspect', action='store_true',
                        help='Inspect HTML structure without processing')
    
    args = parser.parse_args()
    
    if not os.path.exists(args.input_dir):
        print(f"Error: Input directory {args.input_dir} does not exist")
        return
    
    if not os.path.exists(args.output_dir):
        os.makedirs(args.output_dir)
    
    # Get list of characters to process
    if args.all:
        characters = []
        for file in os.listdir(args.input_dir):
            if file.endswith('.html'):
                characters.append(file.replace('.html', ''))
    else:
        characters = args.characters
    
    # If inspection mode, just inspect the files
    if args.inspect:
        print(f"Inspecting {len(characters)} character(s): {', '.join(characters)}")
        for character in characters:
            html_file = os.path.join(args.input_dir, f"{character}.html")
            if not os.path.exists(html_file):
                print(f"Warning: {html_file} not found")
                continue
            inspect_html_structure(html_file)
        return
    
    print(f"Processing {len(characters)} character(s): {', '.join(characters)}")
    
    success_count = 0
    for character in characters:
        html_file = os.path.join(args.input_dir, f"{character}.html")
        
        if not os.path.exists(html_file):
            print(f"Warning: {html_file} not found")
            continue
        
        print(f"Processing {character}...")
        
        character_data = extract_from_html_file(html_file)
        if character_data:
            output_file = save_character_data(character_data, args.output_dir)
            print(f"Successfully extracted data for {character} -> {output_file}")
            success_count += 1
        else:
            print(f"Failed to extract data for {character}")
    
    print(f"\nCompleted processing. Successfully extracted {success_count}/{len(characters)} characters.")
    
    if success_count == 0:
        print("\nNote: The HTML files might contain dynamically loaded data.")
        print("Try using browser developer tools to inspect the actual data structure.")
        print("You may need to modify this script to handle the specific format used by these files.")

if __name__ == '__main__':
    main()