# Key Features

Pydoll brings groundbreaking capabilities to browser automation, making it significantly more powerful than traditional tools while being easier to use.

## Core Capabilities

### Zero WebDrivers

Unlike traditional browser automation tools like Selenium, Pydoll eliminates the need for WebDrivers entirely. By connecting directly to browsers through the Chrome DevTools Protocol, Pydoll:

- Eliminates version compatibility issues between browser and driver
- Reduces setup complexity and maintenance overhead
- Provides more reliable connections without driver-related issues
- Allows for automation of all Chromium-based browsers with a unified API

No more "chromedriver version doesn't match Chrome version" errors or mysterious webdriver crashes.

### Async-First Architecture

Built from the ground up with Python's asyncio, Pydoll provides:

- **True Concurrency**: Run multiple operations in parallel without blocking
- **Efficient Resource Usage**: Manage many browser instances with minimal overhead
- **Modern Python Patterns**: Context managers, async iterators, and other asyncio-friendly interfaces
- **Performance Optimizations**: Reduced latency and increased throughput for automation tasks

### Human-Like Interactions

Avoid detection by mimicking real user behavior:

- **Natural Typing**: Type text with randomized timing between keystrokes
- **Realistic clicking**: Click with realistic timing and movement, including offset

### Event-Driven Capabilities

Respond to browser events in real-time:

- **Network Monitoring**: Track requests, responses, and failed loads
- **DOM Observation**: React to changes in the page structure
- **Page Lifecycle Events**: Capture navigation, loading, and rendering events
- **Custom Event Handlers**: Register callbacks for specific events of interest

### Multi-Browser Support

Pydoll works seamlessly with:

- **Google Chrome**: Primary support with all features available
- **Microsoft Edge**: Full support for Edge-specific features
- **Chromium**: Support for other Chromium-based browsers

### Screenshot and PDF Export

Capture visual content from web pages:

- **Full Page Screenshots**: Capture entire page content, even beyond the viewport
- **Element Screenshots**: Target specific elements for capture
- **High-Quality PDF Export**: Generate PDF documents from web pages
- **Custom Formatting**: Coming soon!

## Native Cloudflare Captcha Bypass

!!! warning "Important Information About Captcha Bypass"
    The effectiveness of Cloudflare Turnstile bypass depends on several factors:
    
    - **IP Reputation**: Cloudflare assigns a "trust score" to each IP address. Clean residential IPs typically receive higher scores.
    - **Previous History**: IPs with a history of suspicious activity may be permanently flagged.
    
    Pydoll can achieve scores comparable to a regular browser session, but cannot overcome IP-based blocks or extremely restrictive configurations. For best results, use residential IPs with good reputation.
    
    Remember that captcha bypass techniques operate in a gray area and should be used responsibly.

One of Pydoll's most powerful features is its ability to automatically bypass Cloudflare Turnstile captchas that block most automation tools:

### Context Manager Approach (Synchronous)

```python
import asyncio
from pydoll.browser import Chrome

async def bypass_cloudflare_example():
    browser = Chrome()
    await browser.start()
    page = await browser.get_page()
    
    # The context manager will wait for the captcha to be processed
    # before continuing execution
    async with page.expect_and_bypass_cloudflare_captcha():
        await page.go_to('https://site-with-cloudflare.com')
        print("Waiting for captcha to be handled...")
    
    # This code runs only after the captcha is successfully bypassed
    print("Captcha bypassed! Continuing with automation...")
    await page.find_element_by_id('protected-content').get_text()
    
    await browser.stop()

asyncio.run(bypass_cloudflare_example())
```

### Background Processing Approach

```python
import asyncio
from pydoll.browser import Chrome

async def background_bypass_example():
    browser = Chrome()
    await browser.start()
    page = await browser.get_page()
    
    # Enable automatic captcha solving before navigating
    await page.enable_auto_solve_cloudflare_captcha()
    
    # Navigate to the protected site - captcha handled automatically in background
    await page.go_to('https://site-with-cloudflare.com')
    print("Page loaded, captcha will be handled in the background...")
    
    # Add a small delay to allow captcha solving to complete
    await asyncio.sleep(3)
    
    # Continue with automation
    await page.find_element_by_id('protected-content').get_text()
    
    # Disable auto-solving when no longer needed
    await page.disable_auto_solve_cloudflare_captcha()
    
    await browser.stop()

asyncio.run(background_bypass_example())
```

Access websites that actively block automation tools without using third-party captcha solving services. This native captcha handling makes Pydoll suitable for automating previously inaccessible websites.

