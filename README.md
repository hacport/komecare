# KomeCare

A scam checker for older people, written in Python.

You paste in an email, a text or a link. It tells you if it looks like a scam, with a red, amber or green verdict and the reasons in normal English.


## Why I'm making this

My mum used to work at a home-care company, and the carers there kept getting asked the same things by elderly clients. "Is this email real?" "My computer says it has a virus, what do I press?" "I've forgotten my password again."

I looked at what already exists. Antivirus software is good at catching threats, but it explains them in language most people can't follow, never mind someone in their seventies. The simple launchers made for older users are easy to use but have no protection in them at all. I couldn't find one thing that does both, so I started building it.


## How it works

It looks at two things, the wording and the links.

**The wording.** Scam messages lean on the same tricks again and again, so I grouped them into rules: rushing you, threatening to close your account, asking for bank details or passwords, asking for gift cards, asking you to install remote-access software, promising money, and fake delivery notices. Each rule has a weight. Gift cards and remote access score highest because a real company basically never asks for those. A rule only counts once, so a message can't rack up points just by saying "urgent" five times.

**The links.** It pulls out every web address and checks for:

- lookalike names like `amaz0n.co.uk` or `paypa1.com`. It swaps the fake characters back (0 to o, 1 to l) and compares the name with real UK brands
- a real brand name sitting on someone else's domain, like `hmrc.gov.uk.verify-login.com`
- links that are just numbers, links with disguised characters, shortened links, and plain `http`

**The verdict.** The weights get added up. Under 2 is green, 2 to 4 is amber, 5 and over is red. Every point comes with a reason the user can read.


## What's next

- [x] Threat scanner (wording rules and link checks)
- [x] Tests for the scanner
- [ ] Password vault, with the key made from the master password using Argon2id and entries encrypted with AES-256-GCM
- [ ] Carer login that locks after too many wrong tries
- [ ] SQLite database for the vault, reminders and settings
- [ ] Activity log that shows if anyone has tampered with it
- [ ] Email scanning over IMAP, including checking if the sender is who they say they are (SPF, DKIM, DMARC)
- [ ] Big-button interface designed for older users
- [ ] Diary and reminders
- [ ] Test it against public phishing datasets and publish the hit rate and false alarm rate
- [ ] Write up the threat model

## Design

I planned the whole thing before writing code. The design document is in [docs/KomeCare-design.pdf](docs/KomeCare-design.pdf). It has the data flow diagrams, the database design, the algorithms and the test plan. Some decisions have changed since I wrote it, and this README is the up to date version.

## Files

```
komecare/
  rules.py      the scam wording rules and their weights
  urls.py       finds links and checks for lookalikes
  scanner.py    adds up the score and gives the verdict
tests/
  test_scanner.py
docs/
  KomeCare-design.pdf   the original design document
```
