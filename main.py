import json

from src.reader.website import BillboardChartWebsite

import datetime

date = datetime.date(1958, 8, 4)
#date = None

website = BillboardChartWebsite("HSI", date)

items = website.get_items()
for item in items:
    print(item.__repr__())