import dataclasses as dc

@dc.dataclass
class Item():
    idx: int
    value: int
    weight: int
    density: float = dc.field(init=False)

    def __post_init__(self):
        self.density = round(self.value / self.weight, 4)
