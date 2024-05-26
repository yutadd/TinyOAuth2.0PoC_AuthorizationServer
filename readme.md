# OAuth2.0 Authorization Server PoC
## Usage
```python
cd <top of this repository>
python3 ./main.py
```
で認可サーバーを起動できます。
起動完了後、クライアントからこのようなパラメータを送信することで認証＆認可画面が表示されます。
http://localhost:8080/authorize?client_id=1&response_type=code&state=xyz&scope=read&redirect_uri=http://localhost/callback
認証＆認可画面で正しく認証情報を入れ、`認可する`ボタンを押すと認証が行われ、クライアントのredirect_uriにリダイレクトされます。
