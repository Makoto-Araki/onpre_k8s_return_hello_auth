# onpre_k8s_return_hello_auth (FastAPI + Redis認証)

## 概要(Overview)
FastAPI を用いてアクセストークン / リフレッシュトークン方式の認証を Redis を使用して実装したサンプルアプリで以下の仕組みを含みます。
- 有効期限付きアクセストークン
- 有効期限付きリフレッシュトークン
- リフレッシュトークンのローテーション
- リフレッシュトークン再利用検知
- Kubernetes 上へのデプロイ
```note
外部の認証基盤(OAuthサーバ等)に依存せず、API認証の内部動作の理解を目的
```

## アーキテクチャ
Client
  |
  |  HTTP (Bearer Token)
  v
FastAPI (Kubernetes Pods)
  |
  |  Token管理・検証
  v
Redis (共有)

## 認証設計
### トークンの種類
| トークン             | 説明                                          |
| ------------------- | --------------------------------------------- |
| アクセストークン     | APIへアクセスするための短命トークン              |
| リフレッシュトークン | 新しいアクセストークンを取得するための長命トークン |

### トークンの有効期限
| トークン             | 説明                                          |
| ------------------- | --------------------------------------------- |
| アクセストークン     | 300秒 (5分)                                     |
| リフレッシュトークン | 3600秒 (60分)                                   |
```note
RedisのTTL機能を利用して自動失効
```

### アクセストークン検証
- クライアントは Authorization ヘッダにトークン付与
- 形式 Authorization: Bear <access_token>
- FastAPIのDependencyで Redis 上での存在確認

### リフレッシュトークン再利用検知
- 既に使用済みのリフレッシュトークンを再送信
- リクエスト拒否
- トークン漏洩の可能性ありと判断
```note
リフレッシュトークンの不正利用の早期検知を実現
```

### APIエンドポイント一覧
| Method | Path     | 説明                 | 認証 |
| ------ | -------- | -------------------- | ---- |
| POST   | /login   | ログイン・トークン発行 | 不要 |
| POST   | /refresh | トークン更新          | 不要 |
| GET    | /hello1  | 認証必須API           | 必要 |
| GET    | /hello2  | 認証必須API           | 必要 |
| GET    | /hello3  | 認証必須API           | 必要 |
| GET    | /health  | ヘルスチェック        | 不要 |

## クイックスタート
### 開発環境
```bash
## ディレクトリ作成
$ mkdir onpre_k8s_return_hello_auth

## ディレクトリ移動
$ cd onpre_k8s_return_hello_auth

## リモートリポジトリ複製
$ git clone git@github.com:Makoto-Araki/onpre_k8s_return_hello_auth.git

## Dev-Container用イメージビルド
$ docker build --no-cache -t onpre_k8s_return_hello_auth_image .

## Dev-Container用イメージからVSCode上でDev-Container起動
$ code .
```

### Docker-Desktop上のKubernetesクラスタにデプロイ
```bash
## コンテキスト一覧
$ kubectl config get-contexts

## コンテキスト確認
$ kubectl config current-context

## namespace一覧
$ kubectl get namespaces

## namespace作成
$ kubectl create namespace user-apps

## Redis用のService作成
$ kubectl apply -n user-apps -f k8s/redis-service.yaml

## Redis用のStatefulSet作成
$ kubectl apply -n user-apps -f k8s/redis-statefulset.yaml

## Deploymentリソース差分確認
$ kubectl diff -n user-apps -f k8s/deployment.yaml

## Deploymentリソース作成または更新
$ kubectl apply -n user-apps -f k8s/deployment.yaml

## Deploymentリソース確認
$ kubectl get deployments -n user-apps

## Ingress-Controller導入
$ kubectl apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/main/deploy/static/provider/cloud/deploy.yaml

## Ingress-ControllerのPod確認
$ kubectl get pods -n ingress-nginx

## Ingress-ControllerのService確認
$ kubectl get service -n ingress-nginx

## Service作成
$ kubectl apply -n user-apps -f k8s/service.yaml

## Ingress作成
$ kubectl apply -n user-apps -f k8s/ingress.yaml

## Windows側のhostsファイル修正
$ notepad C:\Windows\System32\drivers\etc\hosts ※127.0.0.1 araki.comを追記
```

### ログイン
```bash
$ curl -X POST "http://araki.com/login?username=admin&password=password"
```

### ログインのレスポンス
```bash
{
    "access_token": "ACCESS_TOKEN_01",
    "refresh_token": "REFRESH_TOKEN_01",
    "token_type": "bearer"
    "expires_in": 300,
}
```

### 認証付きAPI呼び出し
```bash
$ curl -H "Authorization: Bear ACCESS_TOKEN" http://araki.com/hello1
```

### 認証付きAPI呼び出しのレスポンス
```bash
{
    "message": "Hello1"
}
```

### トークン更新
```bash
curl -X POST "http://araki.com/refresh?refresh_token=REFRESH_TOKEN_01"
```

### トークン更新のレスポンス
```bash
{
    "access_token": "ACCESS_TOKEN_02",  # 新しいアクセストークン発行
    "refresh_token": "REFRESH_TOKEN_02",  # 新しいリフレッシュトークン発行
    "token_type": "bearer",
    "expire_in": 300
}
```
```note
古いリフレッシュトークン REFRESH_TOKEN_01 は無効化
```

### リフレッシュトークン再利用検知
```bash
curl -X POST "http://araki.com/refresh?refresh_token=REFRESH_TOKEN_01"
```

### リフレッシュトークン再利用検知のレスポンス
```bash
{
    "detail": "Refresh token reuse detected"
}
```