## Concurrent Scraping

Pydoll's async architecture allows you to scrape multiple pages or websites simultaneously for maximum efficiency:

```python
import asyncio
from pydoll.browser.chrome import Chrome
from pydoll.constants import By

async def scrape_page(url):
    """Process a single page and extract data"""
    async with Chrome() as browser:
        await browser.start()
        page = await browser.get_page()
        await page.go_to(url)
        
        # Extract data
        title = await page.execute_script('return document.title')
        
        # Find elements and extract content
        elements = await page.find_elements(By.CSS_SELECTOR, '.article-content')
        content = []
        for element in elements:
            text = await element.get_element_text()
            content.append(text)
            
        return {
            "url": url,
            "title": title,
            "content": content
        }

async def main():
    # List of URLs to scrape in parallel
    urls = [
        'https://example.com/page1',
        'https://example.com/page2',
        'https://example.com/page3',
        'https://example.com/page4',
        'https://example.com/page5',
    ]
    
    # Process all URLs concurrently
    results = await asyncio.gather(*(scrape_page(url) for url in urls))
    
    # Print results
    for result in results:
        print(f"Scraped {result['url']}: {result['title']}")
        print(f"Found {len(result['content'])} content blocks")
    
    return results

# Run the concurrent scraping
all_data = asyncio.run(main())
```

This approach provides dramatic performance improvements over sequential scraping, especially for I/O-bound tasks like web scraping. Instead of waiting for each page to load one after another, Pydoll processes them all simultaneously, reducing total execution time significantly. For example, scraping 10 pages that each take 2 seconds to load would take just over 2 seconds total instead of 20+ seconds with sequential processing.

## Advanced Keyboard Control

Pydoll provides human-like keyboard interaction with precise control over typing behavior:

```python
import asyncio
from pydoll.browser.chrome import Chrome
from pydoll.constants import By
from pydoll.common.keys import Keys

async def realistic_typing_example():
    async with Chrome() as browser:
        await browser.start()
        page = await browser.get_page()
        await page.go_to('https://example.com/login')
        
        # Find login form elements
        username = await page.find_element(By.ID, 'username')
        password = await page.find_element(By.ID, 'password')
        
        # Type with realistic timing (interval between keystrokes)
        await username.type_keys("user@example.com", interval=0.15)
        
        # Use special key combinations
        await password.click()
        await password.key_down(Keys.SHIFT)
        await password.send_keys("PASSWORD")
        await password.key_up(Keys.SHIFT)
        
        # Press Enter to submit
        await password.send_keys(Keys.ENTER)
        
        # Wait for navigation
        await asyncio.sleep(2)
        print("Logged in successfully!")

asyncio.run(realistic_typing_example())
```

This realistic typing helps avoid detection by websites that look for automation patterns. The natural timing and ability to use special key combinations makes Pydoll's interactions virtually indistinguishable from human users.

## Powerful Event System

Pydoll's event system allows you to react to browser events in real-time:

```python
import asyncio
from pydoll.browser.chrome import Chrome
from pydoll.events.network import NetworkEvents
from pydoll.events.page import PageEvents
from functools import partial

async def event_monitoring_example():
    async with Chrome() as browser:
        await browser.start()
        page = await browser.get_page()
        
        # Monitor page load events
        async def on_page_loaded(event):
            print(f"🌐 Page loaded: {event['params'].get('url')}")
            
        await page.enable_page_events()
        await page.on(PageEvents.PAGE_LOADED, on_page_loaded)
        
        # Monitor network requests
        async def on_request(page, event):
            url = event['params']['request']['url']
            print(f"🔄 Request to: {url}")
            
        await page.enable_network_events()
        await page.on(NetworkEvents.REQUEST_WILL_BE_SENT, 
                      partial(on_request, page))
        
        # Navigate and see events in action
        await page.go_to('https://example.com')
        await asyncio.sleep(5)  # Allow time to see events
        
asyncio.run(event_monitoring_example())
```

The event system makes Pydoll uniquely powerful for monitoring API requests and responses, creating reactive automations, debugging complex web applications, and building comprehensive web monitoring tools.

## File Upload Support

Seamlessly handle file uploads in your automation:

