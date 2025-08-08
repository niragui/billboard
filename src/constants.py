import os

SRC_FOLDER = os.path.dirname(__file__)
PACKAGE_FOLDER = os.path.dirname(SRC_FOLDER)
DATA_FOLDER = os.path.join(PACKAGE_FOLDER, "data")

CHARTS_FILE = os.path.join(DATA_FOLDER, "charts.json")

BILLBOARD_URL = "https://www.billboard.com"