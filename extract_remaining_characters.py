#!/usr/bin/env python3
"""
Extract frame data for all remaining SF6 characters
"""

import os
import json
import re
from typing import Dict, List, Any, Optional
from bs4 import BeautifulSoup

# Character name mappings (Japanese to English)
CHARACTER_NAMES = {
    'aki': {'japanese': 'A.K.I.', 'english': 'A.K.I.'},
    'blanka': {'japanese': 'ブランカ', 'english': 'Blanka'},
    'deejay': {'japanese': 'ディージェイ', 'english': 'Dee Jay'},
    'dhalsim': {'japanese': 'ダルシム', 'english': 'Dhalsim'},
    'ed': {'japanese': 'エド', 'english': 'Ed'},
    'ehonda': {'japanese': 'E.本田', 'english': 'E. Honda'},
    'elena': {'japanese': 'エレナ', 'english': 'Elena'},
    'gouki': {'japanese': '豪鬼', 'english': 'Akuma'},
    'guile': {'japanese': 'ガイル', 'english': 'Guile'},
    'jamie': {'japanese': 'ジェイミー', 'english': 'Jamie'},
    'jp': {'japanese': 'JP', 'english': 'JP'},
    'juri': {'japanese': 'ジュリ', 'english': 'Juri'},
    'kimberly': {'japanese': 'キンバリー', 'english': 'Kimberly'},
    'lily': {'japanese': 'リリー', 'english': 'Lily'},
    'mai': {'japanese': '不知火舞', 'english': 'Mai Shiranui'},
    'manon': {'japanese': 'マノン', 'english': 'Manon'},
    'marisa': {'japanese': 'マリーザ', 'english': 'Marisa'},
    'rashid': {'japanese': 'ラシード', 'english': 'Rashid'},
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
    note_element = row.find(class_=re.compile(r'frame_note__'))
    
    # Extract drive gauge data
    drive_gain_element = row.find(class_=re.compile(r'frame_drive_gauge_gain_hit__'))
    drive_loss_guard_element = row.find(class_=re.compile(r'frame_drive_gauge_lose_dguard__'))
    drive_loss_punish_element = row.find(class_=re.compile(r'frame_drive_gauge_lose_punish__'))
    
    # Extract SA gauge data
    sa_gain_element = row.find(class_=re.compile(r'frame_sa_gauge_gain__'))
    
    move_data = {
        "id": move_id,
        "name": {
            "japanese": move_name,
            "english": move_name,  # We'll use the same for now
            "japanese_base": move_name
        },
        "category": {
            "japanese": "通常技",  # Default, will be determined later
            "english": "Normal Attacks"
        },
        "type": "normal",
        "frames": {
            "startup": clean_frame_value(extract_text_from_element(startup_element)),
            "active": clean_frame_value(extract_text_from_element(active_element)),
            "recovery": clean_frame_value(extract_text_from_element(recovery_element)),
            "on_hit": clean_frame_value(extract_text_from_element(hit_element)),
            "on_block": clean_frame_value(extract_text_from_element(block_element))
        },
        "properties": {
            "damage": clean_frame_value(extract_text_from_element(damage_element)),
            "cancel": extract_text_from_element(cancel_element),
            "combo_scaling": extract_text_from_element(combo_element),
            "attribute": extract_text_from_element(attribute_element),
            "notes": extract_text_from_element(note_element)
        },
        "drive_system": {
            "gain_on_hit": clean_frame_value(extract_text_from_element(drive_gain_element)),
            "loss_on_guard": clean_frame_value(extract_text_from_element(drive_loss_guard_element)),
            "loss_on_punish": clean_frame_value(extract_text_from_element(drive_loss_punish_element))
        },
        "sa_gain": clean_frame_value(extract_text_from_element(sa_gain_element))
    }
    
    return move_data

def categorize_moves(moves: List[Dict]) -> Dict[str, List[int]]:
    """Categorize moves and update their category information."""
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
        
        # Categorize based on move names
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
        elif any(keyword in move_name for keyword in ['弱', '中', '強', 'OD']) or '拳' in move_name or '脚' in move_name:
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
    """Determine the move type based on the move name."""
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
    # Available HTML files
    html_dir = '/Users/yutayokota/Downloads/sf_frame_html/'
    output_dir = '/Users/yutayokota/projects/sf-frame/src/data/'
    
    # Check which characters already exist
    existing_characters = set()
    if os.path.exists(output_dir):
        for file in os.listdir(output_dir):
            if file.endswith('_frame_data_structured.json'):
                char_name = file.replace('_frame_data_structured.json', '')
                existing_characters.add(char_name)
    
    print(f"Already created: {sorted(existing_characters)}")
    
    # Find all available HTML files
    all_html_files = []
    for file in os.listdir(html_dir):
        if file.endswith('.html'):
            char_name = file.replace('.html', '')
            all_html_files.append(char_name)
    
    # Find characters that need to be processed
    remaining_characters = []
    for char in all_html_files:
        if char not in existing_characters:
            remaining_characters.append(char)
    
    remaining_characters = sorted(remaining_characters)
    print(f"Need to process: {remaining_characters}")
    print(f"Total characters to process: {len(remaining_characters)}")
    
    if not remaining_characters:
        print("All characters have already been processed!")
        return
    
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # Process each remaining character
    success_count = 0
    failed_characters = []
    
    for character in remaining_characters:
        html_file = os.path.join(html_dir, f"{character}.html")
        print(f"\n{'='*50}")
        print(f"Processing {character} ({success_count + 1}/{len(remaining_characters)})")
        print(f"{'='*50}")
        
        character_data = extract_character_data(html_file)
        if character_data:
            try:
                output_file = save_character_data(character_data, output_dir)
                print(f"✅ Successfully saved {character} data to: {os.path.basename(output_file)}")
                success_count += 1
                
                # Show sample move for verification
                if character_data['moves']:
                    sample_move = character_data['moves'][0]
                    print(f"   Sample move: {sample_move['name']['japanese']}")
                    print(f"   Frames: S{sample_move['frames']['startup']} | A{sample_move['frames']['active']} | R{sample_move['frames']['recovery']}")
                    print(f"   Hit/Block: {sample_move['frames']['on_hit']}/{sample_move['frames']['on_block']} | Damage: {sample_move['properties']['damage']}")
                
            except Exception as e:
                print(f"❌ Failed to save {character} data: {e}")
                failed_characters.append(character)
        else:
            print(f"❌ Failed to extract {character} data")
            failed_characters.append(character)
    
    # Summary
    print(f"\n{'='*60}")
    print(f"EXTRACTION COMPLETE")
    print(f"{'='*60}")
    print(f"✅ Successfully processed: {success_count}/{len(remaining_characters)} characters")
    
    if failed_characters:
        print(f"❌ Failed characters: {failed_characters}")
    
    print(f"\nAll character JSON files are now in: {output_dir}")

if __name__ == '__main__':
    main()