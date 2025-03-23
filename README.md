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
| `async start()` | 🔥 Fire up your browser and get ready for automation magic! | `await browser.start()` |
| `async stop()` | 👋 Gracefully shut down your browser when the mission is complete | `await browser.stop()` |
| `async get_page()` | ✨ Magically grab an existing page or create a fresh one | `page = await browser.get_page()` |
| `async new_page(url='')` | 🆕 Spawn a brand new page with explosive speed | `page_id = await browser.new_page()` |
| `async get_page_by_id(page_id)` | 🔍 Find and control any specific page with pinpoint precision | `page = await browser.get_page_by_id(id)` |
| `async get_targets()` | 🎯 Discover all open pages - perfect for multi-tab wizardry | `targets = await browser.get_targets()` |
| `async set_window_bounds(bounds)` | 📐 Reshape your browser window exactly how you want it | `await browser.set_window_bounds({'width': 1024})` |
| `async set_window_maximized()` | 💪 Make your browser take up the entire screen with one command | `await browser.set_window_maximized()` |
| `async get_cookies()` | 🍪 Peek into all cookies for ultimate session control | `cookies = await browser.get_cookies()` |
| `async set_cookies(cookies)` | 🧁 Set up custom cookies for instant authentication | `await browser.set_cookies([{...}])` |
| `async delete_all_cookies()` | 🧹 Wipe cookies clean for a fresh browsing experience | `await browser.delete_all_cookies()` |
| `async set_download_path(path)` | 📂 Tell your browser exactly where to save your precious files | `await browser.set_download_path('/downloads')` |

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
| `async go_to(url, timeout=300)` | 🚀 Blast off to any URL with intelligent loading detection | `await page.go_to('https://example.com')` |
| `async refresh()` | 🔄 Refresh your page with a single command - instant content updates! | `await page.refresh()` |
| `async close()` | 🚪 Close the current tab while keeping your browser alive | `await page.close()` |
| `async current_url` | 🧭 Instantly know exactly where you are in your automation journey | `url = await page.current_url` |
| `async page_source` | 📝 Grab the complete HTML with one magical command | `html = await page.page_source` |
| `async get_screenshot(path)` | 📸 Capture visual evidence of your automation conquests | `await page.get_screenshot('shot.png')` |
| `async print_to_pdf(path)` | 📄 Transform any page into a beautiful PDF document | `await page.print_to_pdf('page.pdf')` |
| `async has_dialog()` | 🔔 Never be surprised by unexpected alerts again | `if await page.has_dialog():` |
| `async accept_dialog()` | 👍 Make those pesky dialogs disappear with one command | `await page.accept_dialog()` |
| `async execute_script(script, element)` | ⚡ Unleash the full power of JavaScript directly from Python | `await page.execute_script('alert("Hi!")')` |
| `async get_network_logs(matches=[])` | 🕸️ See exactly what requests your page is making behind the scenes | `logs = await page.get_network_logs()` |
| `async find_element(by, value)` | 🔎 Find any element with laser-like precision | `el = await page.find_element(By.ID, 'btn')` |
| `async find_elements(by, value)` | 🔍 Gather multiple elements in one swoop | `items = await page.find_elements(By.CSS, 'li')` |
| `async wait_element(by, value, timeout=10)` | ⏳ Intelligently wait for elements to appear - no more sleeps! | `await page.wait_element(By.ID, 'loaded', 5)` |

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
| `value` | 💬 Get the current value of any input - perfect for validation | `value = input_field.value` |
| `class_name` | 🎨 Access element's CSS classes for style verification | `classes = element.class_name` |
| `id` | 🏷️ Grab the element's unique ID for perfect identification | `id = element.id` |
| `is_enabled` | ✅ Check if an element is ready for interaction | `if button.is_enabled:` |
| `async bounds` | 📏 Get the exact coordinates for pixel-perfect interaction | `coords = await element.bounds` |
| `async inner_html` | 🧩 Peek inside an element's HTML structure | `html = await element.inner_html` |
| `async get_element_text()` | 📜 Extract clean text content - no HTML mess | `text = await element.get_element_text()` |
| `get_attribute(name)` | 📊 Access any attribute with lightning speed | `href = link.get_attribute('href')` |
| `async scroll_into_view()` | 👁️ Make sure elements are visible before clicking | `await element.scroll_into_view()` |
| `async click(x_offset=0, y_offset=0)` | 👆 Click elements with amazing precision - even with custom offsets | `await button.click()` |
| `async click_using_js()` | 🔮 Use JavaScript magic to click problematic elements | `await overlay_button.click_using_js()` |
| `async send_keys(text)` | ⌨️ Enter text into fields at maximum speed | `await input.send_keys("text")` |
| `async type_keys(text, interval=0.1)` | 👨‍💻 Type like a real human with customizable speed | `await input.type_keys("hello", 0.2)` |
| `async get_screenshot(path)` | 📷 Grab pictures of specific elements - perfect for debugging | `await error.get_screenshot('error.png')` |
| `async set_input_files(files)` | 📤 Upload files with incredible ease | `await input.set_input_files('file.pdf')` |

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

