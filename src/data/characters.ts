import { Character } from '../types/frameData';
import ryuData from './ryu_frame_data_structured.json';
import kenData from './ken_frame_data_structured.json';
import chunliData from './chunli_frame_data_structured.json';
import lukeData from './luke_frame_data_structured.json';
import cammyData from './cammy_frame_data_structured.json';
import akiData from './aki_frame_data_structured.json';
import blankaData from './blanka_frame_data_structured.json';
import deejayData from './deejay_frame_data_structured.json';
import dhalsimData from './dhalsim_frame_data_structured.json';
import edData from './ed_frame_data_structured.json';
import ehondaData from './ehonda_frame_data_structured.json';
import elenaData from './elena_frame_data_structured.json';
import goukiData from './gouki_frame_data_structured.json';
import guileData from './guile_frame_data_structured.json';
import jamieData from './jamie_frame_data_structured.json';
import jpData from './jp_frame_data_structured.json';
import juriData from './juri_frame_data_structured.json';
import kimberlyData from './kimberly_frame_data_structured.json';
import lilyData from './lily_frame_data_structured.json';
import maiData from './mai_frame_data_structured.json';
import manonData from './manon_frame_data_structured.json';
import marisaData from './marisa_frame_data_structured.json';
import rashidData from './rashid_frame_data_structured.json';
import sagatData from './sagat_frame_data_structured.json';
import terryData from './terry_frame_data_structured.json';
import vegaMbisonData from './vega_mbison_frame_data_structured.json';
import zangiefData from './zangief_frame_data_structured.json';

export const RYU_CHARACTER: Character = ryuData as Character;
export const KEN_CHARACTER: Character = kenData as Character;
export const CHUNLI_CHARACTER: Character = chunliData as Character;
export const LUKE_CHARACTER: Character = lukeData as Character;
export const CAMMY_CHARACTER: Character = cammyData as Character;
export const AKI_CHARACTER: Character = akiData as Character;
export const BLANKA_CHARACTER: Character = blankaData as Character;
export const DEEJAY_CHARACTER: Character = deejayData as Character;
export const DHALSIM_CHARACTER: Character = dhalsimData as Character;
export const ED_CHARACTER: Character = edData as Character;
export const EHONDA_CHARACTER: Character = ehondaData as Character;
export const ELENA_CHARACTER: Character = elenaData as Character;
export const GOUKI_CHARACTER: Character = goukiData as Character;
export const GUILE_CHARACTER: Character = guileData as Character;
export const JAMIE_CHARACTER: Character = jamieData as Character;
export const JP_CHARACTER: Character = jpData as Character;
export const JURI_CHARACTER: Character = juriData as Character;
export const KIMBERLY_CHARACTER: Character = kimberlyData as Character;
export const LILY_CHARACTER: Character = lilyData as Character;
export const MAI_CHARACTER: Character = maiData as Character;
export const MANON_CHARACTER: Character = manonData as Character;
export const MARISA_CHARACTER: Character = marisaData as Character;
export const RASHID_CHARACTER: Character = rashidData as Character;
export const SAGAT_CHARACTER: Character = sagatData as Character;
export const TERRY_CHARACTER: Character = terryData as Character;
export const VEGA_MBISON_CHARACTER: Character = vegaMbisonData as Character;
export const ZANGIEF_CHARACTER: Character = zangiefData as Character;

export const CHARACTERS: Character[] = [
  RYU_CHARACTER,
  KEN_CHARACTER,
  CHUNLI_CHARACTER,
  LUKE_CHARACTER,
  CAMMY_CHARACTER,
  AKI_CHARACTER,
  BLANKA_CHARACTER,
  DEEJAY_CHARACTER,
  DHALSIM_CHARACTER,
  ED_CHARACTER,
  EHONDA_CHARACTER,
  ELENA_CHARACTER,
  GOUKI_CHARACTER,
  GUILE_CHARACTER,
  JAMIE_CHARACTER,
  JP_CHARACTER,
  JURI_CHARACTER,
  KIMBERLY_CHARACTER,
  LILY_CHARACTER,
  MAI_CHARACTER,
  MANON_CHARACTER,
  MARISA_CHARACTER,
  RASHID_CHARACTER,
  SAGAT_CHARACTER,
  TERRY_CHARACTER,
  VEGA_MBISON_CHARACTER,
  ZANGIEF_CHARACTER
];

export const getCharacterById = (id: string): Character | undefined => {
  return CHARACTERS.find(character => character.character === id);
};

export const getCharacterByName = (name: string): Character | undefined => {
  return CHARACTERS.find(character => 
    character.character_name.english.toLowerCase() === name.toLowerCase() ||
    character.character_name.japanese === name
  );
};