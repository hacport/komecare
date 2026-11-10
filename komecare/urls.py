# Link checks. Finds the web addresses in a message and looks for the
# tricks scammers use to make a fake site look like a real one.

import re
from difflib import SequenceMatcher
from urllib.parse import urlparse

# real sites that get copied a lot in the UK
TRUSTED_DOMAINS = [
    "amazon.co.uk", "amazon.com", "gov.uk", "nhs.uk", "royalmail.com",
    "paypal.com", "barclays.co.uk", "lloydsbank.com", "hsbc.co.uk",
    "natwest.com", "santander.co.uk", "halifax.co.uk", "nationwide.co.uk",
    "evri.com", "dpd.co.uk", "bt.com", "tvlicensing.co.uk", "apple.com",
    "microsoft.com", "google.com",
]

# brand name -> the only domain it should appear on
BRANDS = {
    "amazon": "amazon.co.uk",
    "hmrc": "gov.uk",
    "nhs": "nhs.uk",
    "royalmail": "royalmail.com",
    "paypal": "paypal.com",
    "barclays": "barclays.co.uk",
    "lloyds": "lloydsbank.com",
    "hsbc": "hsbc.co.uk",
    "natwest": "natwest.com",
    "santander": "santander.co.uk",
    "halifax": "halifax.co.uk",
    "evri": "evri.com",
    "tvlicensing": "tvlicensing.co.uk",
}

SHORTENERS = ["bit.ly", "tinyurl.com", "t.co", "goo.gl", "ow.ly", "is.gd", "cutt.ly"]

# characters that get swapped in to fake a letter, e.g. amaz0n
SWAPS = {"0": "o", "1": "l", "3": "e", "5": "s", "@": "a", "$": "s"}

# endings that are two parts long, so the name is the bit before them
TWO_PART_ENDINGS = ["co.uk", "org.uk", "gov.uk", "ac.uk", "nhs.uk", "me.uk", "ltd.uk"]


def find_links(text):
    """Get every web address out of a message."""
    links = re.findall(r"(?:https?://|www\.)[^\s<>\"']+", text, re.IGNORECASE)
    # a link at the end of a sentence picks up the full stop, so strip it
    return [link.rstrip(".,;:!?)") for link in links]


def get_host(link):
    """Get the site part of a link, e.g. 'amazon.co.uk' from the full address."""
    if not link.lower().startswith("http"):
        link = "http://" + link
    host = urlparse(link).hostname
    if host is None:
        return ""
    host = host.lower()
    if host.startswith("www."):
        host = host[4:]
    return host


def is_trusted(host):
    """True if the host is a trusted site or a real subdomain of one."""
    for domain in TRUSTED_DOMAINS:
        if host == domain or host.endswith("." + domain):
            return True
    return False


def undo_swaps(text):
    """Turn amaz0n back into amazon."""
    result = ""
    for char in text:
        result += SWAPS.get(char, char)
    return result


def get_name(host):
    """Get the main name from a host: 'amazon' from 'shop.amazon.co.uk'."""
    parts = host.split(".")
    if ".".join(parts[-2:]) in TWO_PART_ENDINGS:
        ending_length = 2
    else:
        ending_length = 1
    if len(parts) <= ending_length:
        return ""
    return parts[-ending_length - 1]


def find_lookalike(host):
    """If this host is pretending to be a trusted site, return which one.

    Only the name part is compared (amaz0n against amazon). Comparing the
    whole address flagged normal sites just for ending in .co.uk.
    Short names like 'bt' have to match exactly, because short words look
    similar to too many innocent ones.
    """
    name = undo_swaps(get_name(host))
    if name == "":
        return None
    for domain in TRUSTED_DOMAINS:
        real_name = get_name(domain)
        if real_name == "":
            continue
        if name == real_name:
            return domain
        if len(real_name) >= 5:
            similarity = SequenceMatcher(None, name, real_name).ratio()
            if similarity >= 0.8:
                return domain
    return None


def find_brand(host):
    """If the host uses a brand name it doesn't own, return (brand, real site)."""
    cleaned = undo_swaps(host)
    words = re.split(r"[.\-]", cleaned)
    for brand, real_site in BRANDS.items():
        if len(brand) >= 5:
            found = brand in cleaned.replace("-", "")
        else:
            # short brands like nhs must be a whole word, or they match by accident
            found = brand in words
        if found:
            return brand, real_site
    return None


def check_link(link):
    """Check one link. Returns a list of (weight, reason)."""
    host = get_host(link)
    problems = []

    if host == "" or is_trusted(host):
        return problems

    if re.fullmatch(r"\d{1,3}(\.\d{1,3}){3}", host):
        problems.append((3, "The link uses a string of numbers instead of a website name."))

    if host.startswith("xn--") or ".xn--" in host:
        problems.append((3, "The link uses disguised characters to imitate another website."))

    if host in SHORTENERS:
        problems.append((1, "The link is shortened, which hides where it really goes."))

    lookalike = find_lookalike(host)
    brand = find_brand(host)
    if lookalike is not None:
        problems.append((4, "The link looks like " + lookalike + " but is not the real website."))
    elif brand is not None:
        problems.append((4, "The link mentions " + brand[0].upper() + " but does not go to " + brand[1] + "."))

    if link.lower().startswith("http://"):
        problems.append((1, "The link is not secure (it starts with http, not https)."))

    return problems
