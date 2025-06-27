from flask import Flask, request, jsonify
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import traceback
import logging
import threading
import queue
import time

app = Flask(__name__)
logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')
logger = logging.getLogger(__name__)

# === Shared resources ===
task_queue = queue.Queue()
result_queue = queue.Queue()

# === Chrome worker thread ===
def browser_worker():
    logger.info("Worker: Starting Chrome browser once")
    options = uc.ChromeOptions()
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--disable-gpu")

    driver = uc.Chrome(
        options=options,
        headless=True,
        suppress_welcome=True,
        use_subprocess=True,
        version_main=137
    )

    while True:
        task = task_queue.get()
        if task is None:  # Exit signal
            break

        request_id, url = task
        logger.info(f"Worker: Processing URL: {url}")
        try:
            driver.get(url)
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )
            html = driver.page_source
            title = driver.title
            result_queue.put((request_id, {"title": title, "html": html}))
        except Exception as e:
            result_queue.put((request_id, {"error": str(e)}))
        finally:
            task_queue.task_done()

    logger.info("Worker: Quitting browser")
    driver.quit()

# Start background Chrome worker thread
worker_thread = threading.Thread(target=browser_worker, daemon=True)
worker_thread.start()

@app.route('/visit', methods=['GET'])
def visit():
    url = request.args.get('url')
    if not url:
        return jsonify({"error": "Missing URL"}), 400

    request_id = str(time.time()) + threading.current_thread().name
    logger.info(f"Received /visit request: {url} [{request_id}]")
    task_queue.put((request_id, url))

    # Wait for result (max 15s timeout)
    start_time = time.time()
    while time.time() - start_time < 15:
        try:
            res_id, result = result_queue.get(timeout=1)
            if res_id == request_id:
                return jsonify(result)
            else:
                # not mine → requeue it
                result_queue.put((res_id, result))
        except queue.Empty:
            pass

    return jsonify({"error": "Timeout while processing request"}), 504

@app.route('/')
def index():
    return "Welcome to the Fast Chrome Pool Web Scraper!"

if __name__ == '__main__':
    logger.info("Starting Flask app on 0.0.0.0:5003")
    app.run(host='0.0.0.0', port=5003, threaded=True)
