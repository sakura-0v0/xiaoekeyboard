"""
特殊按键的映射表
"""
OTHER_KEY_MAP = {
    "À": "~",
    "Ü": "\\",
    "½": "-",
    "»": "=",
    "Û": "[",
    "Ý": "]",
    "º": ";",
    "Þ": "'",
    "¼": ",",
    "¾": ".",
    "¿": "/",
    "o": "num_/",
    "j": "num_*",
    "m": "num_-",
    "k": "num_+",
    "a": "num_1",
    "b": "num_2",
    "c": "num_3",
    "d": "num_4",
    "e": "num_5",
    "f": "num_6",
    "g": "num_7",
    "h": "num_8",
    "i": "num_9",
    "`": "num_0",
    "n": "num_.",
}


OTHER_KEY_MAP_reserve = {
    value: key for key, value in OTHER_KEY_MAP.items()
}