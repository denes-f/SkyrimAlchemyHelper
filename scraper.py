from abc import ABC, abstractmethod
import sqlite3

import requests
from bs4 import BeautifulSoup
import pandas as pd


class BaseStep(ABC):

    def __init__(self):
        self.result = None

    @abstractmethod
    def run(self):
        """To be extended."""


class BasePipeline(ABC):
    STEPS = []

    def __init__(self):
        result = None
        for step in self.STEPS:
            step.result = result
            result = step.run()


class GetHtml:

    def __init__(self, url):
        self.url = url

    def run(self):
        return requests.get(self.url).content


class ParseHtml(BaseStep):

    def run(self):
        return BeautifulSoup(self.result, 'html.parser')


class ExtractHTML(BaseStep):
    def __init__(self, selector):
        super().__init__()
        self.selector = selector

    def run(self):
        return self.result.select(self.selector)


class BundleHTML(BaseStep):

    def run(self):
        result = {}
        for item in self.result:
            result[item.find_previous('h4').text.removesuffix('[]')] = item
        return result


class Show(BaseStep):

    def run(self):
        print(self.result)
        return self.result


class ParseTable(BaseStep):

    def run(self):
        result = {}
        for table_name, table in self.result.items():
            result[table_name] = pd.read_html(str(table))
        return result


class UpdateDfWithKey(BaseStep):

    def run(self):
        result = []
        for table_name, table in self.result.items():
            table = table[0]
            table['added_in'] = table_name
            result.append(table)
        return result


class Union(BaseStep):

    def run(self):
        return pd.concat(self.result, ignore_index=True)


class DfToSQLite(BaseStep):

    def __init__(self, db_name, table_name):
        super().__init__()
        self.db_name = db_name
        self.table_name = table_name

    def run(self):
        conn = sqlite3.connect(self.db_name)
        self.result.to_sql(self.table_name, conn, if_exists='replace', index=False)
        conn.close()
        return self.result
