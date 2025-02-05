
<p align="center">
    <h1>Pydoll: Async Web Automation Library</h1>
</p>
<br>
<p align="center">
    <img src="https://github.com/user-attachments/assets/c4615101-d932-4e79-8a08-f50fbc686e3b" alt="Alt text" />
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

Pydoll is a specialized Python library engineered for Chromium-based browser automation that eliminates the need for webdriver dependencies while delivering more realistic browser interactions. Built on the foundations laid by Selenium and Puppeteer, it fully embraces Python's asynchronous programming paradigm, resulting in superior performance metrics. The library excels in advanced features such as event capture systems and concurrent web scraping capabilities, making it a powerful tool for modern web automation tasks.


## Table of Contents

- [Basic Usage](#basic-usage)
- [Features](#features)
    - [Browser](#browser)
    - [Page](#page)
    - [WebElement](#webelement)
    - [Events](#events)
    - [Scraping multiple pages concurrently](#scraping-multiple-pages-concurrently)
    - [Proxy support](#proxy-support)


## Basic Usage

In this section, we will demonstrate some basic usage of Pydoll. First, we will install the library using pip:

```bash
pip install git+https://github.com/thalissonvs/pydoll.git
```

Now, let's create a simple script that opens a browser and navigates to a website:

```python
import asyncio
from pydoll.browser.chrome import Chrome

async def main():
    async with Chrome() as browser:
        await browser.start()
        page = await browser.get_page()
        await page.go_to('https://example.com')
        url = await page.current_url
        print(url)

asyncio.run(main())
```

Let's interact with the page by clicking on a button:

```python
import asyncio
from pydoll.browser.chrome import Chrome
from pydoll.constants import By

async def main():
    async with Chrome() as browser:
        await browser.start()
        page = await browser.get_page()
        await page.go_to('https://example.com')
        button = await page.find_element(By.CSS, 'button')
        await button.click()

asyncio.run(main())
```

If you want to specify the browser's options, you can simply do the following:

```python
import asyncio
from pydoll.browser.chrome import Chrome
from pydoll.browser.options import Options

async def main():
    options = Options()
    options.add_argument('--headless')
    options.binary_location = '/path/to/chrome'
    async with Chrome(options=options) as browser:
        await browser.start()
        page = await browser.get_page()
        await page.go_to('https://example.com')

asyncio.run(main())
```

You can find the available options arguments [here](https://peter.sh/experiments/chromium-command-line-switches/).

## Features

Pydoll provides tree main interfaces to interact with: `Browser`,
which handles the browser actions, like opening a new tab, close, resize, etc;
`Page`, which handles the page actions, like navigating to a URL, clicking on
elements, etc; and `WebElement`, which handles the element actions, like clicking,
typing, etc.

Let's see some of the features of each interface.

### Browser

As mentioned earlier, the `Browser` interface is responsible for handling the browser actions. You can open a new tab, close, resize, etc. Let's see some examples:

```python
import asyncio
from pydoll.browser.chrome import Chrome

async def main():
    async with Chrome() as browser:
        await browser.start()
        await browser.set_download_path('/path/to/download')
        await browser.set_window_maximized()
        page_one = await browser.get_page()
        page_two = await browser.get_page()
        cookies = await browser.get_cookies()

asyncio.run(main())
```

An important thing to note is that the `Browser` interface has a global context, which means that all the pages share the same context. This means that if you set a cookie in one page, it will be available in all the other pages.

If you want to, for example, set a cookie only in one page, you must use the `Page` interface.

You can see all the available methods in the `Browser` interface [here](./pydoll/browser/base.py).

### Page

The `Page` interface is responsible for handling the page actions. You can navigate to a URL, refresh, set cookies, get screenshot, etc. Let's see some examples:

```python
import asyncio
from pydoll.browser.chrome import Chrome

async def main():
    async with Chrome() as browser:
        await browser.start()
        page = await browser.get_page()
        await page.go_to('https://example.com')
        await page.refresh()
        await page.get_screenshot('/path/to/screenshot.png')
        await page.set_cookies([{'name': 'name', 'value': 'value'}])

asyncio.run(main())
```

The `Page` interface has a individual context, which means that all the actions you do in one page will not affect the other pages. For example, you can set a cookie in one page and it will not be available in the other pages. You can also enable events in one page and it will not affect the other pages. We will see more about events in the next section.

You can see all the available methods in the `Page` interface [here](./pydoll/browser/page.py).


### WebElement

The `WebElement` interface is responsible for handling the element actions. You can click, type, get the text, etc. Let's see some examples:

```python
import asyncio
from pydoll.browser.chrome import Chrome
from pydoll.constants import By

async def main():
    async with Chrome() as browser:
        await browser.start()
        page = await browser.get_page()
        await page.go_to('https://example.com')
        input_area = await page.find_element(By.CSS, 'input')
        await input_area.click()
        await input_area.send_keys('Hello, World!')
        text = await input_area.get_element_text()
        value = input_area.get_attribute('value')

asyncio.run(main())
```

The `find_element` method returns another `WebElement` object, which means that you can chain the methods. You can use an element to find another element and so on.

You can see all the available methods in the `WebElement` interface [here](./pydoll/element.py).


### Events

Pydoll provides an event system that allows you to capture events that occur in the page. You can register a callback function to be called when an event occurs. Let's see an example:

```python
import asyncio
from pydoll.browser.chrome import Chrome
from pydoll.events.page import PageEvents

async def main():
    async with Chrome() as browser:
        await browser.start()
        page = await browser.get_page()
        await page.go_to('https://example.com')
        await page.enable_page_events()
        await page.on(PageEvents.PAGE_LOADED, lambda: print('Page loaded'))

asyncio.run(main())
```

In this example, always when the page is loaded, the message 'Page loaded' will be printed. The events are divided into domains, like `PageEvents`, `NetworkEvents`, etc. 

Using events is a powerful way to interact with the page. For example, you can use the `NetworkEvents.REQUEST_WILL_BE_SENT` event to capture all the requests that are being sent by the page and modify them before they are sent. This is just one example, there are many other possibilities. You can see all the available events in the `events` folder.


### Scraping multiple pages concurrently

Pydoll provides a way to scrape multiple pages concurrently. Let's see an example:

```python
import asyncio
from pydoll.browser.chrome import Chrome
from pydoll.constants import By
from pydoll.events.page import PageEvents

async def scrape_page(event, page):
    await page.go_to('https://example.com')
    title = await page.get_title()
    return title

async def main():
    async with Chrome() as browser:
        await browser.start()
        page_one = await browser.get_page()
        page_two = await browser.get_page()
        
        await page_one.enable_page_events()
        await page_two.enable_page_events()

        await page_one.on(PageEvents.PAGE_LOADED, lambda event: scrape_page(event, page_one))
        await page_two.on(PageEvents.PAGE_LOADED, lambda event: scrape_page(event, page_two))

        await asyncio.gather(
            page_one.go_to('https://example.com'),
            page_two.go_to('https://example.com')
        )

asyncio.run(main())
```

In this example, we are scraping two pages concurrently. We are using the `asyncio.gather` function to run the `go_to` method of both pages concurrently. Also, we are using the `on` method to register a callback function to be called when the page is loaded. The callback function is the `scrape_page` function, which receives the event and the page as arguments. The `scrape_page` function navigates to the page and gets the title. The `scrape_page` function is called concurrently for both pages.

### Proxy support

Pydoll provides a way to use private proxies (with authentication) and public proxies. You don't need to worry about the proxy authentication, Pydoll will handle it for you. Let's see an example:

```python
import asyncio
from pydoll.browser.chrome import Chrome
from pydoll.browser.options import Options

async def main():
    options = Options()
    options.add_argument('--proxy-server=http://username:password@ip:port')
    async with Chrome(options=options) as browser:
        await browser.start()
        page = await browser.get_page()
        await page.go_to('https://example.com')

asyncio.run(main())
```

As you can see, you just need to add the `--proxy-server` argument to the options. You can use public proxies as well, you just need to remove the `username:password` part.

This is just some of the features of Pydoll. Unbrace the full potential of Pydoll by exploring the library's documentation and experimenting with its capabilities.
