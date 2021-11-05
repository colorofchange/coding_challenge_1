def esc_ent(text: str) -> str:
    """
    Replaces htmlentities with escaped char
    >>> esc_ent('Hello &quot;World&quot;')
    'Hello \"World\"'
    
    """
    if text != None:
        text = text.replace('&quot;', '\"')

    return text