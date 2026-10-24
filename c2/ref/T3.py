import re
K = r'(?:password|token|api_key|secret)'
def mask_secrets(text):
    text = re.sub(r'("'+K+r'"\s*:\s*")((?:[^"\\]|\\.)*)(")', r'\1***\3', text, flags=re.I)
    return re.sub(r'(?<![\w"])('+K+r')(\s*[=:]\s*)(?!")(\S+)', r'\1\2***', text, flags=re.I)
