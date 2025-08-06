# 開発環境用Dockerfile
FROM node:20-alpine

# 作業ディレクトリの設定
WORKDIR /app

# package.jsonとpackage-lock.jsonをコピー
COPY package*.json ./

# 依存関係のインストール
RUN npm ci

# アプリケーションのソースコードをコピー
COPY . .

# Viteのデフォルトポートを公開
EXPOSE 5173

# 開発サーバーの起動
CMD ["npm", "run", "dev"]