<p align="center">
    <img src="https://github.com/user-attachments/assets/219f2dbc-37ed-4aea-a289-ba39cdbb335d" alt="Pydoll Logo" /> <br><br>
</p>

<p align="center">
    <a href="https://codecov.io/gh/autoscrape-labs/pydoll">
        <img src="https://codecov.io/gh/autoscrape-labs/pydoll/graph/badge.svg?token=40I938OGM9"/> 
    </a>
    <img src="https://github.com/thalissonvs/pydoll/actions/workflows/tests.yml/badge.svg" alt="Tests">
    <img src="https://github.com/thalissonvs/pydoll/actions/workflows/ruff-ci.yml/badge.svg" alt="Ruff CI">
    <img src="https://github.com/thalissonvs/pydoll/actions/workflows/release.yml/badge.svg" alt="Release">
    <img src="https://github.com/thalissonvs/pydoll/actions/workflows/mypy.yml/badge.svg" alt="MyPy CI">
</p>

<p align="center">
  <a href="https://autoscrape-labs.github.io/pydoll/">Documentation</a> •
  <a href="#getting-started">Getting Started</a> •
  <a href="#advanced-features">Advanced Features</a> •
  <a href="#contributing">Contributing</a> •
  <a href="#support-my-work">Support</a> •
  <a href="#license">License</a>
</p>


## Why Pydoll Exists

Picture this: you need to automate browser tasks. Maybe it's testing your web application, scraping data from websites, or automating repetitive processes. Traditionally, this meant dealing with external drivers, complex configurations, and a host of compatibility issues that seemed to appear out of nowhere.

**Pydoll was born to change that.**

Built from the ground up with a different philosophy, Pydoll connects directly to the Chrome DevTools Protocol (CDP), eliminating the need for external drivers entirely. This isn't just a technical change - it's a revolution in how you interact with browsers through Python.

We believe that powerful automation shouldn't require you to become a configuration expert. With Pydoll, you focus on what matters: your automation logic, not the underlying complexity.

## What Makes Pydoll Special

**Genuine Simplicity**: We don't want you wasting time configuring drivers or dealing with compatibility issues. With Pydoll, you install and you're ready to automate.

**Truly Human Interactions**: Our algorithms simulate real human behavior patterns - from timing between clicks to how the mouse moves across the screen.

**Native Async Performance**: Built from the ground up with `asyncio`, Pydoll doesn't just support asynchronous operations - it was designed for them.

**Integrated Intelligence**: Automatic bypass of Cloudflare Turnstile and reCAPTCHA v3 captchas, without external services or complex configurations.

**Powerful Network Monitoring**: Intercept, modify, and analyze all network traffic with ease, giving you complete control over requests.

**Event-Driven Architecture**: React to page events, network requests, and user interactions in real-time.

**Intuitive Element Finding**: Modern `find()` and `query()` methods that make sense and work as you'd expect.

**Robust Type Safety**: Comprehensive type system for better IDE support and error prevention.

## Installation

```bash
pip install pydoll-python
```

That's it. No drivers to download, no complex configurations. Just install and start automating.

## Getting Started

### Your First Automation

Let's start with something simple. The code below opens a browser, navigates to a website, and interacts with elements:

```python
import asyncio
from pydoll.browser import Chrome

async def my_first_automation():
    # Create a browser instance
    async with Chrome() as browser:
        # Start the browser and get a tab
        tab = await browser.start()
        
        # Navigate to a website
        await tab.go_to('https://example.com')
        
        # Find elements intuitively
        button = await tab.find(tag_name='button', class_name='submit')
        await button.click()
        
        # Or use CSS selectors/XPath directly
        link = await tab.query('a[href*="contact"]')
        await link.click()

# Run the automation
asyncio.run(my_first_automation())
```

### Custom Configuration

Sometimes you need more control. Pydoll offers flexible configuration options:

```python
from pydoll.browser import Chrome
from pydoll.browser.options import ChromiumOptions

async def custom_automation():
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
        
        # The browser is now using your custom settings

asyncio.run(custom_automation())
```

## Advanced Features

### Intelligent Captcha Bypass

One of Pydoll's most impressive features is its ability to automatically handle Cloudflare Turnstile captchas. This means fewer interruptions and smoother automations:

```python
import asyncio
from pydoll.browser import Chrome

async def bypass_cloudflare():
    async with Chrome() as browser:
        tab = await browser.start()
        
        # Method 1: Context manager (waits for captcha completion)
        async with tab.expect_and_bypass_cloudflare_captcha():
            await tab.go_to('https://site-with-cloudflare.com')
            print("Captcha automatically solved!")
        
        # Method 2: Background processing
        await tab.enable_auto_solve_cloudflare_captcha()
        await tab.go_to('https://another-protected-site.com')
        # Captcha solved in background while code continues
        
        await tab.disable_auto_solve_cloudflare_captcha()

asyncio.run(bypass_cloudflare())
```


### Advanced Element Finding

Pydoll offers multiple intuitive ways to find elements. No matter how you prefer to work, we have an approach that makes sense for you:

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

One of the great advantages of Pydoll's asynchronous design is the ability to process multiple tasks simultaneously:

```python
import asyncio
from pydoll.browser import Chrome

async def scrape_page(url):
    """Extract data from a single page"""
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
    
    # Process all URLs simultaneously
    tasks = [scrape_page(url) for url in urls]
    results = await asyncio.gather(*tasks)
    
    for result in results:
        print(f"{result['url']}: {result['title']} ({result['link_count']} links)")

asyncio.run(concurrent_scraping())
```

### Event-Driven Automation

React to page events and user interactions in real-time. This enables more sophisticated and responsive automations:

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
            search_box = await tab.find(id='search-box')
            await search_box.type('automation')
        
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

Pydoll provides seamless iframe interaction through the `get_frame()` method. This is especially useful for dealing with embedded content:

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

## The Philosophy Behind Pydoll

Pydoll isn't just another automation library. It represents a different approach to solving real problems that developers face daily.

**Simplicity Without Sacrificing Power**: We believe that powerful tools don't need to be complex. Pydoll offers advanced functionality through a clean and intuitive API.

**Performance That Matters**: In a world where every millisecond counts, Pydoll's native asynchronous design ensures your automations are not just functional, but efficient.

**Constant Evolution**: The web ecosystem is always changing, and Pydoll evolves with it. New challenges like advanced captchas are met with innovative solutions integrated into the library.

## Documentation

For comprehensive documentation, detailed examples, and deep dives into Pydoll's features, visit our [official documentation site](https://autoscrape-labs.github.io/pydoll/).

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
- Starring the repo
- Sharing it on social media
- Writing blog posts or tutorials
- Giving feedback or reporting issues

Every bit of support makes a difference — thank you!

## License

Pydoll is licensed under the [MIT License](LICENSE).

<p align="center">
  <b>Pydoll</b> — Making browser automation magical!
</p>
