import matplotlib.pyplot as plt
import os
import matplotlib.font_manager as fm
from typing import NamedTuple

FONT_FURORE = fm.FontProperties(fname="./fonts/Furore.otf")

Color = str


class ColorSchema(NamedTuple):
    colors: list[Color]

    @property
    def schema_size(self):
        return len(self.colors)


class WedgesProperties(NamedTuple):
    lw: int | None = None  # Ширина линий
    ls: str | None = None  # Стиль линий
    edgecolor: Color | None = None  # Цвет линий
    capstyle: str | None = None  # Внешний вид линий butt - квадрат, round округлый
    fill: bool | None = None  # Заливать?
    hatch: str | None = None  # Штриховка Как применить ее для отдельного сектора?
    label: str | None = None  # Будет выводиться в легенде. Где она?
    sketch_params: int | None = None  # Параметр "кривости" рисунка


class TextProperties(NamedTuple):
    color: Color | None = None
    backgroundcolor: Color | None = None
    font: str | None = None
    fontfamily: str | None = None
    fontproperties: fm.FontProperties | None = None
    fontsize: str | float | None = None


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


class PiePropertiesSimple:
    def __init__(self,
                 colors: list[Color] | None = None,
                 labeldistance: float | None = None,  # Расстояние от центра окружности до подписи. В радиусах
                 autopct: str | None = None,  # Формат подписи размера доли
                 pctdistance: float | None = None,
                 # Расстояние от центра окружности до подписи размера доли. В радиусах
                 shadow: bool | None = None,  # Тень от фигуры
                 startangle: int | None = None,  # Угол поворота
                 radius: float | None = None,
                 center: tuple[int, int] | None = None,
                 # Координаты центра диаграммы, относительно фрейма (координатной сетки)
                 frame: bool | None = None,  # Отображение рамки с координатами
                 rotatelabels: bool | None = None,  # Поворот подписей
                 wedgeprops: WedgesProperties | None = None,  # Внешний вид секторов
                 textprops: TextProperties | None = None  # Внешний вид текста
                 ):
        self.colors = colors
        self.labeldistance = labeldistance
        self.autopct = autopct
        self.pctdistance = pctdistance
        self.shadow = shadow
        self.startangle = startangle
        self.radius = radius
        self.center = center
        self.frame = frame
        self.rotatelabels = rotatelabels
        self.wedgeprops = wedgeprops
        self.textprops = textprops


colors1 = ["#fbef86",
           "#fde96d",
           "#f8d162",
           "#f2ba55",
           "#eea14d",
           "#e88c3f",
           "#e77235",
           "#c64e29",
           "#9d452a",
           "#753d2b"
           ]

yellow_orange_crayola = ColorSchema(colors=colors1)

pie_property1 = PieProperties(
    colors=yellow_orange_crayola.colors,
    labeldistance=1.1,
    pctdistance=0.8,
    shadow=False,
    startangle=90,
    radius=1.1,
    center=(0, 0),
    frame=False,
    rotatelabels=False,
    wedgeprops=WedgesProperties(
        lw=1,
        ls='--',
        edgecolor='k',
        capstyle='round'
    ),
    textprops=TextProperties(
        color="blask",
        fontproperties=FONT_FURORE,
        fontsize="large"
    )
)

pie_property2 = PiePropertiesSimple(
    colors=yellow_orange_crayola.colors,
    labeldistance=1.1,
    pctdistance=0.8,
    shadow=False,
    startangle=90,
    radius=1.1,
    center=(0, 0),
    frame=False,
    rotatelabels=False,
    wedgeprops=WedgesProperties(
        lw=1,
        ls='--',
        edgecolor='k',
        capstyle='round'
    ),
    textprops=TextProperties(
        color="blask",
        fontproperties=FONT_FURORE,
        fontsize="large"
    )
)


def draw_plot(data, labels, filename: str):
    fig = plt.figure(figsize=(10, 9))
    ax1 = plt.pie(data,
                  labels=labels,
                  labeldistance=1.1,  # Расстояние от центра окружности до подписи. В радиусах
                  # autopct='%1.1f%%',  # Формат подписи размера доли
                  pctdistance=0.8,  # Расстояние от центра окружности до подписи размера доли. В радиусах
                  shadow=False,
                  startangle=90,
                  colors=colors1,
                  radius=1.1,

                  wedgeprops={'lw': 1,  # Ширина линий
                              'ls': '-',  # Стиль линий
                              'edgecolor': "#402e2b",  # Цвет линий
                              "capstyle": "round",  # Внешний вид линий butt - квадрат, round округлый
                              'fill': True,  # Заливать?
                              'hatch': "",  # Штриховка Как применить ее для отдельного сектора?
                              'label': "123",  # Будет выводиться в легенде. Где она?
                              'sketch_params': 0  # Параметр "кривости" рисунка
                              },  # Внешний вид секторов
                  textprops={'color': "black",
                             # 'backgroundcolor': "white",
                             # 'font': "Gora Free",
                             # 'fontfamily': 'Gora Free',
                             'fontproperties': FONT_FURORE,
                             'fontsize': 'large'  # Или размер float
                             },  # Внешний вид текста
                  center=(0, 0),  # Координаты центра диаграммы, относительно фрейма (координатной сетки)
                  frame=False,  # Отображение рамки с координатами
                  rotatelabels=False  # Поворот подписей
                  )  # line 240
    plt.savefig(filename)
    fig.clear()
    plt.close(fig)


if __name__ == "__main__":
    #print(pie_property2.__dict__)

    filename = f"testplot1.png"
    test_data = [1, 20, 3, 40, 5, 6, 7, 8, 9, 10][::-1]
    test_labels = ["Короче текст 1 но чуть по длиннее ", "Короче текст 2\n но с переносом строки", 3, 4, 5, 6, "Короче текст 7 \nочень сука длинный\n фыждвлаофолыиазшгйукилуфокипм", 8, 9, 10][::-1]
    draw_plot(test_data, test_labels, filename)
    os.system(f"xdg-open {filename}")
