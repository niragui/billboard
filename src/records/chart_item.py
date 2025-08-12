from typing import Optional

import datetime

NEW_CHANGE = "NEW"
RE_ENTRY_CHANGE = "RE"
NO_CHANGE = "="

NEW_PEAK_TEXT = "NEW PEAK"
RE_PEAK_TEXT = "RE-PEAK"
PEAK_TEXT = "PEAK"

NO_IMAGE = "lazyload-fallback"


class ChartItem:
    def __init__(self,
                 position: int,
                 title: str,
                 image: str,
                 last_week: str,
                 peak: int,
                 weeks: int,
                 debut_date: str,
                 debut_position: int,
                 peak_date: str,
                 date: datetime.date,
                 credits: Optional[str] = None):
        self.position = position
        self.title = title
        if image.find(NO_IMAGE) >= 0:
            image = None
        self.image = image

        if last_week.isdigit():
            self.last_week = int(last_week)
        else:
            self.last_week = None

        self.peak = peak
        self.weeks = weeks
        self.debut_date = datetime.date.fromisoformat(debut_date)
        self.debut_position = debut_position
        self.peak_date = datetime.date.fromisoformat(peak_date)
        self.date = date
        self.credits = credits

    @property
    def item_id(self):
        """
        Returns a string that represents the chart uniquely, based on
        its debut position and debut date
        """
        return f"{self.debut_date}-{self.debut_position}"

    @property
    def is_new_peak(self):
        """
        Returns a bool indicating if the record has reached a new peak
        """
        return self.date == self.peak_date

    @property
    def is_peak(self):
        """
        Returns a bool indicating if the record is at its peak
        """
        return self.peak == self.position

    @property
    def is_new(self):
        """
        Returns a bool indicating if the song is a new entry
        """
        return self.weeks == 1

    @property
    def is_re_entry(self):
        """
        Returns a bool indicating if the song is a new entry
        """
        if self.last_week is not None:
            return False

        return not self.is_new

    @property
    def has_changed(self):
        """
        Returns a bool indicating if the record has changed
        """
        if self.last_week is None:
            return True

        return self.position != self.last_week

    @property
    def is_repeak(self):
        """
        Returns a bool indicating if the record has returned to its peak
        """
        if not self.is_peak:
            return False

        if not self.has_changed:
            return False

        if self.is_new:
            return False

        return not self.is_new_peak

    @property
    def change(self):
        """
        Return a string representing the item change
        """
        if self.is_new:
            return NEW_CHANGE

        if self.is_re_entry:
            return RE_ENTRY_CHANGE

        if not self.has_changed:
            return NO_CHANGE

        change = self.last_week - self.position
        if change > 0:
            return f"+{change}"
        else:
            return str(change)

    @property
    def peak_text(self):
        """
        Return a string representing the peak position of the item
        """
        if self.is_new_peak:
            return NEW_PEAK_TEXT

        if self.is_repeak:
            return RE_PEAK_TEXT

        if self.is_peak:
            return PEAK_TEXT

        return None

    @property
    def text(self):
        """
        Return a string representing the item position
        """
        text = f"#{self.position} ({self.change}) — {self.title}"

        if self.credits:
            text += f", {self.credits}"

        if self.is_peak and not self.is_new:
            text += f" *{self.peak_text}*"
        elif not self.is_new:
            text += f" *peak #{self.peak}*"

        return text

    def to_dict(self):
        return {
            "position": self.position,
            "title": self.title,
            "image": self.image,
            "last_week": self.last_week,
            "peak": self.peak,
            "weeks": self.weeks,
            "debut_date": self.debut_date.isoformat(),
            "debut_position": self.debut_position,
            "peak_date": self.peak_date.isoformat(),
            "date": self.date.isoformat(),
            "credits": self.credits,
        }

    def __repr__(self):
        if self.credits:
            return f"ChartItem(Title: {self.title} | Credits: {self.credits} | Position: #{self.position} | ID: {self.item_id})"
        else:
            return f"ChartItem(Title: {self.title} | Position: #{self.position} | ID: {self.item_id})"

    def __str__(self):
        return self.text

    def __eq__(self, other: "ChartItem"):
        return self.item_id == other.item_id