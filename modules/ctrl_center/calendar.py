import datetime

from gi.repository import GLib

from ignis.utils import Utils
from ignis.variable import Variable
from ignis.widgets import Widget


class Calendar(Widget.Box):
    def on_change_page(self):
        date = self.cal.get_date()
        year = date.get_year()
        month = date.get_month()
        now = datetime.datetime.now()

        if now.year == year and now.month == month:
            self.cal.mark_day(now.day)
            self.back_to_today_visible.value = False
        else:
            self.cal.unmark_day(now.day)
            self.back_to_today_visible.value = True

    def __init__(self) -> None:
        self.cal = Widget.Calendar(
            hexpand=True,
            show_day_names=True,
            show_heading=True,
        )
        self.back_to_today_visible = Variable(False)

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

        self.cal.connect("next_month", lambda x: self.on_change_page())
        self.cal.connect("next_year", lambda x: self.on_change_page())
        self.cal.connect("prev_month", lambda x: self.on_change_page())
        self.cal.connect("prev_year", lambda x: self.on_change_page())
        self.on_change_page()

        back_to_today_btn = Widget.Button(
            halign="end",
            css_classes=[
                "mt-5",
                "txt-red",
                "hover:bg-3",
                "p-2",
                "round",
                "transition-all",
            ],
            on_click=lambda _: back_to_today(),
            child=Widget.Label(label="Today"),
        )

        def back_to_today():
            self.cal.select_day(GLib.DateTime.new_now_local())
            self.on_change_page()

        super().__init__(
            hexpand=True,
            vertical=True,
            child=[
                Widget.Box(
                    css_classes=["round", "bg-2", "p-3"],
                    child=[
                        self.cal,
                    ],
                ),
                Widget.Revealer(
                    child=back_to_today_btn,
                    transition_type="crossfade",
                    reveal_child=self.back_to_today_visible.bind("value"),
                ),
            ],
        )
