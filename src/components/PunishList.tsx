import React from 'react';
import { Move } from '../types/frameData';

interface PunishListProps {
  punishMoves: Move[];
  defenderCharacterName: string;
  attackerMove: Move | null;
}

export const PunishList: React.FC<PunishListProps> = ({
  punishMoves,
  defenderCharacterName,
  attackerMove
}) => {
  const getMoveTypeColor = (type: Move['type']) => {
    switch (type) {
      case 'standing_normal':
      case 'crouching_normal':
      case 'jumping_normal':
      case 'normal':
        return 'bg-blue-100 text-blue-800 border-blue-200';
      case 'special_normal':
      case 'special_move':
        return 'bg-yellow-100 text-yellow-800 border-yellow-200';
      case 'super_art':
        return 'bg-red-100 text-red-800 border-red-200';
      case 'throw':
        return 'bg-purple-100 text-purple-800 border-purple-200';
      case 'system':
        return 'bg-green-100 text-green-800 border-green-200';
      default:
        return 'bg-gray-100 text-gray-800 border-gray-200';
    }
  };

  const getMoveTypeBadge = (type: Move['type']) => {
    switch (type) {
      case 'standing_normal':
      case 'crouching_normal':
      case 'jumping_normal':
      case 'normal':
        return '通常技';
      case 'special_normal':
        return '特殊技';
      case 'special_move':
        return '必殺技';
      case 'super_art':
        return 'SA';
      case 'throw':
        return '投げ';
      case 'system':
        return 'システム';
      default:
        return '';
    }
  };

  if (!attackerMove) {
    return (
      <div className="bg-gray-50 rounded-lg p-8 text-center">
        <div className="text-gray-400 text-lg">
          攻撃側のキャラクターと技を選択してください
        </div>
      </div>
    );
  }

  if (punishMoves.length === 0) {
    return (
      <div className="bg-yellow-50 rounded-lg p-8 text-center border border-yellow-200">
        <div className="text-yellow-600 text-lg font-medium">
          確定反撃可能な技がありません
        </div>
        <div className="text-yellow-500 text-sm mt-2">
          ガード硬直差 {attackerMove.frames.on_block && typeof attackerMove.frames.on_block === 'number' && attackerMove.frames.on_block >= 0 ? '+' : ''}{attackerMove.frames.on_block}F に対して確反できる技は見つかりませんでした
        </div>
      </div>
    );
  }

  const filteredPunishMoves = punishMoves.filter((move) => {
    const startup = move.frames.startup;
    const onBlock = move.frames.on_block;
    return startup !== null && typeof startup === 'number' && startup > 3 &&
           onBlock !== null;
  });

  return (
    <div className="space-y-4">
      <div className="bg-gradient-to-r from-green-50 to-blue-50 rounded-lg p-4 border border-green-200">
        <h3 className="text-lg font-bold text-gray-800 mb-2">
          {defenderCharacterName}の確定反撃技 ({filteredPunishMoves.length}個)
        </h3>
        <div className="text-sm text-gray-600">
          <span className="font-medium">{attackerMove.name.japanese}</span> のガード硬直差
          <span className="font-bold text-red-600 mx-1">
            {attackerMove.frames.on_block && typeof attackerMove.frames.on_block === 'number' && attackerMove.frames.on_block >= 0 ? '+' : ''}{attackerMove.frames.on_block}F
          </span>
          に対する確定反撃
        </div>
      </div>

      <div className="grid gap-3">
        {filteredPunishMoves
          .sort((a, b) => {
            const aStartup = typeof a.frames.startup === 'number' ? a.frames.startup : 999;
            const bStartup = typeof b.frames.startup === 'number' ? b.frames.startup : 999;
            return bStartup - aStartup;
          }) // 発生フレームでソート
          .map((move, index) => (
            <div
              key={index}
              className="bg-white rounded-lg border-2 border-gray-200 p-4 hover:border-blue-300 hover:shadow-md transition-all duration-200"
            >
              <div className="flex items-center justify-between mb-3">
                <div className="flex items-center space-x-3">
                  <h4 className="text-lg font-bold text-gray-800">{move.name.japanese}</h4>
                  <span className={`px-2 py-1 rounded-full text-xs font-medium border ${getMoveTypeColor(move.type)}`}>
                    {getMoveTypeBadge(move.type)}
                  </span>
                </div>
                <div className="text-right">
                  <div className="text-xs text-gray-500">猶予フレーム</div>
                  <div className="font-bold text-green-600">
                    {attackerMove.frames.on_block && move.frames.startup &&
                     typeof attackerMove.frames.on_block === 'number' &&
                     typeof move.frames.startup === 'number' ?
                     Math.abs(attackerMove.frames.on_block) - move.frames.startup + 1 : '?'}F
                  </div>
                </div>
              </div>

              <div className="grid grid-cols-2 md:grid-cols-5 gap-3 text-sm">
                <div className="bg-blue-50 p-2 rounded border">
                  <div className="text-gray-500 text-xs">発生</div>
                  <div className="font-bold text-blue-600">{move.frames.startup}F</div>
                </div>

                <div className="bg-green-50 p-2 rounded border">
                  <div className="text-gray-500 text-xs">持続</div>
                  <div className="font-bold text-green-600">{move.frames.active}F</div>
                </div>

                <div className="bg-purple-50 p-2 rounded border">
                  <div className="text-gray-500 text-xs">ダメージ</div>
                  <div className="font-bold text-purple-600">{move.properties.damage || '-'}</div>
                </div>

                <div className="bg-yellow-50 p-2 rounded border">
                  <div className="text-gray-500 text-xs">ヒット硬直差</div>
                  <div className={`font-bold ${typeof move.frames.on_hit === 'number' && move.frames.on_hit >= 0 ? 'text-green-600' : 'text-red-600'}`}>
                    {typeof move.frames.on_hit === 'number' && move.frames.on_hit >= 0 ? '+' : ''}{move.frames.on_hit}F
                  </div>
                </div>

                <div className="bg-red-50 p-2 rounded border">
                  <div className="text-gray-500 text-xs">ガード硬直差</div>
                  <div className={`font-bold ${typeof move.frames.on_block === 'number' && move.frames.on_block >= 0 ? 'text-green-600' : 'text-red-600'}`}>
                    {typeof move.frames.on_block === 'number' && move.frames.on_block >= 0 ? '+' : ''}{move.frames.on_block}F
                  </div>
                </div>
              </div>
            </div>
          ))}
      </div>
    </div>
  );
};