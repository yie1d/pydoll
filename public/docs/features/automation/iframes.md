# Working with IFrames

IFrames (inline frames) are one of the trickiest aspects of browser automation. Pydoll provides a clean, intuitive API for iframe interaction that abstracts away the complexity of CDP target management.

## Quick Start

### Basic IFrame Interaction

```python
import asyncio
from pydoll.browser.chromium import Chrome

async def interact_with_iframe():
    async with Chrome() as browser:
        tab = await browser.start()
        await tab.go_to('https://example.com/page-with-iframe')
        
        # Find the iframe element
        iframe_element = await tab.find(tag_name='iframe', id='content-frame')
        
        # Get a Tab instance for the iframe
        iframe = await tab.get_frame(iframe_element)
        
        # Now interact with elements inside the iframe
        button = await iframe.find(id='submit-button')
        await button.click()
        
        # Find and fill form inside iframe
        username = await iframe.find(name='username')
        await username.type_text('john_doe')

asyncio.run(interact_with_iframe())
```

!!! tip "IFrames are Just Tabs"
    In Pydoll, an iframe returns a `Tab` object. This means **all methods available on Tab work on iframes**: `find()`, `query()`, `execute_script()`, `take_screenshot()`, and more.

## Common Use Cases

### Nested IFrames

Some pages have iframes inside iframes. Handle them by chaining `get_frame()` calls:

```python
import asyncio
from pydoll.browser.chromium import Chrome

async def nested_iframes():
    async with Chrome() as browser:
        tab = await browser.start()
        await tab.go_to('https://example.com/nested-frames')
        
        # Get the outer iframe
        outer_iframe_element = await tab.find(id='outer-frame')
        outer_iframe = await tab.get_frame(outer_iframe_element)
        
        # Get the inner iframe (inside the outer iframe)
        inner_iframe_element = await outer_iframe.find(id='inner-frame')
        inner_iframe = await outer_iframe.get_frame(inner_iframe_element)
        
        # Interact with elements in the innermost iframe
        content = await inner_iframe.find(class_name='content')
        text = await content.text
        print(f"Content from nested iframe: {text}")

asyncio.run(nested_iframes())
```

### Multiple IFrames on Same Page

When dealing with multiple iframes, treat each as its own Tab:

```python
import asyncio
from pydoll.browser.chromium import Chrome

async def multiple_iframes():
    async with Chrome() as browser:
        tab = await browser.start()
        await tab.go_to('https://example.com/multi-frame')
        
        # Get all iframes on the page
        iframe_elements = await tab.find(tag_name='iframe', find_all=True)
        
        for idx, iframe_element in enumerate(iframe_elements):
            frame = await tab.get_frame(iframe_element)
            
            # Each iframe has its own isolated content
            title = await frame.execute_script('return document.title')
            print(f"IFrame {idx} title: {title}")
            
            # Interact with specific iframe
            if idx == 0:
                # Work with first iframe
                button = await frame.find(tag_name='button')
                await button.click()
            elif idx == 1:
                # Work with second iframe
                input_field = await frame.find(tag_name='input')
                await input_field.type_text('Hello from iframe 2!')

asyncio.run(multiple_iframes())
```

### CAPTCHA IFrames

Many CAPTCHA systems (like hCaptcha) use iframes:

```python
import asyncio
from pydoll.browser.chromium import Chrome

async def handle_captcha_iframe():
    async with Chrome() as browser:
        tab = await browser.start()
        await tab.go_to('https://example.com/with-captcha')
        
        # Find the CAPTCHA iframe
        captcha_iframe_element = await tab.find(
            tag_name='iframe',
            class_name='hcaptcha-iframe',
            timeout=10
        )
        
        # Switch to iframe context
        captcha_frame = await tab.get_frame(captcha_iframe_element)
        
        # Interact with CAPTCHA elements
        checkbox = await captcha_frame.find(id='checkbox')
        await checkbox.click()
        
        # Wait for CAPTCHA to process
        await asyncio.sleep(2)

asyncio.run(handle_captcha_iframe())
```

## Understanding IFrames

### What is an IFrame?

An `<iframe>` (inline frame) is an HTML element that embeds another HTML document within the current page. Think of it as a "browser window within a browser window."

```html
<html>
  <body>
    <h1>Main Page</h1>
    <p>This is the main document</p>
    
    <!-- This iframe loads a completely separate document -->
    <iframe src="https://other-site.com/content.html" id="my-frame">
    </iframe>
  </body>
</html>
```

Each iframe:

- Has its own **separate DOM** (Document Object Model)
- Loads its own HTML, CSS, and JavaScript
- Can be from a different domain (cross-origin)
- Operates in an isolated browsing context

### Why You Can't Interact Directly

This code **won't work** as you might expect:

```python
# ❌ This will NOT find elements inside the iframe
button = await tab.find(id='button-inside-iframe')
```

**Why?** Because `tab.find()` searches the **main page's DOM**. The iframe has a **completely separate DOM** that isn't accessible from the parent.

Think of it like this:

```
Main Page DOM                 IFrame DOM (Separate!)
├── <html>                    ├── <html>
│   ├── <body>                │   ├── <body>
│   │   ├── <div>             │   │   ├── <div>
│   │   └── <iframe>          │   │   └── <button id="inside">
│   │       (separate world)  │   └── </body>
│   └── </body>               └── </html>
└── </html>
```

