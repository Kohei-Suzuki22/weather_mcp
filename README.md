# Weather MCP Server

Model Context Protocol (MCP) サーバーの実装プロジェクトです。天気情報を提供するツールを実装します。

## 参考ドキュメント

- [Building MCP Servers](https://modelcontextprotocol.io/docs/develop/build-server)
- [公式サンプルコード](https://github.com/modelcontextprotocol/quickstart-resources/tree/main/weather-server-python)

## システム要件

- Python 3.10以上
- uv (Pythonパッケージマネージャー)

## セットアップ

```bash
# 仮想環境の作成とアクティベート
uv venv
source .venv/bin/activate

# 依存関係のインストール
uv add "mcp[cli]" httpx
```

## 実行方法

```bash
uv run main.py
```

## 提供するツール

| ツール名 | 説明 |
|---------|------|
| `get_alerts` | 米国の州の気象警報を取得 |
| `get_forecast` | 緯度・経度から天気予報を取得 |

## Claude for Desktop への統合

`~/Library/Application Support/Claude/claude_desktop_config.json` を編集：

```json
{
  "mcpServers": {
    "weather": {
      "command": "uv",
      "args": [
        "--directory",
        "/ABSOLUTE/PATH/TO/weather",
        "run",
        "main.py"
      ]
    }
  }
}
```

## 注意事項

- STDIOベースのサーバーでは `print()` を使用しないこと（JSON-RPCメッセージが破損する）
- ログ出力には `logging` モジュールを使用する
