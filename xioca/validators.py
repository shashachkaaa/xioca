# 📦 Xioca UserBot
# 👤 Copyright (C) 2025 shashachkaaa
#
# ⚖️ Licensed under GNU AGPL v3.0
# 🌐 Source: https://github.com/shashachkaaa/xioca
# 📝 Docs:   https://www.gnu.org/licenses/agpl-3.0.html

class ValidationError(ValueError):
    """Raised when a config value is invalid."""
    pass

class Validator:
    """Base validator: parse(text)->value and validate(value)->value."""
    def parse(self, text: str):
        return text

    def validate(self, value):
        return value

class Boolean(Validator):
    TRUE = {"1","true","yes","y","on","да","д","+"}
    FALSE = {"0","false","no","n","off","нет","н","-"}

    def parse(self, text: str) -> bool:
        t = (text or "").strip().lower()
        if t in self.TRUE:
            return True
        if t in self.FALSE:
            return False
        raise ValidationError("Expected boolean (true/false)")

    def validate(self, value) -> bool:
        if isinstance(value, bool):
            return value
        raise ValidationError("Expected bool")

class Integer(Validator):
    def __init__(self, min: int = None, max: int = None):
        self.min = min
        self.max = max

    def parse(self, text: str) -> int:
        try:
            v = int((text or "").strip())
        except Exception:
            raise ValidationError("Expected integer")
        return self.validate(v)

    def validate(self, value) -> int:
        if not isinstance(value, int) or isinstance(value, bool):
            raise ValidationError("Expected int")
        if self.min is not None and value < self.min:
            raise ValidationError(f"Min is {self.min}")
        if self.max is not None and value > self.max:
            raise ValidationError(f"Max is {self.max}")
        return value

class Float(Validator):
    def __init__(self, min: float = None, max: float = None):
        self.min = min
        self.max = max

    def parse(self, text: str) -> float:
        try:
            v = float((text or "").strip())
        except Exception:
            raise ValidationError("Expected float")
        return self.validate(v)

    def validate(self, value) -> float:
        if isinstance(value, bool) or not isinstance(value, (int, float)):
            raise ValidationError("Expected float")
        v = float(value)
        if self.min is not None and v < self.min:
            raise ValidationError(f"Min is {self.min}")
        if self.max is not None and v > self.max:
            raise ValidationError(f"Max is {self.max}")
        return v

class String(Validator):
    def __init__(self, min_len: int = None, max_len: int = None):
        self.min_len = min_len
        self.max_len = max_len

    def parse(self, text: str) -> str:
        return self.validate(str(text or ""))

    def validate(self, value) -> str:
        if not isinstance(value, str):
            raise ValidationError("Expected string")
        if self.min_len is not None and len(value) < self.min_len:
            raise ValidationError(f"Min length is {self.min_len}")
        if self.max_len is not None and len(value) > self.max_len:
            raise ValidationError(f"Max length is {self.max_len}")
        return value

class Choice(Validator):
    def __init__(self, *choices: str):
        self.choices = list(choices)

    def parse(self, text: str) -> str:
        return self.validate((text or "").strip())

    def validate(self, value) -> str:
        if value not in self.choices:
            raise ValidationError(f"Allowed: {', '.join(self.choices)}")
        return value

class validators:
    Boolean = Boolean
    Integer = Integer
    Float = Float
    String = String
    Choice = Choice
