<p align="center">
    <h1>🚀 Pydoll: Async Web Automation in Python!</h1>
</p>
<br>
<p align="center">
    <img src="https://github.com/user-attachments/assets/c4615101-d932-4e79-8a08-f50fbc686e3b" alt="Alt text" /> <br><br>
</p>

<p align="center">
    <img src="https://codecov.io/github/thalissonvs/pydoll/graph/badge.svg?token=40I938OGM9"/> 
    <img src="https://github.com/thalissonvs/pydoll/actions/workflows/tests.yml/badge.svg" alt="Tests">
    <img src="https://github.com/thalissonvs/pydoll/actions/workflows/ruff-ci.yml/badge.svg" alt="Ruff CI">
    <img src="https://github.com/thalissonvs/pydoll/actions/workflows/release.yml/badge.svg" alt="Release">
    <img src="https://tokei.rs/b1/github/thalissonvs/pydoll" alt="Total lines">
    <img src="https://tokei.rs/b1/github/thalissonvs/pydoll?category=files" alt="Files">
    <img src="https://tokei.rs/b1/github/thalissonvs/pydoll?category=comments" alt="Comments">
    <img src="https://img.shields.io/github/issues/thalissonvs/pydoll?label=Issues" alt="GitHub issues">
    <img src="https://img.shields.io/github/issues-closed/thalissonvs/pydoll?label=Closed issues" alt="GitHub closed issues">
    <img src="https://img.shields.io/github/issues/thalissonvs/pydoll/bug?label=Bugs&color=red" alt="GitHub bug issues">
    <img src="https://img.shields.io/github/issues/thalissonvs/pydoll/enhancement?label=Enhancements&color=purple" alt="GitHub enhancement issues">
</p>
<p align="center">
    <a href="https://trendshift.io/repositories/13125" target="_blank"><img src="https://trendshift.io/api/badge/repositories/13125" alt="thalissonvs%2Fpydoll | Trendshift" style="width: 250px; height: 55px;" width="250" height="55"/></a>
</p>

Pydoll is an innovative Python library that's redefining Chromium browser automation! Unlike other solutions, Pydoll **completely eliminates the need for webdrivers**, providing a much more fluid and reliable automation experience.



## ⭐ Extraordinary Features

- **Zero Webdrivers!** Say goodbye to webdriver compatibility and configuration headaches
- **Native Captcha Bypass!** Naturally passes through Cloudflare Turnstile and reCAPTCHA v3 *
- **Performance** thanks to native asynchronous programming
- **Realistic Interactions** that simulate human behavior
- **Advanced Event System** for complex and reactive automations

> Note: for cloudflare captcha, you have to perform a click in the checkbox. Just find a div containing the iframe and use the `.click()` method. Automatic detection and click coming soon! 
  
## Table of Contents