```python
import asyncio
import os
from pydoll.browser.chrome import Chrome
from pydoll.constants import By

async def file_upload_example():
    async with Chrome() as browser:
        await browser.start()
        page = await browser.get_page()
        await page.go_to('https://example.com/upload')
        
        # Method 1: Direct file input
        file_input = await page.find_element(By.XPATH, '//input[@type="file"]')
        await file_input.set_input_files('path/to/document.pdf')
        
        # Method 2: Using file chooser with an upload button
        sample_file = os.path.join(os.getcwd(), 'sample.jpg')
        async with page.expect_file_chooser(files=sample_file):
            upload_button = await page.find_element(By.ID, 'upload-button')
            await upload_button.click()
            
        # Submit the form
        submit = await page.find_element(By.ID, 'submit-button')
        await submit.click()
        
        print("Files uploaded successfully!")

asyncio.run(file_upload_example())
```

File uploads are notoriously difficult to automate in other frameworks, often requiring workarounds. Pydoll makes it straightforward with both direct file input and file chooser dialog support.

## Multi-Browser Example

Pydoll works with different browsers through a consistent API:

```python
import asyncio
from pydoll.browser.chrome import Chrome
from pydoll.browser.edge import Edge

async def multi_browser_example():
    # Run the same automation in Chrome
    async with Chrome() as chrome:
        await chrome.start()
        chrome_page = await chrome.get_page()
        await chrome_page.go_to('https://example.com')
        chrome_title = await chrome_page.execute_script('return document.title')
        print(f"Chrome title: {chrome_title}")
    
    # Run the same automation in Edge
    async with Edge() as edge:
        await edge.start()
        edge_page = await edge.get_page()
        await edge_page.go_to('https://example.com')
        edge_title = await edge_page.execute_script('return document.title')
        print(f"Edge title: {edge_title}")

asyncio.run(multi_browser_example())
```

Cross-browser compatibility without changing your code. Test your automations across different browsers to ensure they work everywhere.

## Proxy Integration

Unlike many automation tools that struggle with proxy implementation, Pydoll offers native proxy support with full authentication capabilities. This makes it ideal for:

- **Web scraping** projects that need to rotate IPs
- **Geo-targeted testing** of applications across different regions
- **Privacy-focused automation** that requires anonymizing traffic
- **Testing web applications** through corporate proxies

Configuring proxies in Pydoll is straightforward:

```python
import asyncio
from pydoll.browser.chrome import Chrome
from pydoll.browser.options import Options

async def proxy_example():
    # Create browser options
    options = Options()
    
    # Simple proxy without authentication
    options.add_argument('--proxy-server=192.168.1.100:8080')
    # Or proxy with authentication
    # options.add_argument('--proxy-server=username:password@192.168.1.100:8080')
    
    # Bypass proxy for specific domains
    options.add_argument('--proxy-bypass-list=*.internal.company.com,localhost')

    # Start browser with proxy configuration
    async with Chrome(options=options) as browser:
        await browser.start()
        page = await browser.get_page()
        
        # Test the proxy by visiting an IP echo service
        await page.go_to('https://api.ipify.org')
        ip_address = await page.page_source
        print(f"Current IP address: {ip_address}")
        
        # Continue with your automation
        await page.go_to('https://example.com')
        title = await page.execute_script('document.title')
        print(f"Page title: {title}")

asyncio.run(proxy_example())
```

## Request Interception

Intercept and modify network requests before they're sent:

```python
import asyncio
from pydoll.browser.chrome import Chrome
from pydoll.events.fetch import FetchEvents
from pydoll.commands.fetch import FetchCommands
from functools import partial

async def request_interception_example():
    async with Chrome() as browser:
        await browser.start()
        page = await browser.get_page()
        
        # Define the request interceptor
        async def intercept_request(page, event):
            request_id = event['params']['requestId']
            url = event['params']['request']['url']
            
            if '/api/' in url:
                # Get original headers
                original_headers = event['params']['request'].get('headers', {})
                
                # Add custom headers
                custom_headers = {
                    **original_headers,
                    'Authorization': 'Bearer my-token-123',
                    'X-Custom-Header': 'CustomValue'
                }
                
                print(f"🔄 Modifying request to: {url}")
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
        
        # Enable interception and register handler
        await page.enable_fetch_events()
        await page.on(FetchEvents.REQUEST_PAUSED, 
                      partial(intercept_request, page))
        
        # Navigate to trigger requests
        await page.go_to('https://example.com')
        await asyncio.sleep(5)  # Allow time for requests to process

asyncio.run(request_interception_example())
```

This powerful capability allows you to add authentication headers dynamically, modify request payloads before they're sent, mock API responses for testing, and analyze and debug network traffic.

Each of these features showcases what makes Pydoll a next-generation browser automation tool, combining the power of direct browser control with an intuitive, async-native API. 