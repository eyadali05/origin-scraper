# to use the script install playwright with 'pip install playwright' then 'playwright install' then get the origin url you want and place it in the game_url variable
import playwright
from playwright.sync_api import sync_playwright
import logging
import time

game_url = "https://www.origin.com/egy/en-us/store/fifa/fifa-22"
#logging.basicConfig(format="%(asctime)s - %(message)s", level=logging.INFO)


def get_name(page):
    try:
        title_locator = "h1.otktitle-page.otkex-product-hero-title"
        title = page.locator(title_locator).text_content()
    except playwright._impl._api_types.TimeoutError:
        img_locator = "img.otkex-product-hero-logo"
        title_html = page.locator(img_locator)
        title = title_html.get_attribute("alt")
    return title


def get_dev_name(page):
    dev_name_locator = "span.origin-store-pdp-overview-item-message >> nth=4"
    dev_name = page.locator(dev_name_locator).text_content()
    return dev_name


def clean_price(text):
    cleaned = ""
    for character in text:
        try:
            int(character)
            cleaned += character
        except ValueError:
            continue
    cleaned = str(int(cleaned) / 100)
    return cleaned


def get_price(page):
    main_button_selector = "button.otkbtn.otkbtn-primary.otkbtn-primary-btn >> nth=1"
    main_button_text = page.locator(main_button_selector).inner_text()
    if main_button_text == "Get the Game":
        page.wait_for_selector(main_button_selector)
        page.locator(main_button_selector).click()
        time.sleep(2)
        price_button_selector = "button.otkbtn.otkbtn-transparent.otkex-cta >> nth=1"
        price_button_value = page.locator(price_button_selector).inner_text()
        if price_button_value:
            price = clean_price(price_button_value)
    else:
        price = clean_price(main_button_text)

    return price


def scrape_origin(url):
    with sync_playwright() as pw:
        browser = pw.chromium.launch(headless=True, slow_mo=50)
        page = browser.new_page()
        page.set_default_timeout(45000)
        page.goto(url)
        logging.info("page is loaded")
        logging.info("getting title")
        title = get_name(page)
        logging.info("got title")
        logging.info("getting developer name")
        dev_name = get_dev_name(page)
        logging.info("got developer name")
        logging.info("getting price")
        price = get_price(page)
        logging.info("got price")
        browser.close()
    game_data = [title, price, game_url, dev_name, "ORIGIN"]
    logging.info("set up data to be output")
    return game_data


output = scrape_origin(game_url)
if output and len(output) > 1 and list(output):
    for out in output:
        print(out)
