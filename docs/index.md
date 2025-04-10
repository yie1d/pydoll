<p align="center">
    <img src="https://github.com/user-attachments/assets/c4615101-d932-4e79-8a08-f50fbc686e3b" alt="Alt text" /> <br><br>
</p>

<p align="center">
    <a href="https://codecov.io/gh/autoscrape-labs/pydoll">
        <img src="https://codecov.io/gh/autoscrape-labs/pydoll/graph/badge.svg?token=40I938OGM9"/> 
    </a>
    <img src="https://github.com/thalissonvs/pydoll/actions/workflows/tests.yml/badge.svg" alt="Tests">
    <img src="https://github.com/thalissonvs/pydoll/actions/workflows/ruff-ci.yml/badge.svg" alt="Ruff CI">
    <img src="https://github.com/thalissonvs/pydoll/actions/workflows/release.yml/badge.svg" alt="Release">
</p>


# Welcome to Pydoll

Hey there! Thanks for checking out Pydoll, the next generation of browser automation for Python. If you're tired of wrestling with webdrivers and looking for a smoother, more reliable way to automate browsers, you're in the right place.

## What is Pydoll?

Pydoll is revolutionizing browser automation by **eliminating the need for webdrivers** completely! Unlike other solutions that rely on external dependencies, Pydoll connects directly to browsers using their DevTools Protocol, providing a seamless and reliable automation experience with native asynchronous performance.

Whether you're scraping data, testing web applications, or automating repetitive tasks, Pydoll makes it surprisingly easy with its intuitive API and powerful features.

## Installation

