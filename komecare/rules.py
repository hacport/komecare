# The scam wording rules.
#
# Each rule is: name, weight, the reason shown to the user, and the phrases
# that trigger it. Higher weight = stronger sign of a scam.
# Gift cards and remote access are the highest because real companies
# don't ask for those.

RULES = [
    {
        "name": "urgency",
        "weight": 2,
        "reason": "It pressures you to act quickly.",
        "phrases": [
            "urgent", "urgently", "immediately", "act now", "right away",
            "within 24 hours", "final notice", "last chance", "click here now",
        ],
    },
    {
        "name": "account threat",
        "weight": 2,
        "reason": "It threatens that an account will be closed or suspended.",
        "phrases": [
            "suspended", "will be closed", "has been locked", "unusual activity",
            "unauthorised", "unauthorized", "has been compromised",
        ],
    },
    {
        "name": "asking for details",
        "weight": 3,
        "reason": "It asks for bank details, passwords or other private information.",
        "phrases": [
            "bank details", "card details", "verify your account",
            "verify your details", "confirm your details", "confirm your password",
            "your pin", "security code", "national insurance number",
        ],
    },
    {
        "name": "gift cards",
        "weight": 4,
        "reason": "It asks for payment by gift card. Real organisations never do this.",
        "phrases": ["gift card", "gift cards", "itunes card", "amazon voucher", "google play card"],
    },
    {
        "name": "remote access",
        "weight": 4,
        "reason": "It asks you to install a program that lets a stranger control your computer.",
        "phrases": ["anydesk", "teamviewer", "remote access", "remote desktop"],
    },
    {
        "name": "money",
        "weight": 2,
        "reason": "It promises money, a refund or a prize.",
        "phrases": ["you have won", "tax refund", "claim your prize", "claim your refund", "compensation"],
    },
    {
        "name": "delivery",
        "weight": 1,
        "reason": "It mentions a missed parcel or delivery fee, a common scam story.",
        "phrases": ["missed delivery", "redelivery", "delivery fee", "parcel is waiting"],
    },
]
