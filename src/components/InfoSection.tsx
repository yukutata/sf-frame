import { Info } from 'lucide-react';

export const InfoSection = () => {
  return (
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
  );
};