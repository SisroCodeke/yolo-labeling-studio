
"""
Text utilities for handling multilingual text and text rendering
"""

ARABIC_BLOCK_START, ARABIC_BLOCK_END = 0x0600, 0x06FF


def contains_persian(text: str) -> bool:
    """Check if text contains Persian/Arabic characters"""
    return any(ARABIC_BLOCK_START <= ord(ch) <= ARABIC_BLOCK_END for ch in text)


def reverse_rtl_text(text: str) -> str:
    """Reverse RTL text for proper display if needed"""
    if contains_persian(text) and len(text) > 1:
        return text[::-1]
    return text


def get_display_text(class_name: str, class_index: int, show_index: bool = False) -> str:
    """Get formatted display text for class labels"""
    if show_index:
        return f"{class_name} [{class_index}]"
    return class_name
