"""モデル定義とプリセット設定"""

MODEL_PRESETS = {
    "GPT-4": {
        "model": "gpt-4",
        "max_tokens": 2000,
        "temperature": 0.7
    },
    "Claude 2": {
        "model": "claude-2",
        "max_tokens": 1500,
        "temperature": 0.8
    },
    "GPT-3.5 Turbo": {
        "model": "gpt-3.5-turbo",
        "max_tokens": 1000,
        "temperature": 1.0
    }
}

def load_preset(preset_name: str) -> tuple[str, int, float]:
    """プリセットの設定を読み込む"""
    preset = MODEL_PRESETS.get(preset_name, MODEL_PRESETS["GPT-3.5 Turbo"])
    return preset["model"], preset["max_tokens"], preset["temperature"]
