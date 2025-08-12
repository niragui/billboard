from typing import Optional

import requests

import datetime

from .exceptions import ConnectionError, DateError
from .filters import POSITIONS_FILTER, TITLES_FILTER, CREDITS_FILTER
from .filters import EXTRAS_FILTER, IMAGES_FILTER, CARDS_FILTER, DATE_FILTER
from .filters import MEANINGUL_DATES_FILTER, MEANINGUL_POSITIONS_FILTER
from .filters import NodeFilter

from ..constants import CHARTS_FILE

from ..records.chart_item import ChartItem
from ..chart_data.chart_index import ChartsIndex

import os
import sys

THIS_FOLDER = os.path.dirname(__file__)
AUTOMATIONS_FOLDER = os.path.dirname(os.path.dirname(os.path.dirname(THIS_FOLDER)))

sys.path.append(AUTOMATIONS_FOLDER)

from BeautifulSoup.src.parser import MySoup, Tag


def read_date_from_node(node: Tag):
    """
    Subtract the date in isoformat from the date node

    Parameters:
        - node: Node with the date data
    """
    date_text = node.text.strip()

    date_item = datetime.datetime.strptime(date_text, "%m/%d/%y").date()

    return date_item


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
            raise ConnectionError(f"Could Not Connect To The Base Website [URL: {url} | Reason: {chart_response.reason}]")

        return chart_response.content.decode("utf-8")

    def get_soup(self):
        """
        Gets the soup item of the chart
        """
        html = self.get_html()

        with open("chart.html", "w") as f:
            f.write(html)

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

        if len(debuts_pos_found) == 1:
            return []

        debuts_nodes = []


        for i, element in enumerate(debuts_pos_found):
            if i % 2 == 1:
                continue
            debuts_nodes.append(element)

        return debuts_nodes

    def get_chart_date(self):
        """
        Returns the date as presented in the chart
        """
        soup = self.get_soup()

        date_node = soup.find(DATE_FILTER)
        if date_node is None:
            raise DateError(f"Chart Date Not Found For {self.chart.get_url(self.date)}")

        chart_date = datetime.date.fromisoformat(date_node.attrs["data-date"])

        return chart_date

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

            position = int(positions_found.text)
            title = titles_found.text.strip()
            image_url = images_found[0].attrs["src"]
            last_week = extras_found[0].text.strip()
            peak = int(extras_found[1].text)
            weeks = int(extras_found[2].text)

            if len(meaningful_dates) > 0:
                debut_date = read_date_from_node(meaningful_dates[0])
                if debut_date > chart_date:
                    debut_year = debut_date.year % 1000
                    debut_century = chart_date.year // 100
                    new_year = debut_century * 100 + debut_year
                    debut_date = debut_date.replace(year=new_year)

                if len(debuts_nodes) == 0:
                    debut_position = None
                else:
                    debut_position = int(debuts_nodes[0].text)
            elif weeks == 1:
                debut_date = chart_date
                debut_position = position

            if len(meaningful_dates) > 1:
                peak_date = read_date_from_node(meaningful_dates[1])
            elif weeks == 1:
                peak_date = chart_date
            else:
                peak_date = None

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
                debut_date=debut_date.isoformat(),
                debut_position=debut_position,
                peak_date=peak_date.isoformat(),
                date=chart_date,
                credits=credits
            )

            items.append(chart_item)

        return items

    def __repr__(self) -> str:
        return f"BillboardChartWebsite(Chart: {self.chart.name} | Date: {self.date})"

    def __str__(self) -> str:
        return f"BillboardChartWebsite(Chart: {self.chart.name} | Date: {self.date})"