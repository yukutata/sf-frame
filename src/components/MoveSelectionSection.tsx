import { Shield } from 'lucide-react';
import { Character } from '../types/frameData';
import { MoveSelect } from './MoveSelect';

interface MoveSelectionSectionProps {
  attackerData: Character | undefined;
  selectedMove: string;
  onMoveChange: (moveIndex: string) => void;
}

export const MoveSelectionSection: React.FC<MoveSelectionSectionProps> = ({
  attackerData,
  selectedMove,
  onMoveChange,
}) => {
  if (!attackerData) return null;

  return (
    <div className="bg-white/10 backdrop-blur-lg rounded-2xl border border-white/20 p-6 mb-6">
      <h2 className="text-2xl font-bold text-white mb-6 flex items-center">
        <Shield className="w-6 h-6 mr-2 text-yellow-400" />
        技選択
      </h2>

      <MoveSelect
        moves={attackerData.moves}
        selectedMove={selectedMove}
        onMoveChange={onMoveChange}
        disabled={!attackerData}
      />
    </div>
  );
};