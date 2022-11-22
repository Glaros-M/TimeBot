import matplotlib.pyplot as plt
import os
import matplotlib.font_manager as fm
from typing import NamedTuple

FONT_FURORE = fm.FontProperties(fname="./fonts/Furore.otf")

Color = str


class ColorSchema(NamedTuple):
    colors: list[Color]
    comment: str

    # text_color: Color = "black"

    @property
    def schema_size(self):
        return len(self.colors)


class WedgesProperties(NamedTuple):
    lw: int | None = None  # Ширина линий
    ls: str | None = None  # Стиль линий
    edgecolor: Color | None = "black"  # Цвет линий
    capstyle: str | None = None  # Внешний вид линий butt - квадрат, round округлый
    fill: bool | None = True  # Заливать?
    hatch: str | None = None  # Штриховка Как применить ее для отдельного сектора?
    label: str | None = None  # Будет выводиться в легенде. Где она?
    sketch_params: int | None = None  # Параметр "кривости" рисунка

    def dict(self):
        return self._asdict()

    def __repr__(self):
        return str(self.dict())


class TextProperties(NamedTuple):
    color: Color | None = None
    backgroundcolor: Color | None = "0001"
    fontfamily: str | None = None
    fontproperties: fm.FontProperties | None = None
    fontsize: str | float | None = None

    def dict(self):
        return self._asdict()

    def __repr__(self):
        return str(self.dict())


class PieProperties(NamedTuple):
    colors: list[Color] | None = None
    labeldistance: float | None = None  # Расстояние от центра окружности до подписи. В радиусах
    autopct: str | None = None  # Формат подписи размера доли
    pctdistance: float | None = None  # Расстояние от центра окружности до подписи размера доли. В радиусах
    shadow: bool | None = None  # Тень от фигуры
    startangle: int | None = None  # Угол поворота
    radius: float | None = None
    center: tuple[int, int] | None = None  # Координаты центра диаграммы, относительно фрейма (координатной сетки)
    frame: bool | None = None  # Отображение рамки с координатами
    rotatelabels: bool | None = None  # Поворот подписей
    wedgeprops: WedgesProperties | None = None  # Внешний вид секторов
    textprops: TextProperties | None = None  # Внешний вид текста

    def dict(self):
        d = {**self._asdict()}
        d.update({'wedgeprops': self.wedgeprops.dict()})
        d.update({'textprops': self.textprops.dict()})
        return d

    def __repr__(self):
        return str(self.dict())


yellow_orange_crayola = ColorSchema(colors=["#fbef86",
                                            "#fde96d",
                                            "#f8d162",
                                            "#f2ba55",
                                            "#eea14d",
                                            "#e88c3f",
                                            "#e77235",
                                            "#c64e29",
                                            "#9d452a",
                                            "#753d2b"
                                            ],
                                    comment="""color gradient from 
                                            https://medium.com/%D1%86%D0%B2%D0%B5%D1%82/%D0%BF%D0%BE%D0%B4%D0%B1%D0%
                                            BE%D1%80-%D0%BF%D1%80%D0%B0%D0%B2%D0%B8%D0%BB%D1%8C%D0%BD%D1%8B%D1%85-%D1%
                                            86%D0%B2%D0%B5%D1%82%D0%BE%D0%B2%D1%8B%D1%85-%D0%BF%D0%B0%D0%BB%D0%B8%D1%
                                            82%D1%80-%D0%B4%D0%BB%D1%8F-%D0%B2%D0%B8%D0%B7%D1%83%D0%B0%D0%BB%D0%B8%D0%
                                            B7%D0%B0%D1%86%D0%B8%D0%B8-%D0%B4%D0%B0%D0%BD%D0%BD%D1%8B%D1%85
                                            -323735a4ceb2"""
                                    )

wedgeprops1 = WedgesProperties(
    lw=1,
    ls='-',
    edgecolor="#402e2b",
    capstyle="round",
    fill=True,
    hatch="",
    label="123",
    sketch_params=0
)

textprops1 = TextProperties(
    color="black",
    fontproperties=FONT_FURORE,
    fontsize="large",
    backgroundcolor="0001"
)

yellow_orange_crayola_pie = PieProperties(
    labeldistance=1.1,
    pctdistance=0.8,
    shadow=False,
    startangle=90,
    radius=1.1,
    center=(0, 0),
    frame=False,
    rotatelabels=False,
    wedgeprops=wedgeprops1,
    textprops=textprops1,
    colors=yellow_orange_crayola.colors,
)


if __name__ == "__main__":

    def draw_plot2(data, labels, filename: str):
        fig = plt.figure(figsize=(10, 9))
        ax1 = plt.pie(data,
                      labels=labels,
                      **yellow_orange_crayola_pie.dict(),
                      )  # line 240
        plt.savefig(filename)
        fig.clear()
        plt.close(fig)


    print(yellow_orange_crayola_pie.dict())
    filename = f"testplot1.png"
    test_data = [1, 20, 3, 40, 5, 6, 7, 8, 9, 10][::-1]
    test_labels = ["Короче текст 1 но чуть по длиннее ", "Короче текст 2\n но с переносом строки", 3, 4, 5, 6,
                   "Короче текст 7 \nочень сука длинный\n фыждвлаофолыиазшгйукилуфокипм", 8, 9, 10][::-1]
    draw_plot2(test_data, test_labels, filename)
    os.system(f"xdg-open {filename}")
