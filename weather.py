"""
Weather MCP Server

FastMCPを使用したMCPサーバーの実装例。
NWS (National Weather Service) APIを使用して、米国の天気予報と気象警報を取得する。
"""

from mcp.server.fastmcp import FastMCP

from nws_api import NWS_API_BASE, format_alert, make_nws_request

# =============================================================================
# サーバーの初期化
# =============================================================================
# FastMCPはMCPサーバーを簡単に作成するためのラッパークラス
# 引数 "weather" はサーバー名（ログやデバッグに使用される）
mcp = FastMCP("weather")


# =============================================================================
# MCPツール定義
# =============================================================================
# @mcp.tool() デコレータで関数をMCPツールとして登録する
#
# 重要なポイント:
# - 関数名がツール名になる（例: get_alerts, get_forecast）
# - 型ヒント（state: str）がクライアントに引数の型を伝える
# - docstringがツールの説明としてClaudeに渡される
#   → Claudeはこれを読んで「いつ・どう使うか」を判断する
# - 戻り値は str で返す（Claudeが解釈しやすい形式）
#
# -----------------------------------------------------------------------------
# なぜ @mcp.resource() ではなく @mcp.tool() を使うのか？
# -----------------------------------------------------------------------------
# 本質的な違いは「誰が呼び出しを決定するか」
#
# | 観点         | Resource           | Tool               |
# |--------------|--------------------|--------------------|
# | 呼び出し決定者 | ユーザー/ホストアプリ | LLM (Claude)       |
# | ユーザーの理解度 | 何が欲しいか分かっている | 抽象的な目的だけ伝える |
# | イメージ      | 「このURIを開いて」  | 「天気を調べて」    |
#
# 例:
# - Resource: ユーザーが「weather://alerts/CA」を明示的に指定
# - Tool: ユーザーは「西海岸の天気が心配」と言うだけ
#         → Claudeが「CAのalertsを取ろう」と自律的に判断
#
# 今回の天気APIは「Claudeに自分で判断して呼んでほしい」ので Tool が適切
# =============================================================================

@mcp.tool()
async def get_alerts(state: str) -> str:
    """Get weather alerts for a US state.

    Args:
        state: Two-letter US state code (e.g. CA, NY)
    """
    url = f"{NWS_API_BASE}/alerts/active/area/{state}"
    data = await make_nws_request(url)

    if not data or "features" not in data:
        return "Unable to fetch alerts or no alerts found."

    if not data["features"]:
        return "No active alerts for this state."

    alerts = [format_alert(feature) for feature in data["features"]]
    return "\n---\n".join(alerts)


@mcp.tool()
async def get_forecast(latitude: float, longitude: float) -> str:
    """Get weather forecast for a location.

    Args:
        latitude: Latitude of the location
        longitude: Longitude of the location
    """
    # First get the forecast grid endpoint
    points_url = f"{NWS_API_BASE}/points/{latitude},{longitude}"
    points_data = await make_nws_request(points_url)

    if not points_data:
        return "Unable to fetch forecast data for this location."

    # Get the forecast URL from the points response
    forecast_url = points_data["properties"]["forecast"]
    forecast_data = await make_nws_request(forecast_url)

    if not forecast_data:
        return "Unable to fetch detailed forecast."

    # Format the periods into a readable forecast

    periods = forecast_data["properties"]["periods"]
    forecasts = []
    for period in periods[:5]:  # Only show next 5 periods
        forecast = f"""
{period["name"]}:
Temperature: {period["temperature"]}°{period["temperatureUnit"]}
Wind: {period["windSpeed"]} {period["windDirection"]}
Forecast: {period["detailedForecast"]}
"""
        forecasts.append(forecast)

    return "\n---\n".join(forecasts)