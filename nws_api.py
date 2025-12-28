"""
NWS (National Weather Service) API クライアント

NWS APIとの通信およびレスポンスのフォーマットを担当する。
https://www.weather.gov/documentation/services-web-api
"""

from typing import Any

import httpx

# =============================================================================
# 定数
# =============================================================================
NWS_API_BASE = "https://api.weather.gov"  # NWS APIのベースURL
USER_AGENT = "weather-app/1.0"  # APIリクエストに必要なUser-Agent


# =============================================================================
# API通信
# =============================================================================
async def make_nws_request(url: str) -> dict[str, Any] | None:
    """NWS APIにリクエストを送信する。

    Args:
        url: リクエスト先のURL

    Returns:
        成功時はJSONレスポンス、失敗時はNone
    """
    headers = {"User-Agent": USER_AGENT, "Accept": "application/geo+json"}
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, headers=headers, timeout=30.0)
            response.raise_for_status()
            return response.json()
        except Exception:
            return None


# =============================================================================
# フォーマッター
# =============================================================================
def format_alert(feature: dict) -> str:
    """気象警報をフォーマットする。

    Args:
        feature: NWS APIから取得したalertのfeatureオブジェクト

    Returns:
        人間が読みやすい形式の文字列
    """
    props = feature["properties"]
    return f"""
Event: {props.get("event", "Unknown")}
Area: {props.get("areaDesc", "Unknown")}
Severity: {props.get("severity", "Unknown")}
Description: {props.get("description", "No description available")}
Instructions: {props.get("instruction", "No specific instructions provided")}
"""
