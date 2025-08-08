from typing import Optional

import json

import os

from .chart_data import ChartData

CHARTS_FOLDER = os.path.dirname(__file__)
SRC_FOLDER = os.path.dirname(CHARTS_FOLDER)
PACKAGE_FOLDER = os.path.dirname(SRC_FOLDER)
DATA_FOLDER = os.path.join(PACKAGE_FOLDER, "data")


ABBREVIATION_FIELD = "abbreviation"
NAME_FIELD = "name"
LINK_FIELD = "url"


class ChartsIndex():
    def __init__(self,
                 file: str):
        if not os.path.isfile(file):
            raise OSError(f"Charts File Doesn't Exist")

        self.file = file
        with open(file) as f:
            charts_data = json.load(f)

        self.charts = []
        for chart in charts_data:
            abbreviation = chart[ABBREVIATION_FIELD]
            name = chart[NAME_FIELD]
            link = chart.get(LINK_FIELD, None)

            chart = ChartData(abbreviation, name, link)
            self.charts.append(chart)

        self.charts_by_abbr = {}
        self.charts_by_name = {}
        self.charts_by_link = {}

        for i, chart in enumerate(self.charts):
            self.charts_by_abbr[chart.abbreviation] = i
            self.charts_by_name[chart.name.upper()] = i
            if chart.link:
                self.charts_by_link[chart.link.upper()] = i

    def get_chart(self,
                  key: str):
        """
        Returns a chart given by the asked key.

        Parameters:
            - key: String identifying the chart
        """
        position = None

        if not isinstance(key, str):
            raise TypeError(f"Key For Chart Index Must Be A String [{type(key)}]")

        key = key.upper()
        if key in self.charts_by_abbr:
            position = self.charts_by_abbr[key]
        elif key in self.charts_by_name:
            position = self.charts_by_name[key]
        elif key in self.charts_by_link:
            position = self.charts_by_link[key]
        else:
            raise KeyError(f"{key} Key Couldn't Be Found")

        return self.charts[position]

    def __getitem__(self,
                    key: str):
        return self.get_chart(key)

    def __len__(self):
        return len(self.charts)

    def __repr__(self):
        return f"ChartsIndex(file={self.file} | Items: {len(self.charts)})"

    def __str__(self):
        return f"ChartsIndex(file={self.file} | Items: {len(self.charts)})"
