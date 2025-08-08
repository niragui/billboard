from typing import Optional

import datetime

from ..constants import BILLBOARD_URL


class ChartData():
    def __init__(self,
                 abbreviation: str,
                 name: str,
                 link: Optional[str] = None) -> None:
        self.abbreviation = abbreviation.upper()
        self.name = name
        self.link = link

    def get_url(self,
                date: Optional[datetime.date] = None):
        """
        Returns the URL of the asked chart.

        Parameters:
            - date: Date to get the url for. If None, the url returned
                will be the url of the last chart
        """
        base_url = f"{BILLBOARD_URL}/charts/{self.link}"

        if date is None:
            return base_url

        date_url = f"{base_url}/{date}"
        return date_url

    @property
    def url(self):
        """
        Returns the chart curren url
        """
        return self.get_url()

    def __repr__(self):
        return f"BillboardChart(Name: {self.name} | URL: {self.url})"

    def __str__(self):
        return f"BillboardChart(Name: {self.name} | URL: {self.url})"
