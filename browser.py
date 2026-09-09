import pychrome

CHROME_URL = "http://localhost:9222"

def connect():
    browser = pychrome.Browser(url=CHROME_URL)
    tab = browser.new_tab()
    tab.start()
    return tab

def goto(tab, url):
    tab.Page.enable()
    tab.Page.navigate(url=url)
    tab.wait(3)

def read_text(tab):
    reply = tab.Runtime.evaluate(expression="document.body ? document.body.innerText : ''")
    return reply["result"].get("value", "")

def list_links(tab):
    js = """
    Array.from(document.querySelectorAll('a'))
      .filter(a => a.innerText.trim())
      .slice(0, 30)
      .map((a, i) => i + ': ' + a.innerText.trim() + ' -> ' + a.href)
      .join('\\n')
    """
    reply = tab.Runtime.evaluate(expression=js)
    return reply["result"]["value"]

def click_link(tab, index):
    js = f"""
    Array.from(document.querySelectorAll('a'))
      .filter(a => a.innerText.trim())[{index}].click()
    """
    tab.Runtime.evaluate(expression=js)
    tab.wait(3)

def current_url(tab):
    reply = tab.Runtime.evaluate(expression="location.href")
    return reply["result"]["value"]