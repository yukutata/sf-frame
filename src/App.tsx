import { CHARACTERS } from './data/characters';
import { useFrameChecker } from './hooks/useFrameChecker';
import { HeaderSection } from './components/HeaderSection';
import { CharacterSelectionSection } from './components/CharacterSelectionSection';
import { MoveSelectionSection } from './components/MoveSelectionSection';
import { ResultsSection } from './components/ResultsSection';
import { InfoSection } from './components/InfoSection';

const App = () => {
  const {
    attackerCharacter,
    defenderCharacter,
    selectedMove,
    attackerData,
    defenderData,
    selectedMoveData,
    punishMoves,
    setAttackerCharacter,
    setDefenderCharacter,
    setSelectedMove,
  } = useFrameChecker();

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-900 via-purple-900 to-red-900">
      <div className="container mx-auto px-4 py-8">
        <HeaderSection />

        <div className="max-w-6xl mx-auto mb-8">
          <CharacterSelectionSection
            characters={CHARACTERS}
            attackerCharacter={attackerCharacter}
            defenderCharacter={defenderCharacter}
            onAttackerChange={setAttackerCharacter}
            onDefenderChange={setDefenderCharacter}
          />

          <MoveSelectionSection
            attackerData={attackerData}
            selectedMove={selectedMove}
            onMoveChange={setSelectedMove}
          />
        </div>

        <div className="max-w-6xl mx-auto">
          <ResultsSection
            punishMoves={punishMoves}
            defenderCharacterName={defenderData?.character_name.japanese || ''}
            attackerMove={selectedMoveData}
          />
        </div>

        <div className="max-w-6xl mx-auto mt-8">
          <InfoSection />
        </div>
      </div>
    </div>
  );
}

export default App;