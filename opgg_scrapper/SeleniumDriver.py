from selenium import webdriver

def get_chrome(headless :bool = False, adblock_extenstion_path : str = None ) -> webdriver.Chrome :
    """
    Initializes and returns a Chrome WebDriver instance.

    Args:
        headless (bool, optional): Whether to run in headless mode. Defaults to False.
        adblock_extenstion_path (str, optional): The path to the adblock extension. Defaults to None.

    Returns:
        webdriver.Chrome: A Chrome WebDriver instance.
    """
    options = webdriver.ChromeOptions()
    options.add_argument('--ignore-certificate-errors')
    if adblock_extenstion_path != None :
        options.add_extension(adblock_extenstion_path)
    if headless :
        options.add_argument('--headless')
    options.add_argument('--blink-settings=imagesEnabled=false')
    options.add_argument("--log-level=3")

    return webdriver.Chrome( options=options )

