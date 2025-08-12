import { Sword } from 'lucide-react';
import { Character } from '../types/frameData';
import { CharacterSelect } from './CharacterSelect';

interface CharacterSelectionSectionProps {
  characters: Character[];
  attackerCharacter: string;
  defenderCharacter: string;
  onAttackerChange: (characterId: string) => void;
  onDefenderChange: (characterId: string) => void;
}

export const CharacterSelectionSection = ({
  characters,
  attackerCharacter,
  defenderCharacter,
  onAttackerChange,
  onDefenderChange,
}: CharacterSelectionSectionProps) => {
  return (
    <div className="bg-white/10 backdrop-blur-lg rounded-2xl border border-white/20 p-6 mb-6">
      <h2 className="text-2xl font-bold text-white mb-6 flex items-center">
        <Sword className="w-6 h-6 mr-2 text-red-400" />
        キャラクター選択
      </h2>

      <div className="grid md:grid-cols-2 gap-6">
        <div className="bg-red-500/20 rounded-lg p-4 border border-red-400/30">
          <CharacterSelect
            characters={characters}
            selectedCharacter={attackerCharacter}
            onCharacterChange={onAttackerChange}
            label="攻撃側キャラクター"
            id="attacker-select"
          />
        </div>

        <div className="bg-blue-500/20 rounded-lg p-4 border border-blue-400/30">
          <CharacterSelect
            characters={characters}
            selectedCharacter={defenderCharacter}
            onCharacterChange={onDefenderChange}
            label="防御側キャラクター"
            id="defender-select"
          />
        </div>
      </div>
    </div>
  );
};