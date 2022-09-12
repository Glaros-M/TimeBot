import datetime
import os
import actions
import matplotlib.pyplot as plt
from typing import NamedTuple
from aiogram import types


class TimeDelta(NamedTuple):
    action_name: str
    percent: float


class TimeDeltaPerDay(NamedTuple):
    """Можно в этом месте еще добавить оператор типа итератор __next__"""
    actions_names: list[str] = []
    percents: list[float] = []

    def __len__(self):
        if len(self.actions_names) == len(self.percents):
            return len(self.actions_names)
        else:
            raise Exception("Wrong data in object: length of arrays not equal")

    def __getitem__(self, item):
        return TimeDelta(self.actions_names[item], self.percents[item])

    def __setitem__(self, key, value: TimeDelta):
        self.actions_names[key] = value.action_name
        self.percents[key] = value.percent

    def append(self, value: TimeDelta):
        self.actions_names.append(value.action_name)
        self.percents.append(value.percent)


def get_times_delta_for_date(user_id: int, date: datetime.date = datetime.date(2022, 8, 31)) -> TimeDeltaPerDay | None:
    time_delta_per_day = TimeDeltaPerDay([], [])
    t1 = actions.get_actions_by_date(date, user_id)
    if len(t1) > 1:
        deltas = []
        all_delta = datetime.timedelta(0)
        for i in range(1, len(t1)):
            deltas.append(t1[i].create_datetime - t1[i - 1].create_datetime)
            all_delta += t1[i].create_datetime - t1[i - 1].create_datetime
        deltas.append(datetime.timedelta(0))

        for i in range(len(t1)):
            time_delta_per_day.actions_names.append(t1[i].name)
            time_delta_per_day.percents.append(deltas[i]/all_delta*100)
        return time_delta_per_day
    return None

def accumulate_same_actions(time_delta_per_day: TimeDeltaPerDay) -> TimeDeltaPerDay:
    a = list(set(time_delta_per_day.actions_names))
    b = []
    for i in range(len(a)):
        sum = 0
        for j in range(len(time_delta_per_day)):
            if a[i] == time_delta_per_day.actions_names[j]:
               sum += time_delta_per_day.percents[j]
        b.append(sum)
    return TimeDeltaPerDay(a, b)


def apply_filters(times_delta: TimeDeltaPerDay) -> TimeDeltaPerDay:

    times_delta_per_day = TimeDeltaPerDay([], [])
    # По какой то причине не срабатывают значения по умолчанию при вызове конструктора TimeDeltaPerDay. Каким то
    # образом данные начинают дублироваться в этом месте
    for i in range(len(times_delta)):
        if times_delta[i].percent > 1:
            time_delta = TimeDelta(times_delta[i].action_name, times_delta[i].percent)
            times_delta_per_day.append(time_delta)
    return times_delta_per_day


def draw_plot(time_delta_per_day: TimeDeltaPerDay, filename: str):
    fig = plt.figure(figsize=(10, 7))
    ax1 = plt.pie(time_delta_per_day.percents, labels=time_delta_per_day.actions_names, autopct='%1.1f%%', shadow=True,
            startangle=90)  # line 240
    #plt.legend(loc='lower right') #, bbox_to_anchor=(1.0, 1.0))
    plt.savefig(filename)
    fig.clear()
    plt.close(fig)
    #ax1.savefig(filename)
    # 'left' is not a valid value for loc; supported values are 'best', 'upper right', 'upper left', 'lower left', 'lower right', 'right', 'center left', 'center right', 'lower center', 'upper center', 'center'


def get_today_statistic(user_id: int):
    times_delta = get_times_delta_for_date(user_id, datetime.date.today())
    if times_delta:
        times_delta = accumulate_same_actions(times_delta)
        times_delta = apply_filters(times_delta)
        filename = f"images/{datetime.date.today()}-{user_id}.png"
        draw_plot(times_delta, filename)
        return filename
    return None

if __name__ == "__main__":
    pass