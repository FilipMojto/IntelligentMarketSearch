
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
    ProgressReportPoints.FINISHING_POINT : "finished!"
}