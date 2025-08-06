import React, { useState, useMemo } from 'react';
import { Zap, Shield, Sword, Info } from 'lucide-react';
import { CHARACTERS } from './data/characters';
import { CharacterSelect } from './components/CharacterSelect';
import { MoveSelect } from './components/MoveSelect';
import { PunishList } from './components/PunishList';

function App() {
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

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-900 via-purple-900 to-red-900">
      <div className="container mx-auto px-4 py-8">
        {/* Header */}
        <div className="text-center mb-12">
          <div className="flex justify-center items-center mb-4">
            <Zap className="w-10 h-10 text-yellow-400 mr-3" />
            <h1 className="text-4xl md:text-5xl font-bold text-white bg-gradient-to-r from-yellow-400 to-red-400 bg-clip-text text-transparent">
              SF6 確反チェッカー
            </h1>
            <Zap className="w-10 h-10 text-yellow-400 ml-3" />
          </div>
          <p className="text-xl text-gray-300">
            ストリートファイター6の確定反撃を瞬時にチェック
          </p>
        </div>

        {/* Character Selection */}
        <div className="max-w-6xl mx-auto mb-8">
          <div className="bg-white/10 backdrop-blur-lg rounded-2xl border border-white/20 p-6 mb-6">
            <h2 className="text-2xl font-bold text-white mb-6 flex items-center">
              <Sword className="w-6 h-6 mr-2 text-red-400" />
              キャラクター選択
            </h2>
            
            <div className="grid md:grid-cols-2 gap-6">
              <div className="bg-red-500/20 rounded-lg p-4 border border-red-400/30">
                <CharacterSelect
                  characters={CHARACTERS}
                  selectedCharacter={attackerCharacter}
                  onCharacterChange={handleAttackerChange}
                  label="攻撃側キャラクター"
                  id="attacker-select"
                />
              </div>

              <div className="bg-blue-500/20 rounded-lg p-4 border border-blue-400/30">
                <CharacterSelect
                  characters={CHARACTERS}
                  selectedCharacter={defenderCharacter}
                  onCharacterChange={setDefenderCharacter}
                  label="防御側キャラクター"
                  id="defender-select"
                />
              </div>
            </div>
          </div>

          {/* Move Selection */}
          {attackerData && (
            <div className="bg-white/10 backdrop-blur-lg rounded-2xl border border-white/20 p-6 mb-6">
              <h2 className="text-2xl font-bold text-white mb-6 flex items-center">
                <Shield className="w-6 h-6 mr-2 text-yellow-400" />
                技選択
              </h2>
              
              <MoveSelect
                moves={attackerData.moves}
                selectedMove={selectedMove}
                onMoveChange={setSelectedMove}
                disabled={!attackerData}
              />
            </div>
          )}
        </div>

        {/* Results */}
        <div className="max-w-6xl mx-auto">
          <div className="bg-white/10 backdrop-blur-lg rounded-2xl border border-white/20 p-6">
            <h2 className="text-2xl font-bold text-white mb-6 flex items-center">
              <Zap className="w-6 h-6 mr-2 text-green-400" />
              確定反撃一覧
            </h2>

            <PunishList
              punishMoves={punishMoves}
              defenderCharacterName={defenderData?.character_name.japanese || ''}
              attackerMove={selectedMoveData}
            />
          </div>
        </div>

        {/* Info Panel */}
        <div className="max-w-6xl mx-auto mt-8">
          <div className="bg-white/5 backdrop-blur-lg rounded-xl border border-white/10 p-4">
            <div className="flex items-start space-x-3">
              <Info className="w-5 h-5 text-blue-400 mt-0.5 flex-shrink-0" />
              <div className="text-sm text-gray-300">
                <p className="mb-2">
                  <span className="font-semibold text-white">使い方:</span> 
                  攻撃側のキャラクターと技を選択すると、防御側が確定反撃できる技が表示されます。
                </p>
                <p className="mb-2">
                  <span className="font-semibold text-white">確定反撃の条件:</span> 
                  攻撃技のガード硬直差（マイナス値）の絶対値以下の発生フレームを持つ技が確定反撃となります。
                </p>
                <p>
                  <span className="font-semibold text-white">注意:</span> 
                  実際の対戦では距離や状況によって確定反撃が成立しない場合があります。
                </p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default App;