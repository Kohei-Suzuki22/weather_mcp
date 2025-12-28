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

## 処理の流れ (What's happening under the hood)

Claude for Desktopでの質問から回答までの流れ：

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│  Claude Desktop │     │   MCP Server    │     │  External API   │
│    (Client)     │     │   (weather)     │     │  (weather.gov)  │
└────────┬────────┘     └────────┬────────┘     └────────┬────────┘
         │                       │                       │
         │  1. ユーザーが質問     │                       │
         │  「サクラメントの天気は？」                      │
         │                       │                       │
         │  2. Claudeが利用可能な │                       │
         │     ツールを分析       │                       │
         │                       │                       │
         │  3. ツール実行リクエスト│                       │
         │  (JSON-RPC over STDIO)│                       │
         │──────────────────────>│                       │
         │                       │  4. 外部API呼び出し    │
         │                       │──────────────────────>│
         │                       │                       │
         │                       │  5. APIレスポンス      │
         │                       │<──────────────────────│
         │  6. ツール実行結果     │                       │
         │<──────────────────────│                       │
         │                       │                       │
         │  7. Claudeが結果を解釈 │                       │
         │     して自然言語で回答 │                       │
         │                       │                       │
```

### ポイント

- **自動起動**: Claude Desktopが設定に基づいてMCPサーバープロセスを起動・管理
- **ツール検出**: クライアントがサーバーの `tools/list` を呼び出して利用可能なツールを取得
- **STDIO通信**: 標準入出力を介してJSON-RPCメッセージをやり取り
- **非同期実行**: API呼び出しなどのI/O操作を効率的に処理

## 注意事項

- STDIOベースのサーバーでは `print()` を使用しないこと（JSON-RPCメッセージが破損する）
- ログ出力には `logging` モジュールを使用する
