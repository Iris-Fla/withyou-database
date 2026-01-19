# WithYou Database

場所と写真を管理するためのREST APIサーバーです。FastAPIとSQLAlchemyを使用して構築されています。

## 概要

このプロジェクトは、地理的な場所情報と関連する写真を管理するためのデータベースシステムです。ユーザーが場所を登録し、その場所に複数の写真をアップロードできます。

## 機能

### 場所（Place）
- ✅ **作成**: 新しい場所を登録
- ✅ **読取**: すべての場所または特定の場所を取得
- ✅ **更新**: 既存の場所情報を更新
- ✅ **削除**: 場所と関連する写真を削除

### 写真（Photo）
- ✅ **作成**: 場所に写真をアップロード
- ✅ **読取**: 写真情報を取得
- ✅ **削除**: 写真を削除

## 技術スタック

- **Framework**: FastAPI
- **ORM**: SQLAlchemy
- **Database**: MySQL
- **Containerization**: Docker & Docker Compose
- **Language**: Python 3.11+

## セットアップ

### 前提条件

- Docker
- Docker Compose

### インストール

1. リポジトリをクローン
```bash
git clone <repository-url>
cd withyou-database
```

2. 環境変数を設定（必要に応じて）
```bash
# .envファイルを作成して設定
```

3. Dockerコンテナを起動
```bash
docker-compose up -d --build
```

4. APIサーバーは `http://localhost:8000` で利用可能です

## API エンドポイント

### 場所（Places）

| メソッド | エンドポイント | 説明 |
|---------|---------------|------|
| POST | `/places/` | 新しい場所を作成 |
| GET | `/places/` | すべての場所を取得 |
| GET | `/places/{place_id}` | 特定の場所を取得 |
| PUT | `/places/{place_id}` | 場所を更新 |
| DELETE | `/places/{place_id}` | 場所を削除 |

### 写真（Photos）

| メソッド | エンドポイント | 説明 |
|---------|---------------|------|
| POST | `/places/{place_id}/photos/` | 写真をアップロード |
| GET | `/photos/` | すべての写真を取得 |
| GET | `/photos/{photo_id}` | 特定の写真を取得 |
| DELETE | `/photos/{photo_id}` | 写真を削除 |

## 使用例

### 場所を作成
```bash
curl -X POST "http://localhost:8000/places/" \
  -H "Content-Type: application/json" \
  -d '{
    "lat": 35.6762,
    "lng": 139.6503,
    "title": "東京駅",
    "description": "東京の主要な駅"
  }'
```

### 写真をアップロード
```bash
curl -X POST "http://localhost:8000/places/1/photos/" \
  -F "file=@/path/to/photo.jpg"
```

### 場所を更新
```bash
curl -X PUT "http://localhost:8000/places/1" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "更新されたタイトル"
  }'
```

### 場所を削除
```bash
curl -X DELETE "http://localhost:8000/places/1"
```

## プロジェクト構造

```
withyou-database/
├── app/
│   ├── main.py          # FastAPIアプリケーション
│   ├── models.py        # SQLAlchemyモデル
│   ├── schemas.py       # Pydanticスキーマ
│   ├── database.py      # データベース設定
│   └── __pycache__/
├── static/              # アップロードされた写真の保存先
├── docker-compose.yml   # Docker Compose設定
├── Dockerfile           # Dockerイメージ定義
├── requirements.txt     # Python依存関係
└── README.md           # このファイル
```

## 環境変数

必要に応じて `.env` ファイルで以下の環境変数を設定できます：

```
DATABASE_URL=postgresql://user:password@db:5432/withyou
```

## トラブルシューティング

### コンテナが起動しない場合
```bash
# ログを確認
docker-compose logs -f

# コンテナを再構築
docker-compose down
docker-compose up -d --build
```

### データベース接続エラー
- PostgreSQLコンテナが実行中か確認
- `docker-compose ps` でコンテナの状態を確認
- `DATABASE_URL`が正しく設定されているか確認

## 作成者

WithYou Team