Create and activate a [virtual environment](https://docs.python.org/3/tutorial/venv.html) first, then install Pydoll:

<div class="termy">
```bash
$ pip install pydoll-python

---> 100%
```
</div>

For the latest development version, you can install directly from GitHub:

```bash
$ pip install git+https://github.com/autoscrape-labs/pydoll.git
```

## Why Choose Pydoll?

- **Zero Webdrivers**: Say goodbye to compatibility nightmares and flaky connections
- **Native Captcha Bypass**: Smoothly handles Cloudflare Turnstile and reCAPTCHA v3
- **Async Performance**: Lightning-fast operations with Python's asyncio
- **Human-like Interactions**: Realistic browsing patterns that avoid detection
- **Powerful Event System**: React to browser events in real-time
- **Multi-browser Support**: Works with Chrome and Edge (more coming soon!)

Ready to dive in? The following pages will guide you through installation, basic usage, and advanced features to help you get the most out of Pydoll.

Let's start automating the web, the right way! 🚀

## Quick Start Guide: A simple example

Let's start with a practical example. The following script will open the Pydoll GitHub repository and star it:

```python
import asyncio
import time
from pydoll.browser.chrome import Chrome
from pydoll.constants import By

async def main():
    async with Chrome() as browser:
        await browser.start()
        page = await browser.get_page()
        await page.go_to('https://github.com/autoscrape-labs/pydoll')
        star_button = await page.wait_element(
            By.XPATH, '//form[@action="/autoscrape-labs/pydoll/star"]//button',
            timeout=5,
            raise_exc=False
        )
        if not star_button:
            print("Ops! The button was not found.")
            return

        await star_button.click()
        await asyncio.sleep(3)

asyncio.run(main())
```

This example demonstrates how to navigate to a website, wait for an element to appear, and interact with it. You can adapt this pattern to automate many different web tasks.

??? note "Or use without context manager..."
    If you prefer not to use the context manager pattern, you can manually manage the browser instance:
    
    ```python
    import asyncio
    from pydoll.browser.chrome import Chrome
    from pydoll.constants import By
    
    async def main():
        browser = Chrome()
        await browser.start()
        page = await browser.get_page()
        await page.go_to('https://github.com/autoscrape-labs/pydoll')
        star_button = await page.wait_element(
            By.XPATH, '//form[@action="/autoscrape-labs/pydoll/star"]//button',
            timeout=5,
            raise_exc=False
        )
        if not star_button:
            print("Ops! The button was not found.")
            return

        await star_button.click()
        await asyncio.sleep(3)
        await browser.stop()
    
    asyncio.run(main())
    ```
    
    Note that when not using the context manager, you'll need to explicitly call `browser.stop()` to release resources.

## Extended Example: Custom Browser Configuration

For more advanced usage scenarios, Pydoll allows you to customize your browser configuration using the `Options` class. This is useful when you need to:

- Run in headless mode (no visible browser window)
- Specify a custom browser executable path
- Configure proxies, user agents, or other browser settings
- Set window dimensions or startup arguments

Here's an example showing how to use custom options for Chrome:

```python hl_lines="8-12 30-32 34-38"
import asyncio
import os
from pydoll.browser.chrome import Chrome
from pydoll.browser.options import Options
from pydoll.constants import By

async def main():
    options = Options()
    options.binary_location = '/usr/bin/google-chrome-stable'
    options.add_argument('--headless=new')
    options.add_argument('--start-maximized')
    options.add_argument('--disable-notifications')
    
    async with Chrome(options=options) as browser:
        await browser.start()
        page = await browser.get_page()
        await page.go_to('https://github.com/autoscrape-labs/pydoll')
        star_button = await page.wait_element(
            By.XPATH, '//form[@action="/autoscrape-labs/pydoll/star"]//button',
            timeout=5,
            raise_exc=False
        )
        if not star_button:
            print("Ops! The button was not found.")
            return

        await star_button.click()
        await asyncio.sleep(3)

        screenshot_path = os.path.join(os.getcwd(), 'pydoll_repo.png')
        await page.get_screenshot(screenshot_path)
        print(f"Screenshot saved to: {screenshot_path}")

        repo_description_element = await page.find_element(
            By.CLASS_NAME, 'f4.my-3'
        )
        repo_description = await repo_description_element.text
        print(f"Repository description: {repo_description}")

if __name__ == "__main__":
    asyncio.run(main())
```

This extended example demonstrates:

1. Creating and configuring browser options
2. Setting a custom Chrome binary path
3. Enabling headless mode for invisible operation
4. Setting additional browser flags
5. Taking screenshots (especially useful in headless mode)

??? info "About Chromium Options"
    The `options.add_argument()` method allows you to pass any Chromium command-line argument to customize browser behavior. There are hundreds of available options to control everything from networking to rendering behavior.
    
    Common Chrome Options
    
    ```python
    # Performance & Behavior Options
    options.add_argument('--headless=new')         # Run Chrome in headless mode
    options.add_argument('--disable-gpu')          # Disable GPU hardware acceleration
    options.add_argument('--no-sandbox')           # Disable sandbox (use with caution)
    options.add_argument('--disable-dev-shm-usage') # Overcome limited resource issues
    
    # Appearance Options
    options.add_argument('--start-maximized')      # Start with maximized window
    options.add_argument('--window-size=1920,1080') # Set specific window size
    options.add_argument('--hide-scrollbars')      # Hide scrollbars
    
    # Network Options
    options.add_argument('--proxy-server=socks5://127.0.0.1:9050') # Use proxy
    options.add_argument('--disable-extensions')   # Disable extensions
    options.add_argument('--disable-notifications') # Disable notifications
    
    # Privacy & Security
    options.add_argument('--incognito')            # Run in incognito mode
    options.add_argument('--disable-infobars')     # Disable infobars
    ```
    
    Complete Reference Guides
    
    For a comprehensive list of all available Chrome command-line arguments, refer to these resources:
    
    - [Chromium Command Line Switches](https://peter.sh/experiments/chromium-command-line-switches/) - Complete reference list
    - [Chrome Flags](chrome://flags) - Enter this in your Chrome browser address bar to see experimental features
    - [Chromium Source Code Flags](https://source.chromium.org/chromium/chromium/src/+/main:chrome/common/chrome_switches.cc) - Direct source code reference
    
    Remember that some options may behave differently across Chrome versions, so it's a good practice to test your configuration when upgrading Chrome.

With these configurations, you can run Pydoll in various environments, including CI/CD pipelines, servers without displays, or Docker containers.

Continue reading the documentation to explore Pydoll's powerful features for handling captchas, working with multiple tabs, interacting with elements, and more.

## Minimal Dependencies

One of Pydoll's advantages is its lightweight footprint. Unlike other browser automation tools that require numerous dependencies, Pydoll is intentionally designed to be minimalist while maintaining powerful capabilities.

### Core Dependencies

Pydoll relies on just a few carefully selected packages:

```
python = "^3.10"
websockets = "^13.1"
aiohttp = "^3.9.5"
aiofiles = "^23.2.1"
bs4 = "^0.0.2"
```

That's it! This minimal dependency approach means:

- **Faster installation** - No complex dependency tree to resolve
- **Fewer conflicts** - Reduced chance of version conflicts with other packages
- **Smaller footprint** - Lower disk space usage
- **Better security** - Smaller attack surface and dependency-related vulnerabilities
- **Easier updates** - Simpler maintenance and fewer breaking changes

The small number of dependencies also contributes to Pydoll's reliability and performance, as there are fewer external factors that could impact its operation.

## License

Pydoll is released under the MIT License, which gives you the freedom to use, modify, and distribute the code with minimal restrictions. This permissive license makes Pydoll suitable for both personal and commercial projects.

??? info "View Full MIT License Text"
    ```
    MIT License
    
    Copyright (c) 2023 Pydoll Contributors
    
    Permission is hereby granted, free of charge, to any person obtaining a copy
    of this software and associated documentation files (the "Software"), to deal
    in the Software without restriction, including without limitation the rights
    to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
    copies of the Software, and to permit persons to whom the Software is
    furnished to do so, subject to the following conditions:
    
    The above copyright notice and this permission notice shall be included in all
    copies or substantial portions of the Software.
    
    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
    IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
    FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
    AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
    LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
    OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
    SOFTWARE.
    ```
