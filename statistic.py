import datetime

import actions
import matplotlib.pyplot as plt
from typing import NamedTuple


class TimeDelta(NamedTuple):
    action_name: str
    percent: float


class TimeDeltaPerDay(NamedTuple):
    """Можно в этом месте еще добавить оператор типа итератор __next__"""
    actions_names: list[str]
    percents: list[float]

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


def get_times_delta_for_date(date: datetime.date = datetime.date(2022, 8, 31)) -> TimeDeltaPerDay:
    time_delta_per_day = TimeDeltaPerDay([], [])
    t1 = actions.get_actions_by_date(date)
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


def accumulate_same_actions(time_delta_per_day: TimeDeltaPerDay) -> TimeDeltaPerDay:
    a = list(set(time_delta_per_day.actions_names))
    b = []
    for i in range(len(a)):
        sum = 0
        for j in range(len(time_delta_per_day)):
            if a[i] == time_delta_per_day.actions_names[j]:
               sum+=time_delta_per_day.percents[j]
        b.append(sum)
    return TimeDeltaPerDay(a, b)

def apply_filters(times_delta: TimeDeltaPerDay):
    times_delta2 = times_delta
    for i in range(len(times_delta)):
        print(times_delta[i])
        if times_delta[i].percent < 0.5:
            times_delta2.percents = [times_delta.percents[:i] + times_delta.percents[i:]]
    for i in range(len(times_delta2)):
        print(times_delta2[i])





def draw_plot(time_delta_per_day: TimeDeltaPerDay):
    # makeitastring = ''.join(map(str, labels))
    # colors = ['yellowgreen', 'lightgreen', 'darkgreen', 'gold', 'red', 'lightsalmon', 'darkred']
    plt.pie(time_delta_per_day.percents, labels=time_delta_per_day.actions_names, autopct='%1.1f%%', shadow=True,
            startangle=90)  # line 240
    # plt.pie(sizes, labels, colors)
    # plt.axis('equal')
    # plt.legend()
    # plt.show()
    plt.savefig('testplot.png')


 #   plt.savefig('testplot.png')

if __name__ == "__main__":
    times_delta = accumulate_same_actions(get_times_delta_for_date())
    #draw_plot(times_delta)
    apply_filters(times_delta)