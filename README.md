# onpre_k8s_return_hello_auth (認証機能＋APIサーバー)

## プログラム開発
### Github上でIssue作成
![github_readme_01](images/github_readme_01.png)

### ローカルリポジトリ上で開発
```bash
## ディレクトリ作成
$ cd ~
$ mkdir onpre_k8s_return_hello_auth

## ローカルリポジトリ初期化
$ cd ~/onpre_k8s_return_hello_auth
$ git init

## ローカルリポジトリ設定 
$ git config --global user.email (自分のメールアドレス)
$ git config --global user.name Makoto-Araki

## ローカルリポジトリ設定
$ cd ~/onpre_k8s_return_hello_auth
$ git branch -M main

## リモートリポジトリ設定
$ cd ~/onpre_k8s_return_hello_auth
$ git remote add origin git@github.com:Makoto-Araki/onpre_k8s_return_hello_auth.git

## ブランチ確認
$ cd ~/onpre_k8s_return_hello_auth
$ git branch

## 別ブランチ作成
$ cd ~/onpre_k8s_return_hello_auth
$ git checkout -b feature/add-basicfiles

## 別ブランチをリモートリポジトリに反映
$ cd ~/onpre_k8s_return_hello_auth
$ git push -u origin feature/add-basicfiles

## 開発イメージ用のDockerfile作成
$ cd ~/onpre_k8s_return_hello_auth
$ vi Dockerfile

## プログラム用ディレクトリ作成
$ cd ~/onpre_k8s_return_hello_auth
$ mkdir app

## プログラム作成
$ cd ~/onpre_k8s_return_hello_auth
$ vi app/main.py

## テスト用ディレクトリ作成
$ cd ~/onpre_k8s_return_hello_auth
$ mkdir tests

## テスト用設定ファイル作成
$ cd ~/onpre_k8s_return_hello_auth
$ vi tests/conftest.py

## テスト用プログラム作成
$ cd ~/onpre_k8s_return_hello_auth
$ vi tests/test_main.py

## パッケージリスト作成
$ cd ~/onpre_k8s_return_hello_auth
$ vi requirements.txt

## 開発コンテナのディレクトリ作成
$ cd ~/onpre_k8s_return_hello_auth
$ mkdir .devcontainer

## 開発コンテナの設定ファイル作成
$ cd ~/onpre_k8s_return_hello_auth
$ vi .devcontainer/devcontainer.json

## Kubernetes用のディレクトリ作成
$ cd ~/onpre_k8s_return_hello_auth
$ mkdir k8s

## Kubernetes用のYAML作成
$ cd ~/onpre_k8s_return_hello_auth
$ vi k8s/deployment.yaml

## Kubernetes用のYAML作成
$ cd ~/onpre_k8s_return_hello_auth
$ vi k8s/service.yaml

## VSCode用のディレクトリ作成
$ cd ~/onpre_k8s_return_hello_auth
$ mkdir .vscode

## VSCode用の設定ファイル作成
$ cd ~/onpre_k8s_return_hello_auth
$ vi .vscode/settings.json

## Github-Actions用のディレクトリ作成
$ cd ~/onpre_k8s_return_hello_auth
$ mkdir -p .github/workflows

## Github-Actions用のYAMLファイル作成
$ cd ~/onpre_k8s_return_hello_auth
$ vi .github/workflows/pull_request_ci.yaml

## Github-Actions用のYAMLファイル作成
$ cd ~/onpre_k8s_return_hello_auth
$ vi .github/workflows/main_ci.yaml

## Github-Actions用のYAMLファイル作成
$ cd ~/onpre_k8s_return_hello_auth
$ vi .github/workflows/release.yaml

## 開発イメージビルド
$ cd ~/onpre_k8s_return_hello_auth
$ docker build --no-cache -t onpre_k8s_return_hello_auth_image .

## 開発イメージからVSCode上で開発コンテナ起動
$ cd ~/onpre_k8s_return_hello_auth
$ code .

## 開発コンテナ上でテストプログラム実行
$ cd ~
$ pytest tests/test_main.py

## 開発コンテナ上でアプリ起動 ※開発コンテナ上では Dockerfile のCMDは実行されない
$ cd ~
$ uvicorn app.main:app --host 0.0.0.0 --port 8000

## 開発コンテナ上で動作確認 ※動作確認後は Ctrl + C でアプリ終了
$ cd ~
$ curl http://localhost:8000 ※ブラウザ上でhttp//localhost:8000のURLを閲覧しても可

## 別ブランチをステージング移行
$ cd ~/onpre_k8s_return_hello_auth
$ git add .

## 別ブランチをコミット
$ cd ~/onpre_k8s_return_hello_auth
$ git commit -m "feature/add-basicfiles(#1)" ※#1はIssue番号

## 別ブランチをプッシュ
$ cd ~/onpre_k8s_return_hello_auth
$ git push origin feature/add-basicfiles
```

### GithubでPR作成1
![github_readme_02](images/github_readme_02.png)

### GithubでPR作成2
![github_readme_03](images/github_readme_03.png)

### Githubでマージ1
![github_readme_04](images/github_readme_04.png)

### Githubでマージ2
![github_readme_05](images/github_readme_05.png)

### Githubの別ブランチをマージ後に削除1
![github_readme_06](images/github_readme_06.png)

### Githubの別ブランチをマージ後に削除2
![github_readme_07](images/github_readme_07.png)

