from urllib.parse import urlparse
import re
import requests
from bs4 import BeautifulSoup


def extract_features(url):
    """
    Extract the 50 features expected by the TrustLens
    Random Forest model.

    The extractor uses URL information first and attempts
    to inspect the webpage when it is reachable.
    """

    parsed = urlparse(url)

    # --------------------------------------------------
    # Basic URL information
    # --------------------------------------------------

    domain = parsed.netloc
    hostname = parsed.hostname or ""

    # Remove port if present
    domain_without_port = hostname

    is_ip = bool(
        re.fullmatch(
            r"\d{1,3}(\.\d{1,3}){3}",
            domain_without_port
        )
    )

    tld = ""

    if not is_ip and "." in domain_without_port:
        tld = domain_without_port.split(".")[-1]

    url_length = len(url)
    domain_length = len(domain)

    letters = sum(c.isalpha() for c in url)
    digits = sum(c.isdigit() for c in url)

    special_chars = sum(
        not c.isalnum() and c not in "/.?&=_-:"
        for c in url
    )

    # --------------------------------------------------
    # URL-based features
    # --------------------------------------------------

    no_subdomains = (
        0
        if is_ip
        else max(0, len(domain_without_port.split(".")) - 2)
    )

    suspicious_chars = ["@", "-", "_", "%", "//"]

    no_obfuscated = sum(
        url.count(char)
        for char in suspicious_chars
    )

    has_obfuscation = int(no_obfuscated > 0)

    url_length_safe = max(url_length, 1)

    letter_ratio = letters / url_length_safe
    digit_ratio = digits / url_length_safe
    special_ratio = special_chars / url_length_safe

    tld_length = len(tld)

    # --------------------------------------------------
    # Default webpage features
    # --------------------------------------------------

    line_of_code = 0
    largest_line_length = 0

    has_title = 0
    title = ""

    domain_title_match = 0.0
    url_title_match = 0.0

    has_favicon = 0
    robots = 0
    is_responsive = 0

    no_url_redirect = 0
    no_self_redirect = 0

    has_description = 0

    no_popup = 0
    no_iframe = 0

    has_external_form_submit = 0
    has_social_net = 0

    has_submit_button = 0
    has_hidden_fields = 0
    has_password_field = 0

    bank = 0
    pay = 0
    crypto = 0

    has_copyright = 0

    no_image = 0
    no_css = 0
    no_js = 0

    no_self_ref = 0
    no_empty_ref = 0
    no_external_ref = 0

    # --------------------------------------------------
    # Try to fetch webpage
    # --------------------------------------------------

    html = ""

    try:
        response = requests.get(
            url,
            timeout=5,
            headers={
                "User-Agent": "Mozilla/5.0 TrustLens"
            },
            allow_redirects=True
        )

        html = response.text

        no_url_redirect = len(response.history)

        final_url = response.url

        if parsed.netloc and urlparse(final_url).netloc == parsed.netloc:
            no_self_redirect = no_url_redirect

    except Exception:
        html = ""

    # --------------------------------------------------
    # HTML analysis
    # --------------------------------------------------

    if html:

        soup = BeautifulSoup(html, "html.parser")

        # Lines
        lines = html.splitlines()

        line_of_code = len(lines)

        if lines:
            largest_line_length = max(
                len(line)
                for line in lines
            )

        # Title
        title_tag = soup.find("title")

        if title_tag:
            has_title = 1
            title = title_tag.get_text(
                strip=True
            ).lower()

        # Domain/title similarity
        if title and domain_without_port:

            domain_words = set(
                re.findall(
                    r"[a-zA-Z0-9]+",
                    domain_without_port.lower()
                )
            )

            title_words = set(
                re.findall(
                    r"[a-zA-Z0-9]+",
                    title
                )
            )

            if domain_words:
                domain_title_match = (
                    len(domain_words & title_words)
                    / len(domain_words)
                )

            url_words = set(
                re.findall(
                    r"[a-zA-Z0-9]+",
                    url.lower()
                )
            )

            if url_words:
                url_title_match = (
                    len(url_words & title_words)
                    / len(url_words)
                )

        # Description
        description = soup.find(
            "meta",
            attrs={"name": re.compile(
                "^description$",
                re.I
            )}
        )

        has_description = int(
            description is not None
        )

        # Favicon
        favicon = soup.find(
            "link",
            rel=lambda value:
            value and "icon" in str(value).lower()
        )

        has_favicon = int(
            favicon is not None
        )

        # Responsive design
        viewport = soup.find(
            "meta",
            attrs={"name": "viewport"}
        )

        is_responsive = int(
            viewport is not None
        )

        # Robots
        robots_meta = soup.find(
            "meta",
            attrs={"name": re.compile(
                "^robots$",
                re.I
            )}
        )

        robots = int(
            robots_meta is not None
        )

        # iFrames
        no_iframe = len(
            soup.find_all("iframe")
        )

        # Forms
        forms = soup.find_all("form")

        for form in forms:

            action = form.get("action", "")

            if action:
                action_url = urlparse(
                    action
                )

                if (
                    action_url.netloc
                    and action_url.netloc
                    != domain_without_port
                ):
                    has_external_form_submit = 1

        # Buttons
        submit_elements = soup.find_all(
            ["button", "input"]
        )

        for element in submit_elements:

            element_type = str(
                element.get("type", "")
            ).lower()

            value = str(
                element.get("value", "")
            ).lower()

            if (
                element_type == "submit"
                or "submit" in value
            ):
                has_submit_button = 1

        # Hidden fields
        hidden_fields = soup.find_all(
            "input",
            attrs={"type": "hidden"}
        )

        has_hidden_fields = int(
            len(hidden_fields) > 0
        )

        # Password fields
        password_fields = soup.find_all(
            "input",
            attrs={"type": "password"}
        )

        has_password_field = int(
            len(password_fields) > 0
        )

        # Images
        no_image = len(
            soup.find_all("img")
        )

        # CSS
        no_css = len(
            soup.find_all("link")
        )

        # JavaScript
        no_js = len(
            soup.find_all("script")
        )

        # Links
        links = soup.find_all(
            "a",
            href=True
        )

        for link in links:

            href = link.get("href", "").strip()

            if not href:
                no_empty_ref += 1
                continue

            if href.startswith("#"):
                no_self_ref += 1
                continue

            link_parsed = urlparse(
                href
            )

            if (
                link_parsed.netloc
                and link_parsed.netloc
                != domain_without_port
            ):
                no_external_ref += 1
            else:
                no_self_ref += 1

        # Social media
        social_domains = [
            "facebook.com",
            "twitter.com",
            "x.com",
            "instagram.com",
            "linkedin.com",
            "youtube.com"
        ]

        if any(
            social in html.lower()
            for social in social_domains
        ):
            has_social_net = 1

        # Financial keywords
        lower_html = html.lower()

        bank = int(
            any(
                word in lower_html
                for word in [
                    "bank",
                    "banking",
                    "account number"
                ]
            )
        )

        pay = int(
            any(
                word in lower_html
                for word in [
                    "payment",
                    "pay now",
                    "credit card",
                    "debit card"
                ]
            )
        )

        crypto = int(
            any(
                word in lower_html
                for word in [
                    "bitcoin",
                    "crypto",
                    "cryptocurrency",
                    "ethereum"
                ]
            )
        )

        has_copyright = int(
            "copyright" in lower_html
            or "©" in html
        )

        # Popup detection
        no_popup = len(
            re.findall(
                r"window\.open",
                html,
                re.I
            )
        )

    # --------------------------------------------------
    # URL similarity / character features
    # --------------------------------------------------

    url_similarity_index = 100.0

    char_continuation_rate = (
        letters / max(url_length, 1)
    )

    tld_legitimate_prob = 0.5

    url_char_prob = (
        letters / max(url_length, 1)
    )

    # --------------------------------------------------
    # Assemble exactly 50 model features
    # --------------------------------------------------

    features = {

        "URLLength": url_length,
        "DomainLength": domain_length,
        "IsDomainIP": int(is_ip),

        "URLSimilarityIndex":
            url_similarity_index,

        "CharContinuationRate":
            char_continuation_rate,

        "TLDLegitimateProb":
            tld_legitimate_prob,

        "URLCharProb":
            url_char_prob,

        "TLDLength":
            tld_length,

        "NoOfSubDomain":
            no_subdomains,

        "HasObfuscation":
            has_obfuscation,

        "NoOfObfuscatedChar":
            no_obfuscated,

        "ObfuscationRatio":
            no_obfuscated / max(url_length, 1),

        "NoOfLettersInURL":
            letters,

        "LetterRatioInURL":
            letter_ratio,

        "NoOfDegitsInURL":
            digits,

        "DegitRatioInURL":
            digit_ratio,

        "NoOfEqualsInURL":
            url.count("="),

        "NoOfQMarkInURL":
            url.count("?"),

        "NoOfAmpersandInURL":
            url.count("&"),

        "NoOfOtherSpecialCharsInURL":
            special_chars,

        "SpacialCharRatioInURL":
            special_ratio,

        "IsHTTPS":
            int(parsed.scheme.lower() == "https"),

        "LineOfCode":
            line_of_code,

        "LargestLineLength":
            largest_line_length,

        "HasTitle":
            has_title,

        "DomainTitleMatchScore":
            domain_title_match,

        "URLTitleMatchScore":
            url_title_match,

        "HasFavicon":
            has_favicon,

        "Robots":
            robots,

        "IsResponsive":
            is_responsive,

        "NoOfURLRedirect":
            no_url_redirect,

        "NoOfSelfRedirect":
            no_self_redirect,

        "HasDescription":
            has_description,

        "NoOfPopup":
            no_popup,

        "NoOfiFrame":
            no_iframe,

        "HasExternalFormSubmit":
            has_external_form_submit,

        "HasSocialNet":
            has_social_net,

        "HasSubmitButton":
            has_submit_button,

        "HasHiddenFields":
            has_hidden_fields,

        "HasPasswordField":
            has_password_field,

        "Bank":
            bank,

        "Pay":
            pay,

        "Crypto":
            crypto,

        "HasCopyrightInfo":
            has_copyright,

        "NoOfImage":
            no_image,

        "NoOfCSS":
            no_css,

        "NoOfJS":
            no_js,

        "NoOfSelfRef":
            no_self_ref,

        "NoOfEmptyRef":
            no_empty_ref,

        "NoOfExternalRef":
            no_external_ref
    }

    return features