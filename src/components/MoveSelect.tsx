import React from 'react';
import { Move } from '../types/frameData';

interface MoveSelectProps {
  moves: Move[];
  selectedMove: string;
  onMoveChange: (moveIndex: string) => void;
  disabled: boolean;
}

export const MoveSelect: React.FC<MoveSelectProps> = ({
  moves,
  selectedMove,
  onMoveChange,
  disabled
}) => {
  const getMoveTypeColor = (type: Move['type']) => {
    switch (type) {
      case 'standing_normal':
      case 'crouching_normal':
      case 'jumping_normal':
      case 'normal':
        return 'bg-blue-50 text-blue-700';
      case 'special_normal':
      case 'special_move':
        return 'bg-yellow-50 text-yellow-700';
      case 'super_art':
        return 'bg-red-50 text-red-700';
      case 'throw':
        return 'bg-purple-50 text-purple-700';
      case 'system':
        return 'bg-green-50 text-green-700';
      default:
        return 'bg-gray-50 text-gray-700';
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

  return (
    <div className="flex flex-col space-y-2">
      <label htmlFor="move-select" className="text-sm font-semibold text-white">
        攻撃技
      </label>
      <select
        id="move-select"
        value={selectedMove}
        onChange={(e) => onMoveChange(e.target.value)}
        disabled={disabled}
        className="px-4 py-3 bg-white border-2 border-gray-300 rounded-lg shadow-sm focus:border-blue-500 focus:ring-2 focus:ring-blue-200 transition-all duration-200 text-gray-700 font-medium disabled:bg-gray-100 disabled:cursor-not-allowed"
      >
        <option value="">技を選択</option>
        {moves
          .filter((move) => {
            const startup = move.frames.startup;
            const onBlock = move.frames.on_block;
            return startup !== null && typeof startup === 'number' && startup > 3 &&
                   onBlock !== null;
          })
          .map((move, index) => (
            <option key={index} value={moves.indexOf(move).toString()}>
              {move.name.japanese} (発生{move.frames.startup}F / ガード{typeof move.frames.on_block === 'number' && move.frames.on_block >= 0 ? '+' : ''}{move.frames.on_block})
            </option>
          ))}
      </select>

      {selectedMove !== '' && moves[parseInt(selectedMove)] && (
        <div className="mt-3 p-4 bg-gradient-to-r from-gray-50 to-blue-50 rounded-lg border border-gray-200">
          <div className="flex items-center justify-between mb-2">
            <h4 className="text-lg font-bold text-gray-800">{moves[parseInt(selectedMove)].name.japanese}</h4>
            <span className={`px-2 py-1 rounded-full text-xs font-medium ${getMoveTypeColor(moves[parseInt(selectedMove)].type)}`}>
              {getMoveTypeBadge(moves[parseInt(selectedMove)].type)}
            </span>
          </div>

          <div className="grid grid-cols-2 md:grid-cols-4 gap-3 text-sm">
            <div className="bg-white p-2 rounded border">
              <div className="text-gray-500 text-xs">発生</div>
              <div className="font-bold text-blue-600">{moves[parseInt(selectedMove)].frames.startup}F</div>
            </div>

            <div className="bg-white p-2 rounded border">
              <div className="text-gray-500 text-xs">持続</div>
              <div className="font-bold text-green-600">{moves[parseInt(selectedMove)].frames.active}F</div>
            </div>

            <div className="bg-white p-2 rounded border">
              <div className="text-gray-500 text-xs">ガード硬直差</div>
              <div className={`font-bold ${typeof moves[parseInt(selectedMove)].frames.on_block === 'number' && moves[parseInt(selectedMove)].frames.on_block >= 0 ? 'text-green-600' : 'text-red-600'}`}>
                {typeof moves[parseInt(selectedMove)].frames.on_block === 'number' && moves[parseInt(selectedMove)].frames.on_block >= 0 ? '+' : ''}{moves[parseInt(selectedMove)].frames.on_block}F
              </div>
            </div>

            <div className="bg-white p-2 rounded border">
              <div className="text-gray-500 text-xs">ダメージ</div>
              <div className="font-bold text-purple-600">{moves[parseInt(selectedMove)].properties.damage || '-'}</div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};