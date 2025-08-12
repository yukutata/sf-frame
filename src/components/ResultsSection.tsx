import { Zap } from 'lucide-react';
import { Move } from '../types/frameData';
import { PunishList } from './PunishList';

interface ResultsSectionProps {
  punishMoves: Move[];
  defenderCharacterName: string;
  attackerMove: Move | null;
}

export const ResultsSection = ({
  punishMoves,
  defenderCharacterName,
  attackerMove,
}: ResultsSectionProps) => {
  return (
    <div className="bg-white/10 backdrop-blur-lg rounded-2xl border border-white/20 p-6">
      <h2 className="text-2xl font-bold text-white mb-6 flex items-center">
        <Zap className="w-6 h-6 mr-2 text-green-400" />
        確定反撃一覧
      </h2>

      <PunishList
        punishMoves={punishMoves}
        defenderCharacterName={defenderCharacterName}
        attackerMove={attackerMove}
      />
    </div>
  );
};