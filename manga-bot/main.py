from flask import Flask, request, jsonify
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import traceback
import logging
import os

app = Flask(__name__)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s'
)
logger = logging.getLogger(__name__)

@app.route('/visit', methods=['GET'])
def visit():
    try:
        url = request.args.get('url')
        logger.info(f"Received /visit request with url: {url}")
        if not url:
            logger.warning("Missing URL parameter in request")
            return jsonify({"error": "Missing URL"}), 400

        # Chrome Options
        options = uc.ChromeOptions()
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_argument("--disable-gpu")

        logger.info("Starting undetected_chromedriver")
        user_data_dir = os.path.join(os.getcwd(), "user-data")
        if not os.path.exists(user_data_dir):
                os.makedirs(user_data_dir)
        options.add_argument(f"--user-data-dir={user_data_dir}")
        driver = uc.Chrome(
            options=options,
            headless=True,
            suppress_welcome=True,
            use_subprocess=True,
            version_main=137
        )
        logger.info(f"Navigating to URL: {url}")
        driver.get(url)
        # Wait for the page to load completely
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )

        html = driver.page_source
        title = driver.title

        driver.quit()
        logger.info(f"Successfully scraped URL: {url} with title: {title}")

        return jsonify({
            "title": title,
            "html": html,
        })

    except Exception as e:
        logger.error(f"Error occurred while processing /visit: {e}")
        logger.debug(traceback.format_exc())
        return jsonify({"error": str(e)}), 500


@app.route('/')
def index():
    logger.info("Received request for index route")
    return "Welcome to the Selenium Web Scraper API! Use the /visit endpoint to scrape web pages."

if __name__ == '__main__':
    logger.info("Starting Flask app on 0.0.0.0:3001")
    app.run(host='0.0.0.0', port=3001)
