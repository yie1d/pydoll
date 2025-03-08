
<p align="center">
    <h1>🚀 Pydoll: Async Web Automation in Python!</h1>
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


Pydoll is an innovative Python library that's redefining Chromium browser automation! Unlike other solutions, Pydoll **completely eliminates the need for webdrivers**, providing a much more fluid and reliable automation experience.

## ⭐ Extraordinary Features

- **Zero Webdrivers!** Say goodbye to webdriver compatibility and configuration headaches
- **Native Captcha Bypass!** Naturally passes through Cloudflare Turnstile and reCAPTCHA v3
- **Performance** thanks to native asynchronous programming
- **Realistic Interactions** that simulate human behavior
- **Advanced Event System** for complex and reactive automations

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

## 🔥 Installation

```bash
pip install git+https://github.com/thalissonvs/pydoll.git
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

Powerful interface for global browser control:

```python
async def browser_examples():
    async with Chrome() as browser:
        await browser.start()
        # Control multiple pages with incredible ease
        pages = [await browser.get_page() for _ in range(3)]
        
        # Advanced settings with a simple command
        await browser.set_window_maximized()
```

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
