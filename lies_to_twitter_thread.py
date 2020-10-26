from os import environ

from TwitterAPI import TwitterAPI
from threader import Threader

from the_lies import lies
from lie_fetcher import concat

keys = dict(
    consumer_key=environ["CONSUMER_KEY"],
    consumer_secret=environ["CONSUMER_SECRET"],
    access_token_key=environ["ACCESS_TOKEN_KEY"],
    access_token_secret=environ["ACCESS_TOKEN_SECRET"],
)
api = TwitterAPI(**keys)


def lie_to_tweet(lie: str, lie_no: int) -> str:
    return f"LIE #{lie_no}" + lie[3:]


header_tweet = "News Flash: #ModiLies! Here is a list of the lies Modiji has said over the years. (from June/2014 to this month). To fact-check visit modilies.in"

if __name__ == "__main__":
    lies_list = [
        lie_to_tweet(lie, n + 1) for n, lie in enumerate(concat(lies.values()))
    ]
    for lie in (l for l in lies_list if len(l) >= 270):
        print(lie)
    tweets = [header_tweet] + lies_list

    th = Threader(tweets, api)
    th.send_tweets()
