
import pytest
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options

@pytest.fixture(scope="function")
def driver():
    options = Options()
    # headless confiável nas versões recentes do Chrome
    options.add_argument("--headless=new")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")  # evita /dev/shm pequeno
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--lang=en-US")
    options.add_argument("--remote-allow-origins=*")
    options.page_load_strategy = "eager"

    # reduz pistas de automação (alguns sites se incomodam)
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("useAutomationExtension", False)

    service = ChromeService(ChromeDriverManager().install())
    drv = webdriver.Chrome(service=service, options=options)
    drv.set_window_size(1920, 1080)

    # pequena ajuda para alguns bloqueios
    drv.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
        "source": """
            Object.defineProperty(navigator, 'webdriver', {get: () => undefined})
        """
    })

    yield drv
    drv.quit()
