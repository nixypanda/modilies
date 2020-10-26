from datetime import datetime
from typing import List, Generator
from itertools import takewhile
from concurrent.futures import ThreadPoolExecutor

from dateutil.relativedelta import relativedelta
from bs4 import BeautifulSoup
import requests

_BASE_URL = "https://modilies.in"
_LIE_START_DATE = datetime(year=2014, month=6, day=1)
_TODAY = datetime.now()


def concat(lizt):
    return sum(lizt, [])


def date_gen(start_dt: datetime = None) -> Generator:
    dt = start_dt or datetime.now()
    while True:
        yield dt
        dt += relativedelta(months=1)


def get_url(dt: datetime) -> str:
    return f"{_BASE_URL}/{dt.year}/{dt.month}"


def get_lies_for_date(dt: datetime) -> List[str]:
    def extract_lie_from_header(h1) -> List[str]:
        return h1.find_all(text=True)

    url = get_url(dt)
    res = requests.get(url)
    html_doc = res.text

    soup = BeautifulSoup(html_doc, "html.parser")

    return concat(
        [
            extract_lie_from_header(h1)
            for h1 in soup.find_all("h1", class_="entry-title")
        ]
    )


def safe_lie_fetcher(dt: datetime) -> List[str]:
    try:
        print(f"Getting lies for {sexy_str(dt)}")
        return get_lies_for_date(dt)
    except Exception as e:
        print(f"Failed to get lies for {sexy_str(dt)}: {e}")
        return []
    else:
        print(f"Got lies for {sexy_str(dt)}")


def sexy_str(dt: datetime) -> str:
    return f"{dt.year}/{dt.month}"


if __name__ == "__main__":
    print("Getting them lies...")
    dates_of_interest = takewhile(
        lambda dt: dt < datetime.now(), date_gen(start_dt=_LIE_START_DATE),
    )

    with ThreadPoolExecutor(max_workers=50) as ex:
        date_to_futures = {d: ex.submit(safe_lie_fetcher, d) for d in dates_of_interest}
        dikt = {sexy_str(k): v.result() for k, v in date_to_futures.items()}

    print("Saving Lies...")
    with open("the_lies.py", "w") as f:
        f.write(f"lies = {dikt}")
