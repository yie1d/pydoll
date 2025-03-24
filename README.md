<p align="center">
    <h1>🚀 Pydoll: Async Web Automation in Python!</h1>
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

<p align="center">
  <b>Pydoll</b> is revolutionizing browser automation! Unlike other solutions, it <b>eliminates the need for webdrivers</b>, 
  providing a smooth and reliable automation experience with native asynchronous performance.
</p>

<p align="center">
  <a href="#-installation">Installation</a> •
  <a href="#-quick-start">Quick Start</a> •
  <a href="#-core-components">Core Components</a> •
  <a href="#-whats-new">What's New</a> •
  <a href="#-advanced-features">Advanced Features</a>
</p>

## ✨ Key Features

🔹 **Zero Webdrivers!** Say goodbye to webdriver compatibility nightmares  
🔹 **Native Captcha Bypass!** Smoothly handles Cloudflare Turnstile and reCAPTCHA v3*  
🔹 **Async Performance** for lightning-fast automation  
🔹 **Human-like Interactions** that mimic real user behavior  
🔹 **Powerful Event System** for reactive automations  
🔹 **Multi-browser Support** including Chrome and Edge

> *Note: For Cloudflare captcha, click the checkbox by finding the div containing the iframe and using the `.click()` method. Automatic detection coming soon!

## 🔥 Installation

```bash
pip install pydoll-python
```

## ⚡ Quick Start

Get started with just a few lines of code:

```python
import asyncio
from pydoll.browser.chrome import Chrome
from pydoll.constants import By

async def main():
    async with Chrome() as browser:
        await browser.start()
        page = await browser.get_page()
        
        # Works with captcha-protected sites
        await page.go_to('https://example-with-cloudflare.com')
        button = await page.find_element(By.CSS_SELECTOR, 'button')
        await button.click()

asyncio.run(main())
```

Need to configure your browser? Easy!

```python
from pydoll.browser.chrome import Chrome
from pydoll.browser.options import Options

options = Options()
# Add a proxy
options.add_argument('--proxy-server=username:password@ip:port')
# Custom browser location
options.binary_location = '/path/to/your/browser'

async with Chrome(options=options) as browser:
    await browser.start()
    # Your code here
```

## 🎉 What's New

Version 1.4.0 comes packed with amazing new features:

### 🔤 Advanced Keyboard Control

