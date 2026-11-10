# Tests for the threat scanner. Run with: python -m pytest

from komecare.scanner import scan_message
from komecare.urls import check_link, find_links, get_host


def test_lots_of_scam_signs_is_red():
    message = "Your account has been suspended, verify your bank details urgently, click here now"
    assert scan_message(message)["verdict"] == "RED"


def test_one_urgent_phrase_is_amber():
    assert scan_message("This is an urgent reminder about your delivery")["verdict"] == "AMBER"


def test_normal_message_is_green():
    result = scan_message("Hi Haolat hope you are well see you Thursday for tea")
    assert result["verdict"] == "GREEN"
    assert result["score"] == 0


def test_family_message_is_green():
    message = "Hi Dad just me checking up on you, are you okay I will call you Sunday. Love Janet"
    assert scan_message(message)["verdict"] == "GREEN"


def test_hmrc_scam_is_red():
    message = "Dear customer your HMRC account will be suspended in 24 hours click here to verify your details immediately"
    assert scan_message(message)["verdict"] == "RED"


def test_swapped_character_link_is_caught():
    result = scan_message("Sign in at http://amaz0n.co.uk/login")
    assert result["verdict"] != "GREEN"
    assert "The link looks like amazon.co.uk but is not the real website." in result["reasons"]


def test_gift_card_request_is_caught():
    result = scan_message("Please buy three gift cards and send me the codes")
    assert result["verdict"] != "GREEN"


def test_remote_access_request_is_red():
    message = "This is tech support. Install AnyDesk immediately so we can fix your computer"
    assert scan_message(message)["verdict"] == "RED"


def test_real_sites_are_not_flagged():
    real_links = [
        "https://www.amazon.co.uk/orders",
        "https://www.gov.uk/hmrc",
        "https://www.nhs.uk",
        "https://111.nhs.uk",
    ]
    for link in real_links:
        assert check_link(link) == []


def test_ordinary_sites_are_not_flagged():
    # these were getting flagged when I compared the whole address
    ordinary_links = [
        "https://www.bbc.co.uk/news",
        "https://www.boots.com",
        "https://www.tesco.com",
        "https://www.ageuk.org.uk",
    ]
    for link in ordinary_links:
        assert check_link(link) == []


def test_brand_on_wrong_site_is_caught():
    problems = check_link("https://hmrc.gov.uk.verify-login.com/refund")
    reasons = [reason for weight, reason in problems]
    assert "The link mentions HMRC but does not go to gov.uk." in reasons


def test_number_link_is_caught():
    assert check_link("http://192.168.4.20/login") != []


def test_repeating_a_word_does_not_add_points():
    once = scan_message("urgent")
    many = scan_message("urgent urgent urgent urgent")
    assert once["score"] == many["score"]


def test_finding_links():
    links = find_links("Go to https://www.Example.com/page. Thanks")
    assert links == ["https://www.Example.com/page"]
    assert get_host(links[0]) == "example.com"
