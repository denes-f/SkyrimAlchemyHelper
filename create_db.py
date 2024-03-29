from scraper import *
from config import *


class CreateDBPipeline(BasePipeline):
    STEPS = [
        GetHtml(URL),
        ParseHtml(),
        ExtractHTML('table[class*=highlight]'),
        BundleHTML(),
        ParseTable(),
        UpdateDfWithKey(),
        Union(),
        DfToSQLite('skyrim_aclhemy.db', 'ingredients')
    ]


if __name__ == '__main__':
    CreateDBPipeline()
