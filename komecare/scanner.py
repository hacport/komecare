# The threat scanner. Gives a message a score, then a GREEN / AMBER / RED verdict.

import sys

from komecare.rules import RULES
from komecare.urls import check_link, find_links

AMBER_SCORE = 2
RED_SCORE = 5

ADVICE = {
    "GREEN": "This looks safe. No warning signs were found.",
    "AMBER": "Be careful. Do not click any links or reply until you have checked with someone you trust.",
    "RED": "Danger. This is very likely a scam. Do not click, reply or pay anything.",
}


def scan_message(text):
    """Scan a message. Returns a dictionary with the verdict, score, reasons and advice."""
    lowered = text.lower()
    score = 0
    reasons = []

    # wording: each rule only counts once, however many of its phrases appear
    for rule in RULES:
        for phrase in rule["phrases"]:
            if phrase in lowered:
                score += rule["weight"]
                reasons.append(rule["reason"])
                break

    # links
    for link in find_links(text):
        for weight, reason in check_link(link):
            score += weight
            if reason not in reasons:
                reasons.append(reason)

    if score >= RED_SCORE:
        verdict = "RED"
    elif score >= AMBER_SCORE:
        verdict = "AMBER"
    else:
        verdict = "GREEN"

    return {
        "verdict": verdict,
        "score": score,
        "reasons": reasons,
        "advice": ADVICE[verdict],
    }


def main():
    if len(sys.argv) > 1:
        text = " ".join(sys.argv[1:])
    else:
        text = input("Paste your message or link here: ")

    result = scan_message(text)
    print()
    print(result["verdict"] + ": " + result["advice"])
    for reason in result["reasons"]:
        print("  - " + reason)


if __name__ == "__main__":
    main()
