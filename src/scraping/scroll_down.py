import time


def scroll_down(driver) -> None:
    """
    Scrolls down the webpage repeatedly until no more new content is loaded.
    """
    
    last_height = driver.execute_script("return document.body.scrollHeight")
    
    while True:
        # Scroll down to the bottom
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        
        # Wait to load the page
        time.sleep(2)

        # Calculate new scroll height and compare with last scroll height
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break  # If no more content is loaded, exit the loop
        last_height = new_height
