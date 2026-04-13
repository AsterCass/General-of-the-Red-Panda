def clean_output(text: str) -> str:
    prefixes = ["AI:", "Assistant:", "助手:", "AI：", "Assistant："]
    for p in prefixes:
        if text.strip().startswith(p):
            return text.strip()[len(p):].strip()
    return text