### Githubからmainブランチをプル
```bash
## ブランチ確認
$ cd ~/onpre_k8s_return_hello_auth
$ git branch

## ブランチをmainブランチに戻す
$ cd ~/onpre_k8s_return_hello_auth
$ git checkout main

## Github上のmainブランチの内容をプル
$ cd ~/onpre_k8s_return_hello_auth
$ git pull origin main

## 別ブランチを削除
$ cd ~/onpre_k8s_return_hello_auth
$ git branch -d feature/add-basicfiles
```

### リリース作業
```bash
## タグ付与
$ cd ~/onpre_k8s_return_hello_auth
$ git tag vX.Y.Z

## リリース作業
$ cd ~/onpre_k8s_return_hello_auth
$ git push origin main vX.Y.Z
```

### リリース確認
```note
Dockerhubに指定タグのDockerイメージを確認
```

### Docker-Desktop上の設定確認1
![docker_desktop_setting_01](images/docker_desktop_setting_01.png)

### Docker-Desktop上の設定確認2
![docker_desktop_setting_02](images/docker_desktop_setting_02.png)

### Kubectlの準備
```bash
## kubectlバイナリのダウンロード
$ cd ~/onpre_k8s_return_hello_auth
$ curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"

## kubectlバイナリに権限付与
$ cd ~/onpre_k8s_return_hello_auth
$ sudo install -o root -g root -m 0755 kubectl /usr/local/bin/kubectl

## インストール確認
$ cd ~/onpre_k8s_return_hello_auth
$ kubectl version --client

## ダウンロードしたkubectlバイナリ削除
$ cd ~/onpre_k8s_return_hello_auth
$ rm kubectl

## 既存の設定ファイル削除
$ cd ~/.kube
$ mv config config_old

## Windows11側で起動しているDocker-Desktop上の設定ファイルへのリンク作成
$ cd ~/.kube
$ ln -s /mnt/c/Users/(Windows側のユーザー名)/.kube/config config

## コンテキスト一覧
$ cd ~/onpre_k8s_return_hello_auth
$ kubectl config get-contexts

## コンテキスト確認
$ cd ~/onpre_k8s_return_hello_auth
$ kubectl config current-context

## コンテキスト切替 ※コンテキスト切替時に実行
$ cd ~/onpre_k8s_return_hello_auth
$ kubectl config use-context (コンテキスト名)
```

### Kubernetesで動作確認 ※NodePortでアクセス
```bash
## コンテキスト一覧
$ cd ~/onpre_k8s_return_hello_auth
$ kubectl config get-contexts

## コンテキスト確認
$ cd ~/onpre_k8s_return_hello_auth
$ kubectl config current-context

## 名前空間一覧
$ cd ~/onpre_k8s_return_hello_auth
$ kubectl get namespaces

## 名前空間作成
$ cd ~/onpre_k8s_return_hello_auth
$ kubectl create namespace user-apps

## Deploymentリソース差分確認
$ cd ~/onpre_k8s_return_hello_auth
$ kubectl diff -n user-apps -f k8s/deployment.yaml

## Deploymentリソース作成または更新
$ cd ~/onpre_k8s_return_hello_auth
$ kubectl apply -n user-apps -f k8s/deployment.yaml

## Deploymentリソース確認
$ cd ~/onpre_k8s_return_hello_auth
$ kubectl get deployments -n user-apps

## Serviceリソース差分確認
$ cd ~/onpre_k8s_return_hello_auth
$ kubectl diff -n user-apps -f k8s/service.yaml

## Serviceリソース作成または更新
$ cd ~/onpre_k8s_return_hello_auth
$ kubectl apply -n user-apps -f k8s/service.yaml

## Serviceリソース確認
$ cd ~/onpre_k8s_return_hello_auth
$ kubectl get service -n user-apps

## Serviceにリクエスト送信
$ cd ~/onpre_k8s_return_hello_auth
$ curl http://localhost:30080
```

### NodePortからIngressに移行 ※URLでアクセス
```bash
## コンテキスト一覧
$ cd ~/onpre_k8s_return_hello_auth
$ kubectl config get-contexts

## コンテキスト確認
$ cd ~/onpre_k8s_return_hello_auth
$ kubectl config current-context

## Ingress-Controller導入
$ cd ~/onpre_k8s_return_hello_auth
$ kubectl apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/main/deploy/static/provider/cloud/deploy.yaml

## Ingress-ControllerのPod確認
$ cd ~/onpre_k8s_return_hello_auth
$ kubectl get pods -n ingress-nginx

## Ingress-ControllerのService確認
$ cd ~/onpre_k8s_return_hello_auth
$ kubectl get service -n ingress-nginx

## ServiceのYAML追加
$ cd ~/onpre_k8s_return_hello_auth
$ vi k8s/service2.yaml

## IngressのYAML追加
$ cd ~/onpre_k8s_return_hello_auth
$ vi k8s/ingress.yaml

## 古いService削除
$ cd ~/onpre_k8s_return_hello_auth
$ kubectl delete -n user-apps -f k8s/service.yaml

## 新しいService作成
$ cd ~/onpre_k8s_return_hello_auth
$ kubectl apply -n user-apps -f k8s/service2.yaml

## Ingress作成
$ cd ~/onpre_k8s_return_hello_auth
$ kubectl apply -n user-apps -f k8s/ingress.yaml

## Windows側のhostsファイル修正
$ cd C:\Windows\System32\drivers\etc
$ vi hosts ※127.0.0.1 araki.comを追記

## URLでアクセス可能を確認
$ cd ~/onpre_k8s_return_hello_auth
$ curl http://araki.com
```
