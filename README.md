<p align="center">
    <h1>Pydoll: Async Web Automation in Python!</h1>
</p>
<br>
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

<p align="center">
  <b>Pydoll</b> is revolutionizing browser automation! Unlike other solutions, it <b>eliminates the need for webdrivers</b>, 
  providing a smooth and reliable automation experience with native asynchronous performance and advanced capabilities 
  like intelligent captcha bypass and comprehensive network monitoring.
</p>

<p align="center">
  <a href="https://autoscrape-labs.github.io/pydoll/">Documentation</a> •
  <a href="#-quick-start">Quick Start</a> •
  <a href="#-breaking-changes">Breaking Changes</a> •
  <a href="#-advanced-features">Advanced Features</a> •
  <a href="#-contributing">Contributing</a> •
  <a href="#-support-my-work">Support</a> •
  <a href="#-license">License</a>
</p>

## What Makes Pydoll Special

Pydoll isn't just another browser automation library. It's a complete solution built from the ground up for modern web automation challenges:

🔹 **Zero Webdrivers!** Direct Chrome DevTools Protocol integration - no more compatibility nightmares  
🔹 **Intelligent Captcha Bypass** - Automatically handles Cloudflare Turnstile and reCAPTCHA v3*  
🔹 **True Async Performance** - Built for speed with native asyncio support  
🔹 **Human-like Interactions** - Advanced timing and behavior patterns that mimic real users  
🔹 **Powerful Network Monitoring** - Intercept, modify, and analyze all network traffic  
🔹 **Event-Driven Architecture** - React to page events, network requests, and user interactions  
🔹 **Multi-browser Support** - Chrome and Edge with consistent APIs  
🔹 **Intuitive Element Finding** - Modern `find()` and `query()` methods for effortless element location  
🔹 **Robust Type Safety** - Comprehensive type system for better IDE support and error prevention

## Installation

```bash
pip install pydoll-python
```

## Breaking Changes (v2.0+)

If you're upgrading from an earlier version, please note these important changes:

### Import Changes
```python
# Old way (deprecated)
from pydoll.browser.options import Options
from pydoll.browser import Chrome, Edge

# New way
from pydoll.browser.options import ChromiumOptions
from pydoll.browser.chromium import Chrome, Edge
```

### Element Finding Methods
```python
# Old way
element = await page.find_element(By.CSS_SELECTOR, 'button')

# New intuitive methods
element = await tab.find(tag_name='button')  # Find by attributes
element = await tab.query('button')         # CSS selector or XPath
```

### Tab-Based Architecture
```python
# Old way
async with Chrome() as browser:
    await browser.start()
    page = await browser.get_page()

# New way - start() returns Tab directly
async with Chrome() as browser:
    tab = await browser.start()  # Returns Tab instance directly
    # or create additional tabs
    new_tab = await browser.new_tab()
```

## Quick Start

### Basic Automation
```python
import asyncio
from pydoll.browser import Chrome
from pydoll.browser.options import ChromiumOptions

async def main():
    # Simple automation
    async with Chrome() as browser:
        tab = await browser.start()  # Returns Tab directly
        
        await tab.go_to('https://example.com')
        
        # Modern element finding
        button = await tab.find(tag_name='button', class_name='submit')
        await button.click()
        
        # Or use CSS selectors/XPath directly
        link = await tab.query('a[href*="contact"]')
        await link.click()

asyncio.run(main())
```

### Custom Browser Configuration
```python
from pydoll.browser import Chrome
from pydoll.browser.options import ChromiumOptions

async def main():
    # Configure browser options
    options = ChromiumOptions()
    options.add_argument('--proxy-server=username:password@ip:port')
    options.add_argument('--window-size=1920,1080')
    options.add_argument('--disable-web-security')
    options.binary_location = '/path/to/your/browser'

    async with Chrome(options=options) as browser:
        tab = await browser.start()
        
        # Your automation code here
        await tab.go_to('https://example.com')

asyncio.run(main())
```

## Advanced Features

### Intelligent Captcha Bypass

Pydoll can automatically handle Cloudflare Turnstile captchas without external services:

```python
import asyncio
from pydoll.browser import Chrome

async def bypass_cloudflare():
    async with Chrome() as browser:
        tab = await browser.start()
        
        # Method 1: Context manager (waits for captcha completion)
        async with tab.expect_and_bypass_cloudflare_captcha():
            await tab.go_to('https://site-with-cloudflare.com')
            print("Captcha automatically handled!")
        
        # Method 2: Background processing
        await tab.enable_auto_solve_cloudflare_captcha()
        await tab.go_to('https://another-protected-site.com')
        # Captcha solved in background while code continues
        
        await tab.disable_auto_solve_cloudflare_captcha()

asyncio.run(bypass_cloudflare())
```

### Advanced Element Finding

Pydoll offers multiple intuitive ways to find elements:

