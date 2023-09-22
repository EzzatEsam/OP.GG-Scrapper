from selenium import webdriver
def hardClickElement(driver ,element):
    driver.execute_script("arguments[0].click();", element)

def load_page_with_timeout(driver : webdriver, url : str, timeout=5):
    driver.set_page_load_timeout(timeout)
    try:
        driver.get(url)
    except:
        driver.execute_script("window.stop();")

    
def time_string_to_seconds(time_string : str) -> int :

    # Split the time string into minutes and seconds parts
    minutes, seconds = time_string.split('m ')

    # Remove the 's' character from the seconds part
    seconds = seconds.rstrip('s')

    # Convert minutes and seconds to integers
    minutes = int(minutes)
    seconds = int(seconds)

    # Calculate the total seconds
    total_seconds = minutes * 60 + seconds
    return total_seconds
