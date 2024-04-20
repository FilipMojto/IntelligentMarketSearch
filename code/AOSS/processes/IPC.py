
from dataclasses import dataclass
from typing import List

GUI_TERMINATION_SIGNAL = 1

class ProgressReportPoints:

    TRAINING_MARKET_ANALYSIS = 100/9
    MARKETS_ANALYSIS = 200/9
    SCRAPING_MISSING_DATA = 100/3
    UPDATING_DATA = 200/3
    FINISHING_POINT = 100

PROGRESS_REPORTS = {
    ProgressReportPoints.TRAINING_MARKET_ANALYSIS : "analyzing training market...",
    ProgressReportPoints.MARKETS_ANALYSIS : "analyzing markets...",
    ProgressReportPoints.SCRAPING_MISSING_DATA: "scraping missing data...",
    ProgressReportPoints.UPDATING_DATA : "updating data...",
    ProgressReportPoints.FINISHING_POINT : "finishing..."
}


@dataclass
class ScrapeRequest:
    ID: int
    market_ID: int
    categories: List[int]

class ScrapeRequestGenerator:
    
    def __init__(self):
        self.ID = 1

    def get_request_ID(self):
        old_ID = self.ID
        self.ID += 1
        return old_ID





# SIGNALS FOR IPC BETWEEN DPMP AND GUI process, for regulation of batch updates

UPDATE_INTERVAL_SIGNAL = 3
UPDATE_STOP_SIGNAL = -1

UPDATE_PRODUCTS_SIGNAL = 1
PROGRESS_BAR_SIGNAL = 2