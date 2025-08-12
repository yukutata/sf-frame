import { Character } from '../types/frameData';

interface CharacterSelectProps {
  characters: Character[];
  selectedCharacter: string;
  onCharacterChange: (characterId: string) => void;
  label: string;
  id: string;
}

export const CharacterSelect = ({
  characters,
  selectedCharacter,
  onCharacterChange,
  label,
  id
}: CharacterSelectProps) => {
  return (
    <div className="flex flex-col space-y-2">
      <label htmlFor={id} className="text-sm font-semibold text-white">
        {label}
      </label>
      <select
        id={id}
        value={selectedCharacter}
        onChange={(e) => onCharacterChange(e.target.value)}
        className="px-4 py-3 bg-white border-2 border-gray-300 rounded-lg shadow-sm focus:border-blue-500 focus:ring-2 focus:ring-blue-200 transition-all duration-200 text-gray-700 font-medium"
      >
        <option value="">キャラクターを選択</option>
        {characters.map((character) => (
          <option key={character.character} value={character.character}>
            {character.character_name.japanese} ({character.character_name.english})
          </option>
        ))}
      </select>
    </div>
  );
};