#!/usr/bin/env python3
"""
Extract frame data for Chun-Li and Ken
"""

import os
import json
import re
from typing import Dict, List, Any, Optional
from bs4 import BeautifulSoup

# Character name mappings (Japanese to English)
CHARACTER_NAMES = {
    'chunli': {'japanese': '春麗', 'english': 'Chun-Li'},
    'ken': {'japanese': 'ケン', 'english': 'Ken'}
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

def extract_text_from_element(element):
    """Extract text from an element, handling nested tags."""
    if element is None:
        return ""
    return element.get_text(strip=True)

def clean_frame_value(value: str) -> Any:
    """Clean and parse frame data values."""
    if not value or value == '-' or value == '':
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
    
    # Handle ranges like "4-6" or complex descriptions
    if re.match(r'\d+-\d+', value) or '+' in value or '着地' in value or '全体' in value:
        return value
    
    return value

def extract_move_data_from_row(row, move_id: int) -> Optional[Dict]:
    """Extract move data from a table row using CSS classes."""
    
    # Extract move name
    name_element = row.find(class_=re.compile(r'frame_skill__'))
    if not name_element:
        return None
    
    move_name = extract_text_from_element(name_element)
    if not move_name:
        return None
    
    # Extract frame data using specific CSS classes
    startup_element = row.find(class_=re.compile(r'frame_startup_frame__'))
    active_element = row.find(class_=re.compile(r'frame_active_frame__'))
    recovery_element = row.find(class_=re.compile(r'frame_recovery_frame__'))
    hit_element = row.find(class_=re.compile(r'frame_hit_frame__'))
    block_element = row.find(class_=re.compile(r'frame_block_frame__'))
    
    # Extract other properties
    damage_element = row.find(class_=re.compile(r'frame_damage__'))
    cancel_element = row.find(class_=re.compile(r'frame_cancel__'))
    combo_element = row.find(class_=re.compile(r'frame_combo_correct__'))
    attribute_element = row.find(class_=re.compile(r'frame_attribute__'))
    special_element = row.find(class_=re.compile(r'frame_special_correct__'))
    knockdown_element = row.find(class_=re.compile(r'frame_knockdown__'))
    
    startup = clean_frame_value(extract_text_from_element(startup_element))
    active = clean_frame_value(extract_text_from_element(active_element))
    recovery = clean_frame_value(extract_text_from_element(recovery_element))
    on_hit = clean_frame_value(extract_text_from_element(hit_element))
    on_block = clean_frame_value(extract_text_from_element(block_element))
    
    move_data = {
        "id": move_id,
        "name": {
            "japanese": move_name,
            "english": move_name,
            "japanese_base": move_name
        },
        "category": determine_category(move_name),
        "type": determine_move_type(move_name),
        "frames": {
            "startup": startup,
            "active": active,
            "recovery": recovery,
            "on_hit": on_hit,
            "on_block": on_block
        },
        "damage": clean_frame_value(extract_text_from_element(damage_element)),
        "cancel": extract_text_from_element(cancel_element) or None,
        "combo_correctable": extract_text_from_element(combo_element) == '○',
        "attribute": extract_text_from_element(attribute_element) or None,
        "special_correctable": extract_text_from_element(special_element) == '○',
        "knockdown": extract_text_from_element(knockdown_element) or None
    }
    
    return move_data

def determine_category(move_name: str) -> Dict[str, str]:
    """Determine the category of a move based on its name."""
    if any(x in move_name for x in ['SA', 'CA', 'スーパーアーツ', 'クリティカルアーツ']):
        return CATEGORY_MAPPINGS["スーパーアーツ"]
    elif any(x in move_name for x in ['投げ', '投', 'スルー']):
        return CATEGORY_MAPPINGS["通常投げ"]
    elif any(x in move_name for x in ['昇龍', '波動', 'スピニング', '百裂', '竜巻', '鷹爪', '気功', '霞駆け']):
        return CATEGORY_MAPPINGS["必殺技"]
    elif any(x in move_name for x in ['天空', '虎襲', '追突', '鶴脚', '追蹴', '天仰', '旋風', '千裂', '順体']):
        return CATEGORY_MAPPINGS["特殊技"]
    elif any(x in move_name for x in ['ドライブ', 'パリィ', 'インパクト', 'ラッシュ']):
        return CATEGORY_MAPPINGS["共通システム"]
    else:
        return CATEGORY_MAPPINGS["通常技"]

def determine_move_type(move_name: str) -> str:
    """Determine the type of a move based on its name."""
    if 'ドライブ' in move_name or 'Drive' in move_name:
        return 'drive_system'
    elif 'SA' in move_name or 'CA' in move_name or 'スーパーアーツ' in move_name:
        return 'super'
    elif '投げ' in move_name or '投' in move_name:
        return 'throw'
    elif any(x in move_name for x in ['昇龍', '波動', 'スピニング', '百裂', '竜巻', '鷹爪', '気功', '霞駆け']):
        return 'special'
    elif '立ち' in move_name or 'Stand' in move_name:
        return 'standing_normal'
    elif 'しゃがみ' in move_name or 'Crouch' in move_name:
        return 'crouching_normal'
    elif 'ジャンプ' in move_name or 'Jump' in move_name:
        return 'jumping_normal'
    else:
        return 'unique'

def categorize_moves(moves: List[Dict]) -> Dict[str, List[int]]:
    """Categorize moves based on their properties."""
    categories = {
        "通常技": [],
        "特殊技": [],
        "必殺技": [],
        "スーパーアーツ": [],
        "通常投げ": [],
        "共通システム": []
    }
    
    for move in moves:
        cat_japanese = move['category']['japanese']
        if cat_japanese in categories:
            categories[cat_japanese].append(move['id'])
    
    return categories

def extract_character_data(html_file_path: str) -> Optional[Dict]:
    """Extract complete character data from HTML file."""
    
    character = os.path.basename(html_file_path).replace('.html', '')
    print(f"Extracting data for {character}...")
    
    try:
        with open(html_file_path, 'r', encoding='utf-8') as f:
            html_content = f.read()
        
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # Find all table rows that contain move data
        # Look for rows with frame data classes
        rows = soup.find_all('tr')
        frame_rows = []
        
        for row in rows:
            # Check if this row has frame data classes
            if row.find(class_=re.compile(r'frame_startup_frame__')) or row.find(class_=re.compile(r'frame_skill__')):
                frame_rows.append(row)
        
        print(f"Found {len(frame_rows)} potential frame data rows")
        
        moves = []
        move_id = 1
        
        for row in frame_rows:
            move_data = extract_move_data_from_row(row, move_id)
            if move_data:
                # Skip header rows (技名, 発生, etc.)
                move_name = move_data['name']['japanese']
                if move_name in ['技名', '発生', '持続', '硬直', 'ヒット', 'ガード']:
                    continue
                
                moves.append(move_data)
                move_id += 1
        
        if not moves:
            print(f"No moves found for {character}!")
            return None
        
        print(f"Successfully extracted {len(moves)} moves for {character}")
        
        # Categorize moves
        categories = categorize_moves(moves)
        
        # Build formatted categories
        formatted_categories = {}
        for cat_key, move_ids in categories.items():
            formatted_categories[cat_key] = {
                **CATEGORY_MAPPINGS[cat_key],
                "moves": move_ids
            }
        
        # Get character names
        if character in CHARACTER_NAMES:
            character_names = CHARACTER_NAMES[character]
        else:
            character_names = {'japanese': character, 'english': character}
        
        character_data = {
            "character": character,
            "character_name": character_names,
            "health": 10000,  # Default health
            "categories": formatted_categories,
            "moves": moves
        }
        
        return character_data
        
    except Exception as e:
        print(f"Error extracting data from {html_file_path}: {e}")
        return None

def save_character_data(character_data: Dict, output_dir: str) -> str:
    """Save character data to a JSON file."""
    character = character_data["character"]
    output_file = os.path.join(output_dir, f"{character}_frame_data_structured.json")
    
    with open(output_file, 'w', encoding='utf-8', newline='\n') as f:
        json.dump(character_data, f, indent=2, ensure_ascii=False)
    
    return output_file

def main():
    # HTML files for Chun-Li and Ken
    html_dir = '/Users/yutayokota/Downloads/sf_frame_html/'
    output_dir = '/Users/yutayokota/projects/sf-frame/src/data/'
    
    characters = ['chunli', 'ken']
    
    for character in characters:
        html_file = os.path.join(html_dir, f"{character}.html")
        if not os.path.exists(html_file):
            print(f"HTML file not found: {html_file}")
            continue
        
        character_data = extract_character_data(html_file)
        if character_data:
            output_file = save_character_data(character_data, output_dir)
            print(f"Saved {character} data to {output_file}")
            
            # Show some sample data to verify
            print(f"Sample moves for {character}:")
            for move in character_data['moves'][:3]:
                print(f"  - {move['name']['japanese']}: startup={move['frames']['startup']}, on_hit={move['frames']['on_hit']}, on_block={move['frames']['on_block']}")
        else:
            print(f"Failed to extract data for {character}")

if __name__ == "__main__":
    main()