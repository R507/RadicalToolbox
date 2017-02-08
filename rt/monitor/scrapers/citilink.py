import logging

import bs4

from rt.monitor.scrapers import base

logger = logging.getLogger(__name__)


class Scraper(base.Scraper):

    @classmethod
    def _extract_value(cls, content):
        soup = bs4.BeautifulSoup(content, "html.parser")
        parent_class = soup.find('div', class_='price price_break')
        desired_class = parent_class.find('ins', class_='num')
        value = desired_class.get_text()
        value = value.replace(' ', '')
        value = float(value)  # TODO: float doesn't seem right
        # TODO: handle potential data corruption
        retval = {'value': value}
        return retval


def main():
    # TODO: make proper tests
    value = Scraper.get_result(
        r"https://www.citilink.ru/catalog/"
        r"computers_and_notebooks/parts/videocards/405775/"
    )
    print("Result:\n{}".format(value))


if __name__ == '__main__':
    main()
