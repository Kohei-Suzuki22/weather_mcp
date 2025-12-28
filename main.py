"""
MCP Server エントリーポイント

このファイルはMCPサーバーの起動を担当する。
Claude Desktopは設定ファイル(claude_desktop_config.json)に基づいて
このスクリプトを子プロセスとして起動する。
"""

from weather import mcp  # weather.pyで定義したFastMCPインスタンスをインポート


def main():
    # サーバーを起動
    # transport="stdio" は標準入出力を使用して通信することを意味する
    # - stdin: クライアント(Claude Desktop)からのJSON-RPCリクエストを受信
    # - stdout: クライアントへJSON-RPCレスポンスを送信
    #
    # 注意: print()を使うとstdoutにゴミが混じりJSON-RPCが壊れるため使用禁止
    mcp.run(transport="stdio")


if __name__ == "__main__":
    main()