```python
import asyncio
from pydoll.browser import Chrome

async def element_finding_examples():
    async with Chrome() as browser:
        tab = await browser.start()
        await tab.go_to('https://example.com')
        
        # Find by attributes (most intuitive)
        submit_btn = await tab.find(
            tag_name='button',
            class_name='btn-primary',
            text='Submit'
        )
        
        # Find by ID
        username_field = await tab.find(id='username')
        
        # Find multiple elements
        all_links = await tab.find(tag_name='a', find_all=True)
        
        # CSS selectors and XPath
        nav_menu = await tab.query('nav.main-menu')
        specific_item = await tab.query('//div[@data-testid="item-123"]')
        
        # With timeout and error handling
        delayed_element = await tab.find(
            class_name='dynamic-content',
            timeout=10,
            raise_exc=False  # Returns None if not found
        )
        
        # Advanced: Custom attributes
        custom_element = await tab.find(
            data_testid='submit-button',
            aria_label='Submit form'
        )

asyncio.run(element_finding_examples())
```

### Concurrent Automation

Leverage async capabilities for parallel processing:

```python
import asyncio
from pydoll.browser import Chrome

async def scrape_page(url):
    """Scrape a single page"""
    async with Chrome() as browser:
        tab = await browser.start()
        await tab.go_to(url)
        
        title = await tab.execute_script('return document.title')
        links = await tab.find(tag_name='a', find_all=True)
        
        return {
            'url': url,
            'title': title,
            'link_count': len(links)
        }

async def concurrent_scraping():
    urls = [
        'https://example1.com',
        'https://example2.com',
        'https://example3.com'
    ]
    
    # Process all URLs concurrently
    tasks = [scrape_page(url) for url in urls]
    results = await asyncio.gather(*tasks)
    
    for result in results:
        print(f"{result['url']}: {result['title']} ({result['link_count']} links)")

asyncio.run(concurrent_scraping())
```

### Event-Driven Automation

React to page events and user interactions:

```python
import asyncio
from pydoll.browser import Chrome
from pydoll.protocol.page.events import PageEvent

async def event_driven_automation():
    async with Chrome() as browser:
        tab = await browser.start()
        
        # Enable page events
        await tab.enable_page_events()
        
        # React to page load
        async def on_page_load(event):
            print("Page loaded! Starting automation...")
            # Perform actions after page loads
            await tab.find(id='search-box').type('automation')
        
        # React to navigation
        async def on_navigation(event):
            url = event['params']['url']
            print(f"Navigated to: {url}")
        
        await tab.on(PageEvent.LOAD_EVENT_FIRED, on_page_load)
        await tab.on(PageEvent.FRAME_NAVIGATED, on_navigation)
        
        await tab.go_to('https://example.com')
        await asyncio.sleep(5)  # Let events process

asyncio.run(event_driven_automation())
```

### Working with iFrames

Pydoll provides seamless iframe interaction through the `get_frame()` method:

```python
import asyncio
from pydoll.browser.chromium import Chrome

async def iframe_interaction():
    async with Chrome() as browser:
        tab = await browser.start()
        await tab.go_to('https://example.com/page-with-iframe')
        
        # Find the iframe element
        iframe_element = await tab.query('.hcaptcha-iframe', timeout=10)
        
        # Get a Tab instance for the iframe content
        frame = await tab.get_frame(iframe_element)
        
        # Now interact with elements inside the iframe
        submit_button = await frame.find(tag_name='button', class_name='submit')
        await submit_button.click()
        
        # You can use all Tab methods on the frame
        form_input = await frame.find(id='captcha-input')
        await form_input.type('verification-code')
        
        # Find elements by various methods
        links = await frame.find(tag_name='a', find_all=True)
        specific_element = await frame.query('#specific-id')

asyncio.run(iframe_interaction())
```

## Documentation

For comprehensive documentation, examples, and deep dives into Pydoll's features, visit our [official documentation site](https://autoscrape-labs.github.io/pydoll/).

The documentation includes:
- **Getting Started Guide** - Step-by-step tutorials
- **API Reference** - Complete method documentation  
- **Advanced Techniques** - Network interception, event handling, performance optimization
- **Migration Guide** - Upgrading from older versions
- **Troubleshooting** - Common issues and solutions
- **Best Practices** - Patterns for reliable automation

## Contributing

We'd love your help making Pydoll even better! Check out our [contribution guidelines](CONTRIBUTING.md) to get started. Whether it's fixing bugs, adding features, or improving documentation - all contributions are welcome!

Please make sure to:
- Write tests for new features or bug fixes
- Follow coding style and conventions
- Use conventional commits for pull requests
- Run lint and test checks before submitting

## Support My Work

If you find my projects helpful, consider [sponsoring me on GitHub](https://github.com/sponsors/thalissonvs).  
You'll get access to exclusive perks like prioritized support, custom features, and more!

Can't sponsor right now? No problem — you can still help a lot by:
- ⭐ Starring the repo
- 🐦 Sharing it on social media
- 📝 Writing blog posts or tutorials
- 💬 Giving feedback or reporting issues

Every bit of support makes a difference — thank you! 🙌

## 📄 License

Pydoll is licensed under the [MIT License](LICENSE).

---

<p align="center">
  <b>Pydoll</b> — Making browser automation magical! ✨
</p>