Full keyboard simulation thanks to [@cleitonleonel](https://github.com/cleitonleonel):

```python
import asyncio
from pydoll.browser.chrome import Chrome
from pydoll.browser.options import Options
from pydoll.common.keys import Keys
from pydoll.constants import By

async def main():
    async with Chrome() as browser:
        await browser.start()
        page = await browser.get_page()
        await page.go_to('https://example.com')
        
        input_field = await page.find_element(By.CSS_SELECTOR, 'input')
        await input_field.click()
        
        # Realistic typing with customizable speed
        await input_field.type_keys("hello@example.com", interval=0.2)
        
        # Special key combinations
        await input_field.key_down(Keys.SHIFT)
        await input_field.send_keys("UPPERCASE")
        await input_field.key_up(Keys.SHIFT)
        
        # Navigation keys
        await input_field.send_keys(Keys.ENTER)
        await input_field.send_keys(Keys.PAGEDOWN)

asyncio.run(main())
```

### 📁 File Upload Support

[@yie1d](https://github.com/yie1d) brings seamless file uploads:

```python
# For input elements
file_input = await page.find_element(By.XPATH, '//input[@type="file"]')
await file_input.set_input_files('path/to/file.pdf')  # Single file
await file_input.set_input_files(['file1.pdf', 'file2.jpg'])  # Multiple files

# For other elements using the file chooser
async with page.expect_file_chooser(files='path/to/file.pdf'):
    upload_button = await page.find_element(By.ID, 'upload-button')
    await upload_button.click()
```

### 🌐 Microsoft Edge Support

Now with Edge browser support thanks to [@Harris-H](https://github.com/Harris-H):

```python
import asyncio
from pydoll.browser import Edge
from pydoll.browser.options import EdgeOptions

async def main():
    options = EdgeOptions()
    # options.add_argument('--headless')
    
    async with Edge(options=options) as browser:
        await browser.start()
        page = await browser.get_page()
        await page.go_to('https://example.com')

asyncio.run(main())
```

## 🎯 Core Components

Pydoll offers three main interfaces for browser automation:

### Browser Interface

The Browser interface provides global control over the entire browser instance:

```python
async def browser_demo():
    async with Chrome() as browser:
        await browser.start()
        
        # Create multiple pages
        pages = [await browser.get_page() for _ in range(3)]
        
        # Control the browser window
        await browser.set_window_maximized()
        
        # Manage cookies globally
        await browser.set_cookies([{
            'name': 'session',
            'value': '12345',
            'domain': 'example.com'
        }])
```

#### Key Browser Methods

| Method | Description | Example |
|--------|-------------|---------|
| `async start()` | 🔥 Launch your browser and prepare for automation | `await browser.start()` |
| `async stop()` | 👋 Close the browser gracefully when finished | `await browser.stop()` |
| `async get_page()` | ✨ Get an existing page or create a new one | `page = await browser.get_page()` |
| `async new_page(url='')` | 🆕 Create a new page in the browser | `page_id = await browser.new_page()` |
| `async get_page_by_id(page_id)` | 🔍 Find and control a specific page by ID | `page = await browser.get_page_by_id(id)` |
| `async get_targets()` | 🎯 List all open pages in the browser | `targets = await browser.get_targets()` |
| `async set_window_bounds(bounds)` | 📐 Size and position the browser window | `await browser.set_window_bounds({'width': 1024})` |
| `async set_window_maximized()` | 💪 Maximize the browser window | `await browser.set_window_maximized()` |
| `async get_cookies()` | 🍪 Get all browser cookies | `cookies = await browser.get_cookies()` |
| `async set_cookies(cookies)` | 🧁 Set custom cookies for authentication | `await browser.set_cookies([{...}])` |
| `async delete_all_cookies()` | 🧹 Clear all cookies for a fresh state | `await browser.delete_all_cookies()` |
| `async set_download_path(path)` | 📂 Configure where downloaded files are saved | `await browser.set_download_path('/downloads')` |

### Page Interface

The Page interface lets you control individual browser tabs and interact with web content:

```python
async def page_demo():
    page = await browser.get_page()
    
    # Navigation
    await page.go_to('https://example.com')
    await page.refresh()
    
    # Get page info
    url = await page.current_url
    html = await page.page_source
    
    # Screenshots and PDF
    await page.get_screenshot('screenshot.png')
    await page.print_to_pdf('page.pdf')
    
    # Execute JavaScript
    title = await page.execute_script('return document.title')
```

#### Key Page Methods

| Method | Description | Example |
|--------|-------------|---------|
| `async go_to(url, timeout=300)` | 🚀 Navigate to a URL with loading detection | `await page.go_to('https://example.com')` |
| `async refresh()` | 🔄 Reload the current page | `await page.refresh()` |
| `async close()` | 🚪 Close the current tab | `await page.close()` |
| `async current_url` | 🧭 Get the current page URL | `url = await page.current_url` |
| `async page_source` | 📝 Get the page's HTML content | `html = await page.page_source` |
| `async get_screenshot(path)` | 📸 Save a screenshot of the page | `await page.get_screenshot('shot.png')` |
| `async print_to_pdf(path)` | 📄 Convert the page to a PDF document | `await page.print_to_pdf('page.pdf')` |
| `async has_dialog()` | 🔔 Check if a dialog is present | `if await page.has_dialog():` |
| `async accept_dialog()` | 👍 Dismiss alert and confirmation dialogs | `await page.accept_dialog()` |
| `async execute_script(script, element)` | ⚡ Run JavaScript code on the page | `await page.execute_script('alert("Hi!")')` |
| `async get_network_logs(matches=[])` | 🕸️ Monitor network requests | `logs = await page.get_network_logs()` |
| `async find_element(by, value)` | 🔎 Find an element on the page | `el = await page.find_element(By.ID, 'btn')` |
| `async find_elements(by, value)` | 🔍 Find multiple elements matching a selector | `items = await page.find_elements(By.CSS, 'li')` |
| `async wait_element(by, value, timeout=10)` | ⏳ Wait for an element to appear | `await page.wait_element(By.ID, 'loaded', 5)` |

### WebElement Interface

The WebElement interface provides methods to interact with DOM elements:

```python
async def element_demo():
    # Find elements
    button = await page.find_element(By.CSS_SELECTOR, 'button.submit')
    input_field = await page.find_element(By.ID, 'username')
    
    # Get properties
    button_text = await button.get_element_text()
    is_button_enabled = button.is_enabled
    input_value = input_field.value
    
    # Interact with elements
    await button.scroll_into_view()
    await input_field.type_keys("user123")
    await button.click()
```

#### Key WebElement Methods

| Method | Description | Example |
|--------|-------------|---------|
| `value` | 💬 Get the value of an input element | `value = input_field.value` |
| `class_name` | 🎨 Get the element's CSS classes | `classes = element.class_name` |
| `id` | 🏷️ Get the element's ID attribute | `id = element.id` |
| `is_enabled` | ✅ Check if the element is enabled | `if button.is_enabled:` |
| `async bounds` | 📏 Get the element's position and size | `coords = await element.bounds` |
| `async inner_html` | 🧩 Get the element's inner HTML content | `html = await element.inner_html` |
| `async get_element_text()` | 📜 Get the element's text content | `text = await element.get_element_text()` |
| `get_attribute(name)` | 📊 Get any attribute from the element | `href = link.get_attribute('href')` |
| `async scroll_into_view()` | 👁️ Scroll the element into viewport | `await element.scroll_into_view()` |
| `async click(x_offset=0, y_offset=0)` | 👆 Click the element with optional offsets | `await button.click()` |
| `async click_using_js()` | 🔮 Click using JavaScript for hidden elements | `await overlay_button.click_using_js()` |
| `async send_keys(text)` | ⌨️ Send text to input fields | `await input.send_keys("text")` |
| `async type_keys(text, interval=0.1)` | 👨‍💻 Type text with realistic timing | `await input.type_keys("hello", 0.2)` |
| `async get_screenshot(path)` | 📷 Take a screenshot of the element | `await error.get_screenshot('error.png')` |
| `async set_input_files(files)` | 📤 Upload files with file inputs | `await input.set_input_files('file.pdf')` |

## 🚀 Advanced Features

### Event System

Pydoll's powerful event system lets you react to browser events in real-time:

```python
from pydoll.events.page import PageEvents
from pydoll.events.network import NetworkEvents
from functools import partial

# Page navigation events
async def on_page_loaded(event):
    print(f"🌐 Page loaded: {event['params'].get('url')}")

await page.enable_page_events()
await page.on(PageEvents.PAGE_LOADED, on_page_loaded)

# Network request monitoring
async def on_request(page, event):
    url = event['params']['request']['url']
    print(f"🔄 Request to: {url}")

await page.enable_network_events()
await page.on(NetworkEvents.REQUEST_WILL_BE_SENT, partial(on_request, page))

# DOM change monitoring
from pydoll.events.dom import DomEvents
await page.enable_dom_events()
await page.on(DomEvents.DOCUMENT_UPDATED, lambda e: print("DOM updated!"))
```

### Request Interception

Pydoll gives you the power to intercept and modify network requests before they're sent! This allows you to customize headers or modify request data on the fly.

#### Basic Request Modification

The request interception system lets you monitor and modify requests before they're sent:

```python
from pydoll.events.fetch import FetchEvents
from pydoll.commands.fetch import FetchCommands
from functools import partial

async def request_interceptor(page, event):
    request_id = event['params']['requestId']
    url = event['params']['request']['url']
    
    print(f"🔎 Intercepted request to: {url}")
    
    # Continue the request normally
    await page._execute_command(
        FetchCommands.continue_request(
            request_id=request_id
        )
    )

# Enable interception and register your handler
await page.enable_fetch_events()
await page.on(FetchEvents.REQUEST_PAUSED, partial(request_interceptor, page))
```

#### Adding Custom Headers

Inject authentication or tracking headers into specific requests:

```python
async def auth_header_interceptor(page, event):
    request_id = event['params']['requestId']
    url = event['params']['request']['url']
    
    # Only add auth headers to API requests
    if '/api/' in url:
        # Get the original headers
        original_headers = event['params']['request'].get('headers', {})
        
        # Add your custom headers
        custom_headers = {
            **original_headers,
            'Authorization': 'Bearer your-token-123',
            'X-Custom-Track': 'pydoll-automation'
        }
        
        await page._execute_command(
            FetchCommands.continue_request(
                request_id=request_id,
                headers=custom_headers
            )
        )
    else:
        # Continue normally for non-API requests
        await page._execute_command(
            FetchCommands.continue_request(
                request_id=request_id
            )
        )

await page.enable_fetch_events()
await page.on(FetchEvents.REQUEST_PAUSED, partial(auth_header_interceptor, page))
```

#### Modifying Request Body

Change POST data before it's sent:

```python
async def modify_request_body(page, event):
    request_id = event['params']['requestId']
    url = event['params']['request']['url']
    method = event['params']['request'].get('method', '')
    
    # Only modify POST requests to specific endpoints
    if method == 'POST' and 'submit-form' in url:
        # Get original request body if it exists
        original_body = event['params']['request'].get('postData', '{}')
        
        # In a real scenario, you'd parse and modify the body
        # For this example, we're just replacing it
        new_body = '{"modified": true, "data": "enhanced-by-pydoll"}'
        
        print(f"✏️ Modifying POST request to: {url}")
        await page._execute_command(
            FetchCommands.continue_request(
                request_id=request_id,
                post_data=new_body
            )
        )
    else:
        # Continue normally for other requests
        await page._execute_command(
            FetchCommands.continue_request(
                request_id=request_id
            )
        )

await page.enable_fetch_events()
await page.on(FetchEvents.REQUEST_PAUSED, partial(modify_request_body, page))
```

### Filtering Request Types

You can focus on specific types of requests to intercept:

```python
# Just intercept XHR requests
await page.enable_fetch_events(resource_type='xhr')

# Or focus on document requests
await page.enable_fetch_events(resource_type='document')

# Or maybe just images
await page.enable_fetch_events(resource_type='image')
```

Available resource types include: `document`, `stylesheet`, `image`, `media`, `font`, `script`, `texttrack`, `xhr`, `fetch`, `eventsource`, `websocket`, `manifest`, `other`.

### Concurrent Automation

Process multiple pages simultaneously for maximum efficiency:

```python
async def process_page(url):
    page = await browser.get_page()
    await page.go_to(url)
    # Do your scraping or automation here
    return await page.get_element_text()

# Process multiple URLs concurrently
urls = ['https://example1.com', 'https://example2.com', 'https://example3.com']
results = await asyncio.gather(*(process_page(url) for url in urls))
```

## 💡 Best Practices

Maximize your Pydoll experience with these tips:

✅ **Embrace async patterns** throughout your code for best performance  
✅ **Use specific selectors** (IDs, unique attributes) for reliable element finding  
✅ **Implement proper error handling** with try/except blocks around critical operations  
✅ **Leverage the event system** instead of polling for state changes  
✅ **Properly close resources** with async context managers  
✅ **Wait for elements** instead of fixed sleep delays  
✅ **Use realistic interactions** like `type_keys()` to avoid detection  

## 🤝 Contributing

We'd love your help making Pydoll even better! Check out our [contribution guidelines](CONTRIBUTING.md) to get started. Whether it's fixing bugs, adding features, or improving documentation - all contributions are welcome!

Please make sure to:
- Write tests for new features or bug fixes
- Follow coding style and conventions
- Use conventional commits for pull requests
- Run lint and test checks before submitting

## 🔮 Coming Soon

Get ready for these upcoming features in Pydoll:

🔹 **Auto-detection of Cloudflare Captcha** - Automatic solving without manual intervention  
🔹 **Fingerprint Generation & Rotation** - Dynamic browser fingerprints to avoid detection  
🔹 **Proxy Rotation** - Seamless IP switching for extended scraping sessions  
🔹 **Shadow DOM Access** - Navigate and interact with Shadow Root elements  

Stay tuned and star the repository to get updates when these features are released!

## 📄 License

Pydoll is licensed under the [MIT License](LICENSE).

---

<p align="center">
  <b>Pydoll</b> — Making browser automation magical! ✨
</p>
