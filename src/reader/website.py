from typing import Optional

import requests

import datetime

from .exceptions import ConnectionError
from .filters import POSITIONS_FILTER, TITLES_FILTER, CREDITS_FILTER
from .filters import EXTRAS_FILTER, IMAGES_FILTER, CARDS_FILTER, DATE_FILTER
from .filters import MEANINGUL_DATES_FILTER, MEANINGUL_POSITIONS_FILTER

from ..constants import CHARTS_FILE

from ..records.chart_item import ChartItem
from ..chart_data.chart_index import ChartsIndex

import os
import sys

THIS_FOLDER = os.path.dirname(__file__)
AUTOMATIONS_FOLDER = os.path.dirname(os.path.dirname(os.path.dirname(THIS_FOLDER)))

sys.path.append(AUTOMATIONS_FOLDER)

from BeautifulSoup.src.parser import MySoup, Tag


class BillboardChartWebsite():
    def __init__(self,
                 chart: str,
                 date: Optional[datetime.date] = None,
                 yearly: bool = False) -> None:
        index = ChartsIndex(CHARTS_FILE)

        self.chart = index[chart]
        self.date = date
        self.yearly = yearly

    def get_html(self):
        """
        Requests the Billboard website for the html code of the chart
        """
        url = self.chart.get_url(self.date)

        chart_response = requests.get(url)
        if chart_response.status_code // 100 != 2:
            raise ConnectionError(f"Could Not Connect To The Base Website [{chart_response.reason}]")

        return chart_response.content.decode("utf-8")

    def get_soup(self):
        """
        Gets the soup item of the chart
        """
        html = self.get_html()

        return MySoup(html)

    def get_images(self,
                   soup: Tag):
        """
        Retrives the images nodes from the chart soup.

        Parameters:
            - soup: Chart soup to read
        """
        images_found = soup.find_all(IMAGES_FILTER)

        images_nodes = []

        for i, element in enumerate(images_found, 1):
            image_tag = element.children[0].children[0]
            images_nodes.append(image_tag)

        return images_nodes

    def get_extra_values(self,
                         soup: Tag):
        """
        Retrives the extra values (woc, last week & peaks) nodes from
        the chart soup.

        Parameters:
            - soup: Chart soup to read
        """
        extra_nodes = soup.find_all(EXTRAS_FILTER)

        final_nodes = []
        for i, node in enumerate(extra_nodes):
            if i % 6 < 3:
                final_nodes.append(node)

        return final_nodes

    def get_debut_positions(self,
                            soup: Tag):
        """
        Retrives the debut position nodes from the chart soup.

        Parameters:
            - soup: Chart soup to read
        """
        debuts_pos_found = soup.find_all(MEANINGUL_POSITIONS_FILTER)

        debuts_nodes = []

        for i, element in enumerate(debuts_pos_found):
            if i % 2 == 1:
                continue
            debuts_nodes.append(element)

        return debuts_nodes

    def get_items(self):
        """
        Returns a dict with the entries data of the chart
        """
        soup = self.get_soup()

        items = []

        date_node = soup.find(DATE_FILTER)
        if date_node is None:
            raise KeyError(f"Chart Date Not Found")

        chart_date = datetime.date.fromisoformat(date_node.attrs["data-date"])

        for node in soup.find_all(CARDS_FILTER):
            positions_found = node.find(POSITIONS_FILTER)
            titles_found = node.find(TITLES_FILTER)
            credits_found = node.find(CREDITS_FILTER)
            meaningful_dates = node.find_all(MEANINGUL_DATES_FILTER)
            images_found = self.get_images(node)
            extras_found = self.get_extra_values(node)
            debuts_nodes = self.get_debut_positions(node)

            # Extract and clean data
            position = int(positions_found.text)
            title = titles_found.text.strip()
            image_url = images_found[0].attrs["src"]
            last_week = extras_found[0].text.strip()
            peak = int(extras_found[1].text)
            weeks = int(extras_found[2].text)
            debut_date = meaningful_dates[0].attrs["href"][-10:]
            debut_position = int(debuts_nodes[0].text)
            peak_date = meaningful_dates[1].attrs["href"][-10:]

            credits = None
            if credits_found:
                raw_credits = credits_found.text.strip().replace("\\n", " ")
                credits = " ".join(raw_credits.split())
                credits = credits_found.text.strip()

            # Create ChartItem instance
            chart_item = ChartItem(
                position=position,
                title=title,
                image=image_url,
                last_week=last_week,
                peak=peak,
                weeks=weeks,
                debut_date=debut_date,
                debut_position=debut_position,
                peak_date=peak_date,
                date=chart_date,
                credits=credits
            )

            while chart_item in items:
                chart_item.update_version()

            items.append(chart_item)

        return items

    def __repr__(self) -> str:
        return f"BillboardChartWebsite(Chart: {self.chart.name} | Date: {self.date})"

    def __str__(self) -> str:
        return f"BillboardChartWebsite(Chart: {self.chart.name} | Date: {self.date})"