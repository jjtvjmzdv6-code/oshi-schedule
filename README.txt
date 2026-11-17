ゆめかわ推し活カレンダー 自動更新版

GitHubの既存リポジトリに、このZIP内のファイルをアップロードして既存ファイルは置き換えてください。
追加ファイル:
- .github/workflows/update-schedules.yml
- scripts/fetch_schedules.py
- schedules.json

GitHubのActionsタブで「Update idol schedules」を選び、「Run workflow」を1回押すと初回取得します。
以後は毎日12:00（日本時間）ごろ自動実行されます。
GitHub Pagesは既存設定のままでOKです。

注意:
公式の公開スケジュールページを取得対象にしています。サイト側の変更、会員限定情報、SNSのみの告知などは取得できないことがあります。取得内容は必ず公式リンクで確認してください。