Pydoll gives you superpowers to intercept and modify network requests before they're even sent! This is where the real magic happens - you can transform, block, or enhance any request on the fly.

#### Basic Interception

The simplest form of request interception lets you monitor and modify requests:

```python
from pydoll.events.fetch import FetchEvents
from pydoll.commands.fetch import FetchCommands
from functools import partial

async def basic_interceptor(page, event):
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
await page.on(FetchEvents.REQUEST_PAUSED, partial(basic_interceptor, page))
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

#### Blocking Unwanted Requests

Block ads, trackers, or any other unwanted requests:

```python
async def ad_blocker_interceptor(page, event):
    request_id = event['params']['requestId']
    url = event['params']['request']['url']
    
    # List of domains to block
    blocked_domains = ['ads.example.com', 'tracker.example.com', 'analytics']
    
    # Check if this request should be blocked
    should_block = any(domain in url for domain in blocked_domains)
    
    if should_block:
        print(f"🛑 Blocking request to: {url}")
        await page._execute_command(
            FetchCommands.fail_request(
                request_id=request_id,
                error_reason='Blocked'
            )
        )
    else:
        # Continue with the request
        await page._execute_command(
            FetchCommands.continue_request(
                request_id=request_id
            )
        )

await page.enable_fetch_events()
await page.on(FetchEvents.REQUEST_PAUSED, partial(ad_blocker_interceptor, page))
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

#### Intercepting and Modifying Responses

You can even capture and modify responses before the page sees them:

```python
async def response_modifier(page, event):
    request_id = event['params']['requestId']
    request_url = event['params']['request']['url']
    
    # First, continue the request but ask to intercept the response
    if 'api/products' in request_url:
        await page._execute_command(
            FetchCommands.continue_request(
                request_id=request_id,
                intercept_response=True  # This is the key flag
            )
        )
    else:
        # For other requests, just let them through
        await page._execute_command(
            FetchCommands.continue_request(
                request_id=request_id
            )
        )

# Handle the intercepted response
async def handle_response(page, event):
    request_id = event['params']['requestId']
    
    # Check if this is a response interception event
    if 'responseStatusCode' in event['params']:
        # Get the original response body
        response_body = await page._execute_command({
            'method': 'Fetch.getResponseBody',
            'params': {'requestId': request_id}
        })
        
        body = response_body.get('body', '{}')
        is_base64 = response_body.get('base64Encoded', False)
        
        # Decode if needed and modify the response
        if is_base64:
            import base64
            body = base64.b64decode(body).decode('utf-8')
        
        # Modify the response (in this example, we're appending data)
        # In a real scenario, you'd parse and modify the JSON
        modified_body = body.replace('"inStock": false', '"inStock": true')
        
        # Send the modified response
        await page._execute_command(
            FetchCommands.fulfill_request(
                request_id=request_id,
                response_code=200,
                response_headers={'Content-Type': 'application/json'},
                body=modified_body
            )
        )

# Register both event handlers
await page.enable_fetch_events()
await page.on(FetchEvents.REQUEST_PAUSED, partial(response_modifier, page))
await page.on(FetchEvents.REQUEST_PAUSED, partial(handle_response, page))
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

## 📄 License

Pydoll is licensed under the [MIT License](LICENSE).

---

<p align="center">
  <b>Pydoll</b> — Making browser automation magical! ✨
</p>
