while true; do
    cargo watch -x run
    if [ $? -ne 0 ]; then
        echo "サーバースクリプトがエラーで終了しました。再起動します..."
    fi
    sleep 2
done
