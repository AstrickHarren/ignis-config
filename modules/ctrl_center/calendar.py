import datetime

from gi.repository import GLib

from ignis.utils import Utils
from ignis.widgets import Widget


class Calendar(Widget.Box):
    def on_change_month(self):
        date = self.cal.get_date()
        year = date.get_year()
        month = date.get_month()
        now = datetime.datetime.now()

        if now.year == year and now.month == month:
            self.cal.mark_day(now.day)
        else:
            self.cal.unmark_day(now.day)

    def __init__(self) -> None:
        self.cal = Widget.Calendar(
            hexpand=True,
            show_day_names=True,
            show_heading=True,
        )

        day_names = ["S", "M", "T", "W", "T", "F", "S"]
        month_names = [
            "JANUARY",
            "FEBRUARY",
            "MARCH",
            "APRIL",
            "MAY",
            "JUNE",
            "JULY",
            "AUGUST",
            "SEPTEMBER",
            "OCTOBER",
            "NOVEMBER",
            "DECEMBER",
        ]

        grid = self.cal.observe_children()[1]
        days = grid.observe_children()[:7]
        for day, name in zip(days, day_names):
            day.set_text(name)
        months = self.cal.observe_children()[0].observe_children()[1]
        for month, name in zip(months, month_names):
            month.set_text(name)

        self.cal.connect("next_month", lambda x: self.on_change_month())
        self.cal.connect("next_year", lambda x: self.on_change_month())
        self.cal.connect("prev_month", lambda x: self.on_change_month())
        self.cal.connect("prev_year", lambda x: self.on_change_month())
        self.on_change_month()

        super().__init__(
            hexpand=True,
            css_classes=["round", "bg-2", "p-3"],
            child=[self.cal],
        )
