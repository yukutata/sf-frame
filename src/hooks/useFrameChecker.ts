import { useState, useMemo } from 'react';
import { CHARACTERS } from '../data/characters';

export const useFrameChecker = () => {
  const [attackerCharacter, setAttackerCharacter] = useState('');
  const [defenderCharacter, setDefenderCharacter] = useState('');
  const [selectedMove, setSelectedMove] = useState('');

  const attackerData = useMemo(() =>
    CHARACTERS.find(char => char.character === attackerCharacter),
    [attackerCharacter]
  );

  const defenderData = useMemo(() =>
    CHARACTERS.find(char => char.character === defenderCharacter),
    [defenderCharacter]
  );

  const selectedMoveData = useMemo(() => {
    if (!attackerData || selectedMove === '') return null;
    return attackerData.moves[parseInt(selectedMove)];
  }, [attackerData, selectedMove]);

  const punishMoves = useMemo(() => {
    if (!selectedMoveData || !defenderData) return [];

    const blockDisadvantage = selectedMoveData.frames.on_block;
    if (typeof blockDisadvantage !== 'number' || blockDisadvantage >= 0) return [];

    const absDisadvantage = Math.abs(blockDisadvantage);
    return defenderData.moves.filter(move => {
      const startup = move.frames.startup;
      return typeof startup === 'number' && startup <= absDisadvantage;
    });
  }, [selectedMoveData, defenderData]);

  const handleAttackerChange = (characterId: string) => {
    setAttackerCharacter(characterId);
    setSelectedMove('');
  };

  return {
    attackerCharacter,
    defenderCharacter,
    selectedMove,
    attackerData,
    defenderData,
    selectedMoveData,
    punishMoves,
    setAttackerCharacter: handleAttackerChange,
    setDefenderCharacter,
    setSelectedMove,
  };
};