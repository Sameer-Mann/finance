import requests
from flask import render_template
import urllib.parse


def apology(message, code=400):
    """Render message as an apology to user."""
    def escape(s):
        """
        Escape special characters.

        https://github.com/jacebrowning/memegen#special-characters
        """
        for old, new in [("-", "--"), (" ", "-"), ("_", "__"), ("?", "~q"),
                         ("%", "~p"), ("#", "~h"), ("/", "~s"), ("\"", "''")]:
            s = s.replace(old, new)
        return s
    return render_template("apology.html", top=code,
                           bottom=escape(message)), code


def lookup(symbols):
    """Look up quote for symbol."""

    # Contact API
    baseUrl = "https://cloud.iexapis.com/stable/stock/market/batch"
    token = "sk_ef9431148f1b424f81467ffbf7940f02"
    response = requests.get(
        f"{baseUrl}?symbols={urllib.parse(symbols)}&types=quote&token={token}")
    if response.status_code != 200:
        return None

    # Parse response
    try:
        return [{"price": value['quote']['latestPrice'],
                "name": value['quote']['companyName'], "symbol": key}
                for key, value in response.json().items()]
    except (KeyError, TypeError, ValueError):
        return None


def usd(value):
    """Format value as USD."""
    return (f"${value:,.2f}")
