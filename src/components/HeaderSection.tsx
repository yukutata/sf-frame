import { Zap } from 'lucide-react';

export const HeaderSection = () => {
  return (
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
  );
};