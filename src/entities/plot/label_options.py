from enums.font_weight import FontWeight


class LabelOptions:
    def __init__(
            self,
            text: str = None,
            x: float = None,
            y: float = None,
            font_weight: FontWeight = FontWeight.Normal,
            rotation_angle: int = 0,
            font_size: int = 10,
            text_color: str = None):

        self._x = x
        self._y = y

        self._text = text
        self._font_weight = font_weight
        self._rotation_angle = rotation_angle
        self._font_size = font_size
        self._text_color: str = text_color

    @property
    def x(self) -> float:
        return self._x

    @property
    def y(self) -> float:
        return self._y

    @property
    def text(self) -> str:
        return self._text

    @property
    def font_weight(self) -> FontWeight:
        return self._font_weight

    @property
    def rotation_angle(self) -> int:
        return self._rotation_angle

    @property
    def font_size(self) -> int:
        return self._font_size

    @property
    def text_color(self) -> str:
        return self._text_color