!!! info "Isolated Browsing Contexts"
    IFrames create what's called an **isolated browsing context**. This isolation is a security feature that prevents malicious iframes from accessing or manipulating the parent page's content.

### How Pydoll Solves This

Under the hood, Pydoll uses Chrome DevTools Protocol (CDP) to:

1. **Identify the iframe target**: Each iframe gets its own CDP target ID
2. **Create a new Tab instance**: This Tab is scoped to the iframe's DOM
3. **Provide full access**: All Tab methods work on the iframe's isolated DOM

```python
# This is what happens internally:
iframe_element = await tab.find(tag_name='iframe')  # Find the <iframe> tag
frame = await tab.get_frame(iframe_element)         # Get CDP target for iframe

# Now 'frame' is a Tab that operates on the iframe's DOM
button = await frame.find(id='button-inside-iframe')  # ✅ Works!
```

### Technical Deep Dive: CDP Targets

When you call `tab.get_frame()`, Pydoll:

1. **Extracts the `src` attribute** from the iframe element
2. **Queries CDP for all targets** using `Target.getTargets()`
3. **Matches the iframe URL** to find its corresponding target ID
4. **Creates a Tab instance** with that target ID

Each target has:

- **Unique Target ID**: Identifies the browsing context
- **Separate WebSocket connection**: For isolated CDP communication
- **Own document tree**: Complete independence from parent

```python
# Internally in tab.py:
async def get_frame(self, frame: WebElement) -> Tab:
    # Get iframe's source URL
    frame_url = frame.get_attribute('src')
    
    # Find the target that matches this URL
    targets = await self._browser.get_targets()
    iframe_target = next((t for t in targets if t['url'] == frame_url), None)
    
    # Create a Tab for this iframe's target
    target_id = iframe_target['targetId']
    tab = Tab(self._browser, target_id=target_id, ...)
    
    return tab  # Now you can interact with iframe as a Tab!
```

!!! warning "IFrame Must Have Valid `src`"
    The iframe must have a valid `src` attribute for Pydoll to locate its CDP target. IFrames using `srcdoc` or dynamically injected content may not work with `get_frame()`.

## Comparison: Main Page vs IFrame

| Aspect | Main Page | IFrame |
|--------|-----------|--------|
| **DOM** | Own document tree | Separate document tree |
| **CDP Target** | One target ID | Different target ID |
| **Element Search** | `tab.find()` | `iframe.find()` |
| **JavaScript Context** | `window` of main page | `window` of iframe |
| **Origin** | Page's origin | Can be cross-origin |
| **Storage** | Shared with page | Can be isolated |

## Screenshots in IFrames

!!! info "Screenshot Limitations"
    `tab.take_screenshot()` only works on **top-level targets**. For iframe screenshots, use `element.take_screenshot()` on elements **inside** the iframe.

```python
import asyncio
from pydoll.browser.chromium import Chrome

async def iframe_screenshot():
    async with Chrome() as browser:
        tab = await browser.start()
        await tab.go_to('https://example.com/iframe-page')
        
        iframe_element = await tab.find(tag_name='iframe')
        frame = await tab.get_frame(iframe_element)
        
        # ❌ This won't work for iframes
        # await frame.take_screenshot('frame.png')
        
        # ✅ Instead, screenshot an element inside the iframe
        content = await frame.find(id='content')
        await content.take_screenshot('iframe-content.png')

asyncio.run(iframe_screenshot())
```

## Error Handling

### IFrame Not Found

```python
import asyncio
from pydoll.browser.chromium import Chrome
from pydoll.exceptions import IFrameNotFound, InvalidIFrame, NotAnIFrame

async def safe_iframe_handling():
    async with Chrome() as browser:
        tab = await browser.start()
        await tab.go_to('https://example.com')
        
        try:
            # Find iframe element
            iframe_element = await tab.find(tag_name='iframe', timeout=5)
            
            # Get frame Tab
            frame = await tab.get_frame(iframe_element)
            
        except NotAnIFrame:
            print("Element is not an iframe!")
        except InvalidIFrame as e:
            print(f"Invalid iframe: {e}")
        except IFrameNotFound:
            print("IFrame target not found in browser")

asyncio.run(safe_iframe_handling())
```

### Missing `src` Attribute

```python
import asyncio
from pydoll.browser.chromium import Chrome

async def check_iframe_src():
    async with Chrome() as browser:
        tab = await browser.start()
        await tab.go_to('https://example.com')
        
        iframe_element = await tab.find(tag_name='iframe')
        
        # Check if iframe has a valid src before getting frame
        src = iframe_element.get_attribute('src')
        if not src:
            print("Warning: IFrame has no src attribute")
            # Handle accordingly
        else:
            frame = await tab.get_frame(iframe_element)

asyncio.run(check_iframe_src())
```

## Learn More

For deeper understanding of iframe mechanics and CDP targets:

- **[Deep Dive: Tab Domain](../../deep-dive/tab-domain.md#iframe-handling)**: Technical details on iframe target resolution
- **[Deep Dive: Browser Domain](../../deep-dive/browser-domain.md#target-management)**: How CDP manages multiple targets
- **[Element Finding](../element-finding.md#scoped-search)**: Understanding DOM scope in element searches

IFrames may seem complex, but Pydoll's API makes them as easy to work with as regular page elements. The key is understanding that each iframe is its own isolated Tab with a separate DOM and CDP target.
