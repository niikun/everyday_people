# うがい習慣アプリ

Flask + React で作られた、子供のうがい習慣を促進するアプリです。3つのゲームから1つがランダムに選ばれて遊べます。

## 機能

- **うがい記録**: 毎日のうがいを記録してスタンプを集める
- **ゲーム抽選**: 3つのゲームから1つがランダムに選ばれる
  - 星キャッチゲーム: 落ちてくる星をクリックしてキャッチ
  - メモリーマッチングゲーム: 同じ色のカードをマッチさせる
  - お絵かきゲーム: 自由にお絵かきする
- **進捗管理**: 連続日数や合計日数を記録

## セットアップ

### 必要なもの
- Python 3.7+
- Node.js 14+ (フロントエンド用)
- npm (Node.js に含まれる)

### 簡単起動
```bash
python run.py
```

### 手動セットアップ

1. **Python 依存関係のインストール**
```bash
pip install flask flask-cors
```

2. **フロントエンド依存関係のインストール**
```bash
cd frontend
npm install
```

3. **フロントエンドのビルド**
```bash
npm run build
cd ..
```

4. **アプリケーションの起動**
```bash
python app.py
```

## 使い方

1. ブラウザで `http://localhost:5000` にアクセス
2. 「うがいしました」ボタンを押してスタンプをもらう
3. 「ゲームで遊ぶ」ボタンでゲームを開始
4. 3つのゲームから1つがランダムに選ばれる
5. ゲームをクリアしてスコアを獲得

## ファイル構成

```
/
├── app.py              # Flask バックエンド
├── run.py              # 簡単起動スクリプト
├── requirements.txt    # Python 依存関係
├── gargle_progress.json # 進捗データ (自動生成)
└── frontend/
    ├── package.json    # Node.js 依存関係
    ├── public/
    │   └── index.html  # HTML テンプレート
    └── src/
        ├── App.js      # メインアプリコンポーネント
        ├── App.css     # スタイル
        ├── index.js    # エントリーポイント
        └── components/ # React コンポーネント
            ├── MainScreen.js
            ├── GameIntro.js
            ├── CatchingGame.js
            ├── MemoryGame.js
            ├── DrawingGame.js
            └── GameResult.js
```

## API エンドポイント

- `GET /api/progress` - 進捗データの取得
- `POST /api/stamp` - スタンプの付与
- `POST /api/game/select` - ゲームの抽選
- `POST /api/game/result` - ゲーム結果の保存

## 開発モード

開発モードでフロントエンドを起動:
```bash
cd frontend
npm start
```

バックエンドを起動:
```bash
python app.py
```

フロントエンドは `http://localhost:3000`、バックエンドは `http://localhost:5000` で動作します。