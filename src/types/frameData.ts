export interface LocalizedName {
  japanese: string;
  english: string;
}

export interface FrameData {
  startup: number | null;
  active: number | string | null;
  recovery: number | string | null;
  on_hit: number | string | null;
  on_block: number | null;
}

export interface MoveProperties {
  damage: number | null;
  cancel: string;
  combo_scaling: string;
  attribute: string;
  notes: string;
}

export interface DriveSystemData {
  gain_on_hit: number | null;
  loss_on_guard: number | null;
  loss_on_punish: number | null;
}

export interface MoveName extends LocalizedName {
  japanese_base: string;
}

export interface MoveCategory extends LocalizedName {}

export interface Move {
  id: number;
  name: MoveName;
  category: MoveCategory;
  type: 'standing_normal' | 'crouching_normal' | 'jumping_normal' | 'normal' |
        'special_normal' | 'special_move' | 'super_art' | 'throw' | 'system' | 'other';
  frames: FrameData;
  properties: MoveProperties;
  drive_system: DriveSystemData;
  sa_gain: number | null;
}

export interface CategoryData extends LocalizedName {
  moves: number[];
}

export interface Character {
  character: string;
  character_name: LocalizedName;
  health: number;
  categories: Record<string, CategoryData>;
  moves: Move[];
}

// Utility functions for working with frame data
export const getMovesbyCategory = (data: Character, categoryKey: string): Move[] => {
  const category = data.categories[categoryKey];
  if (!category) return [];

  return category.moves.map(id => data.moves.find(move => move.id === id)).filter(Boolean) as Move[];
};

export const getMovesByType = (data: Character, type: Move['type']): Move[] => {
  return data.moves.filter(move => move.type === type);
};

export const getFrameAdvantage = (move: Move, onBlock: boolean = false): number | string | null => {
  return onBlock ? move.frames.on_block : move.frames.on_hit;
};

export const isPlus = (frameAdvantage: number | string | null): boolean => {
  if (typeof frameAdvantage === 'number') {
    return frameAdvantage > 0;
  }
  return false;
};

export const isSafe = (frameAdvantage: number | string | null): boolean => {
  if (typeof frameAdvantage === 'number') {
    return frameAdvantage >= -4;
  }
  return false;
};