- [Installation](#-installation)
- [Quick Start](#-quick-start)
- [Core Components](#-core-components)
  - [Browser Interface](#browser-interface)
  - [Page Interface](#page-interface)
  - [WebElement Interface](#webelement-interface)
- [Advanced Features](#-advanced-features)
  - [Event System](#event-system)
  - [Concurrent Scraping](#concurrent-scraping)
  - [Proxy Configuration](#proxy-configuration)
- [Event Monitoring](#-event-monitoring)
  - [Page Events](#page-events)
  - [Network Events](#network-events)
  - [DOM Events](#dom-events)
  - [Fetch Events](#fetch-events)
- [Troubleshooting](#-troubleshooting)
- [Best Practices](#-best-practices)
- [Contributing](#-contributing)

## 🔥 Installation

```bash
pip install pydoll-python
```

## ⚡ Quick Start

See how simple it is to get started - no webdriver configuration needed!

```python
import asyncio
from pydoll.browser.chrome import Chrome
from pydoll.constants import By

async def main():
    # Start the browser with no additional webdriver configuration!
    async with Chrome() as browser:
        await browser.start()
        page = await browser.get_page()
        
        # Navigate through captcha-protected sites without worry
        await page.go_to('https://example-with-cloudflare.com')
        button = await page.find_element(By.CSS_SELECTOR, 'button')
        await button.click()

asyncio.run(main())
```

## 🎯 Core Components

### Browser Interface

The Browser domain provides direct control over the browser itself, offering global methods to manage the entire browser instance. Unlike page-specific operations, these methods affect the browser as a whole, allowing you to control multiple pages, handle window properties, manage cookies across all domains, and monitor events throughout the entire browsing session.

Here's an example of how to use the Browser domain:

```python
async def browser_examples():
    async with Chrome() as browser:
        await browser.start()
        # Control multiple pages with incredible ease
        pages = [await browser.get_page() for _ in range(3)]
        
        # Advanced settings with a simple command
        await browser.set_window_maximized()
```

#### Browser Management

Now, let's dive into the methods of the Browser domain.

##### `async start() -> None`
Fires up your browser and gets everything ready for automation magic!

```python
async with Chrome() as browser:
    await browser.start()  # Starts the browser
```

##### `async stop() -> None`
Gracefully shuts down the browser when you're done.

```python
await browser.stop()  # Manually stops the browser
```

##### `async get_page() -> Page`
Grabs an existing page or creates a fresh one if needed - super convenient!

```python
# Gets an existing page or creates a new one
page = await browser.get_page()
await page.go_to("https://www.example.com")
```

##### `async new_page(url: str = '') -> str`
Opens a brand new page and returns its ID for future reference.
Always prefer using the `get_page` method to get a page instance.

```python
# Creates a new page and navigates directly to a URL
page_id = await browser.new_page("https://www.example.com")
```

##### `async get_page_by_id(page_id: str) -> Page`
Lets you access any specific page using its ID - perfect for multi-tab automation!

```python
# Gets a specific page by ID
page = await browser.get_page_by_id(page_id)
```

##### `async get_targets() -> list`
Shows you all open pages in the browser - great for keeping track of everything.

```python
# Lists all open pages in the browser
targets = await browser.get_targets()
for target in targets:
    print(f"Page: {target.get('title')} - URL: {target.get('url')}")
```

Want to switch between tabs or pages? It's super easy! First, get all your targets:

```python
targets = await browser.get_targets()
```

You'll get something like this:

```python
[{'targetId': 'F4729A95E0E4F9456BB6A853643518AF', 'type': 'page', 'title': 'New Tab', 'url': 'chrome://newtab/', 'attached': False, 'canAccessOpener': False, 'browserContextId': 'C76015D1F1C690B7BC295E1D81C8935F'}, {'targetId': '1C44D55BEEE43F44C52D69D8FC5C3685', 'type': 'iframe', 'title': 'chrome-untrusted://new-tab-page/one-google-bar?paramsencoded=', 'url': 'chrome-untrusted://new-tab-page/one-google-bar?paramsencoded=', 'attached': False, 'canAccessOpener': False, 'browserContextId': 'C76015D1F1C690B7BC295E1D81C8935F'}]
```

Then just pick the page you want:

```python
target = next(target for target in targets if target['title'] == 'New Tab')
```

And switch to it:

```python
new_tab_page = await browser.get_page_by_id(target['targetId'])
```

Now you can control this page as if it were the only one open! Switch between tabs effortlessly by keeping references to each page.

##### `async set_window_bounds(bounds: dict) -> None`
Position and size your browser window exactly how you want it!

```python
# Sets the size and position of the window
await browser.set_window_bounds({
    'left': 100, 
    'top': 100, 
    'width': 1024, 
    'height': 768
})
```

##### `async set_window_maximized() -> None`
Make your browser take up the full screen with one simple command.

```python
# Maximizes the browser window
await browser.set_window_maximized()
```

##### `async set_window_minimized() -> None`
Hide the browser window when you don't need to see it.

```python
# Minimizes the browser window
await browser.set_window_minimized()
```

##### `async get_cookies() -> list[dict]`
Peek into all cookies stored by the browser - great for debugging or session management!

```python
# Gets all cookies
cookies = await browser.get_cookies()
for cookie in cookies:
    print(f"Name: {cookie['name']}, Value: {cookie['value']}")
```

##### `async set_cookies(cookies: list[dict]) -> None`
Set up custom cookies for authentication or testing scenarios.

```python
# Sets cookies in the browser
await browser.set_cookies([
    {
        'name': 'session_id',
        'value': '12345',
        'domain': 'example.com',
        'path': '/',
        'expires': -1,  # Session
        'secure': True
    }
])
```

##### `async delete_all_cookies() -> None`
Wipe all cookies clean - perfect for testing from a fresh state!

```python
# Clears all cookies
await browser.delete_all_cookies()
```

##### `async set_download_path(path: str) -> None`
Tell your browser exactly where to save downloaded files.

```python
# Sets the directory to save downloads
await browser.set_download_path("/path/to/downloads")
```

##### `async on(event_name: str, callback: callable, temporary: bool = False) -> int`
Registers a callback for a specific event. You can read more about the events in the [Event Monitoring](#event-monitoring) section.


### Page Interface

Individual page control with surgical precision:

```python
async def page_examples():
    page = await browser.get_page()
    
    # Smooth navigation, even on protected sites
    await page.go_to('https://site-with-recaptcha.com')
    
    # Capture perfect screenshots
    await page.get_screenshot('/screenshots/evidence.png')
```

### WebElement Interface

Interact with elements like a real user:

```python
async def element_examples():
    # Natural and precise interactions
    input_field = await page.find_element(By.CSS_SELECTOR, 'input')
    await input_field.type_keys('Hello World')  # Realistic typing!
    
    # Intuitive chained operations
    dropdown = await page.find_element(By.CSS_SELECTOR, 'select')
    await dropdown.select_option('value')

    # Realistic clicks with offset
    button = await page.find_element(By.CSS_SELECTOR, 'button')
    await button.click(x_offset=5, y_offset=10)
```

## 🚀 Advanced Features

### Event System

Powerful event system for intelligent automation:

```python
from pydoll.events.page import PageEvents

async def event_example():
    await page.enable_page_events()
    # React to events in real-time!
    await page.on(PageEvents.PAGE_LOADED, 
                  lambda e: print('Page loaded successfully!'))
```

### Concurrent Scraping

Scrape multiple pages simultaneously with extraordinary performance:

```python
async def concurrent_example():
    pages = [await browser.get_page() for _ in range(10)]
    # Parallel scraping with intelligent resource management
    results = await asyncio.gather(
        *(scrape_page(page) for page in pages)
    )
    # Just declare the scrape_page method and see the magic happens!
```

### Proxy Configuration

Robust proxy support, including authentication:

```python
async def proxy_example():
    options = Options()
    # Private or public proxies, you choose!
    options.add_argument('--proxy-server=username:password@ip:port')
    
    async with Chrome(options=options) as browser:
        await browser.start()
```


For exploring all available methods and additional features, check out:
- Browser interface: [pydoll/browser/base.py](./pydoll/browser/base.py)
- Page interface: [pydoll/browser/page.py](./pydoll/browser/page.py)
- WebElement interface: [pydoll/element.py](./pydoll/element.py)
- Chrome options: [Chromium Command Line Switches](https://peter.sh/experiments/chromium-command-line-switches/)

## 🎉 Start Now!

Feel free to use, open issues and contributing!
