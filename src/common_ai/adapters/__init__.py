from common_ai.adapters.base import BaseAdapter


def get_adapter(tool: str) -> BaseAdapter:
    if tool == "kiro":
        from common_ai.adapters.kiro import KiroAdapter
        return KiroAdapter()
    elif tool == "claude":
        from common_ai.adapters.claude_code import ClaudeAdapter
        return ClaudeAdapter()
    elif tool == "gemini":
        from common_ai.adapters.gemini import GeminiAdapter
        return GeminiAdapter()
    raise ValueError(f"Unknown tool: {tool}")
