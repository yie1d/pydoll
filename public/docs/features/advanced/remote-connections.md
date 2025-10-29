# Remote Connections & Hybrid Automation

Pydoll allows you to connect to already-running browsers via WebSocket, enabling remote control and hybrid automation scenarios. This is perfect for CI/CD pipelines, containerized environments, debugging sessions, and integrating Pydoll with existing CDP tooling.

!!! info "Zero Setup Required"
    Unlike traditional automation that launches browsers, remote connections let you control browsers that are already running. No process management needed!

## Why Remote Connections?

Remote connections unlock powerful automation scenarios:

| Use Case | Benefit |
|----------|---------|
| **CI/CD Pipelines** | Connect to browser containers without managing processes |
| **Docker Environments** | Control browsers running in separate containers |
| **Remote Debugging** | Automate browsers on remote servers or VMs |
| **Hybrid Tooling** | Integrate Pydoll with your existing CDP infrastructure |
| **Development** | Attach to your local browser for quick testing |
| **Multi-Tool Automation** | Share browser sessions between different tools |

## Setting Up a Remote Browser Server

Before you can connect remotely, you need to start Chrome with debugging enabled and properly configured to accept external connections.

### Basic Server Setup (Linux)

Start Chrome with remote debugging on a server:

```bash
# Basic setup - only accessible from localhost
google-chrome \
  --remote-debugging-port=9222 \
  --headless=new \
  --no-sandbox \
  --disable-dev-shm-usage \
  --user-data-dir=/tmp/chrome-profile

# Server setup - accessible from other machines
google-chrome \
  --remote-debugging-port=9222 \
  --remote-debugging-address=0.0.0.0 \
  --headless=new \
  --no-sandbox \
  --disable-dev-shm-usage \
  --user-data-dir=/tmp/chrome-profile
```

!!! warning "Security Critical"
    Using `--remote-debugging-address=0.0.0.0` makes the debugging port accessible from **any network interface**. This is necessary for remote connections but creates a significant security risk if exposed to the internet.

### Recommended Server Configuration

```bash
# Production-ready configuration
google-chrome \
  --remote-debugging-port=9222 \
  --remote-debugging-address=0.0.0.0 \
  --headless=new \
  --no-sandbox \
  --disable-dev-shm-usage \
  --disable-gpu \
  --disable-software-rasterizer \
  --disable-extensions \
  --disable-background-networking \
  --disable-background-timer-throttling \
  --disable-client-side-phishing-detection \
  --disable-popup-blocking \
  --disable-prompt-on-repost \
  --disable-sync \
  --metrics-recording-only \
  --no-first-run \
  --safebrowsing-disable-auto-update \
  --user-data-dir=/tmp/chrome-remote-$(date +%s)
```

**Key flags explained:**

| Flag | Purpose |
|------|---------|
| `--remote-debugging-port=9222` | Enable CDP on port 9222 |
| `--remote-debugging-address=0.0.0.0` | Allow external connections (security risk!) |
| `--headless` | Run without GUI (server mode) |
| `--no-sandbox` | Required in Docker/containers (security tradeoff) |
| `--disable-dev-shm-usage` | Prevent /dev/shm memory issues in containers |
| `--disable-gpu` | No GPU acceleration (recommended for headless) |
| `--user-data-dir=/tmp/...` | Isolated profile per instance |

!!! warning "About --no-sandbox Flag"
    The `--no-sandbox` flag disables Chrome's security sandbox, which isolates the browser process from the system. This flag is **required** in most Docker/container environments due to kernel capability restrictions, but it comes with security implications:
    
    - **Risk**: Removes isolation between browser and system
    - **When to use**: Docker containers, restricted environments
    - **Mitigation**: Ensure container-level isolation (namespaces, cgroups) and avoid running as root
    
    Consider using `--no-sandbox` only when absolutely necessary and implement additional security layers at the container level.

### Docker Setup

Create a containerized Chrome server:

!!! tip "Using Pre-built Images"
    For production, consider using official pre-built images instead of building your own:
    
    - **Selenium Images**: `selenium/standalone-chrome` (includes WebDriver)
    - **Zenika Alpine Chrome**: `zenika/alpine-chrome` (lightweight, ~200MB)
    - **Browserless**: `browserless/chrome` (production-ready with monitoring)
    
    These images are regularly updated, security-tested, and optimized for container environments.

**Dockerfile (Custom Build):**
```dockerfile
FROM ubuntu:22.04

# Install Chrome
RUN apt-get update && apt-get install -y \
    wget \
    gnupg \
    ca-certificates \
    && wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | apt-key add - \
    && echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list \
    && apt-get update \
    && apt-get install -y google-chrome-stable \
    && rm -rf /var/lib/apt/lists/*

# Expose debugging port
EXPOSE 9222

# Start Chrome with remote debugging
CMD ["google-chrome", \
     "--remote-debugging-port=9222", \
     "--remote-debugging-address=0.0.0.0", \
     "--headless=new", \
     "--no-sandbox", \
     "--disable-dev-shm-usage", \
     "--disable-gpu", \
     "--user-data-dir=/tmp/chrome-profile"]
```

**docker-compose.yml:**
```yaml
version: '3.8'

services:
  chrome-server:
    build: .
    ports:
      - "9222:9222"
    # Security: Only bind to localhost for local access
    # ports:
    #   - "127.0.0.1:9222:9222"
    shm_size: '2gb'  # Critical: Chrome uses /dev/shm for shared memory
                      # Default Docker shm_size (64MB) is insufficient
    restart: unless-stopped
    environment:
      - DISPLAY=:99
    networks:
      - automation-network
    # Optional: Resource limits for production
    # deploy:
    #   resources:
    #     limits:
    #       cpus: '2'
    #       memory: 4G

  automation-client:
    image: python:3.11
    depends_on:
      - chrome-server
    volumes:
      - ./:/app
    working_dir: /app
    command: python automation_script.py
    environment:
      - CHROME_WS=ws://chrome-server:9222/devtools/browser
    networks:
      - automation-network

networks:
  automation-network:
    driver: bridge
```

**Usage:**
```bash
# Start the stack
docker-compose up -d

# Check Chrome is running
curl http://localhost:9222/json/version

# Connect from automation client (inside Docker network)
# ws://chrome-server:9222/devtools/browser/...
```

### Systemd Service (Linux Server)

Create a persistent Chrome service:

**/etc/systemd/system/chrome-remote.service:**
```ini
[Unit]
Description=Chrome Remote Debugging Server
After=network.target

[Service]
Type=simple
User=chrome-user
Group=chrome-user
Environment="DISPLAY=:99"
ExecStart=/usr/bin/google-chrome \
    --remote-debugging-port=9222 \
    --remote-debugging-address=0.0.0.0 \
    --headless=new \
    --no-sandbox \
    --disable-dev-shm-usage \
    --disable-gpu \
    --user-data-dir=/var/lib/chrome-remote
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

**Setup and management:**
```bash
# Create dedicated user
sudo useradd -r -s /bin/false chrome-user
sudo mkdir -p /var/lib/chrome-remote
sudo chown chrome-user:chrome-user /var/lib/chrome-remote

# Install and enable service
sudo systemctl daemon-reload
sudo systemctl enable chrome-remote
sudo systemctl start chrome-remote

# Check status
sudo systemctl status chrome-remote

# View logs
sudo journalctl -u chrome-remote -f

# Restart service
sudo systemctl restart chrome-remote
```

### Network Security Configuration

#### Firewall Rules (iptables)

```bash
# Allow only specific IPs to access port 9222
sudo iptables -A INPUT -p tcp --dport 9222 -s 192.168.1.100 -j ACCEPT
sudo iptables -A INPUT -p tcp --dport 9222 -j DROP

# Save rules
sudo iptables-save > /etc/iptables/rules.v4
```

#### Firewall Rules (ufw)

```bash
# Deny all access to port 9222 by default
sudo ufw deny 9222

# Allow specific IP
sudo ufw allow from 192.168.1.100 to any port 9222

# Allow specific subnet
sudo ufw allow from 192.168.1.0/24 to any port 9222

# Enable firewall
sudo ufw enable
```

#### Nginx Reverse Proxy (with Authentication)

Protect Chrome debugging with HTTP authentication:

**/etc/nginx/sites-available/chrome-remote:**
```nginx
server {
    listen 80;
    server_name chrome.example.com;

    # Basic authentication
    auth_basic "Chrome Remote Debugging";
    auth_basic_user_file /etc/nginx/.htpasswd;

    location / {
        proxy_pass http://localhost:9222;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_read_timeout 86400;
    }
}
```

**Setup:**
```bash
# Create password file
sudo htpasswd -c /etc/nginx/.htpasswd admin

# Enable site
sudo ln -s /etc/nginx/sites-available/chrome-remote /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx

# Connect with authentication
# ws://admin:password@chrome.example.com/devtools/browser/...
```

### Connecting from Another Computer

Once your server is configured, connect from your client machine:

```python
import asyncio
from pydoll.browser.chromium import Chrome

async def connect_to_remote_server():
    """Connect to Chrome running on a remote server."""
    # Server IP and port
    server_ip = "192.168.1.100"
    server_port = 9222
    
    # 1. First, get the WebSocket URL
    import aiohttp
    
    async with aiohttp.ClientSession() as session:
        # Query the server for available targets
        url = f"http://{server_ip}:{server_port}/json/version"
        
        async with session.get(url) as response:
            data = await response.json()
            ws_url = data['webSocketDebuggerUrl']
            
            print(f"Server info:")
            print(f"  Browser: {data.get('Browser')}")
            print(f"  Protocol: {data.get('Protocol-Version')}")
            print(f"  WebSocket: {ws_url}")
    
    # 2. Connect to the browser
    chrome = Chrome()
    tab = await chrome.connect(ws_url)
    
    print(f"\n✅ Connected to remote Chrome server!")
    
    # 3. Use normally
    await tab.go_to('https://example.com')
    title = await tab.execute_script('return document.title')
    print(f"Page title: {title}")
    
    # 4. Cleanup
    await chrome.close()

asyncio.run(connect_to_remote_server())
```

### Testing Your Server Setup

```bash
# 1. Check if Chrome is running
ps aux | grep chrome

# 2. Check if port is listening
netstat -tulpn | grep 9222
# Or
ss -tulpn | grep 9222

# 3. Test local access
curl http://localhost:9222/json/version

# 4. Test remote access (from client machine)
curl http://SERVER_IP:9222/json/version

# 5. Check WebSocket URL
curl http://SERVER_IP:9222/json/version | jq -r '.webSocketDebuggerUrl'

# 6. List all available targets (tabs/pages)
curl http://SERVER_IP:9222/json/list
```

### Multi-Instance Setup

Run multiple Chrome instances on different ports:

```bash
#!/bin/bash
# start-chrome-pool.sh

for port in 9222 9223 9224 9225; do
    google-chrome \
        --remote-debugging-port=$port \
        --remote-debugging-address=0.0.0.0 \
        --headless=new \
        --no-sandbox \
        --disable-dev-shm-usage \
        --user-data-dir=/tmp/chrome-$port &
    
    echo "Started Chrome on port $port"
done

echo "Chrome pool ready. Ports: 9222-9225"
```

**Python client with pool:**
```python
import asyncio
from pydoll.browser.chromium import Chrome
import aiohttp

async def connect_to_pool(server_ip: str, ports: list[int]):
    """Connect to multiple Chrome instances."""
    tasks = []
    
    for port in ports:
        task = connect_to_instance(server_ip, port)
        tasks.append(task)
    
    results = await asyncio.gather(*tasks)
    return results

async def connect_to_instance(server_ip: str, port: int):
    """Connect to a single Chrome instance."""
    # Get WebSocket URL
    async with aiohttp.ClientSession() as session:
        url = f"http://{server_ip}:{port}/json/version"
        async with session.get(url) as response:
            data = await response.json()
            ws_url = data['webSocketDebuggerUrl']
    
    # Connect
    chrome = Chrome()
    tab = await chrome.connect(ws_url)
    
    # Run automation
    await tab.go_to('https://example.com')
    title = await tab.execute_script('return document.title')
    
    print(f"Port {port}: {title}")
    
    await chrome.close()
    return title

# Usage
asyncio.run(connect_to_pool('192.168.1.100', [9222, 9223, 9224, 9225]))
```

### Environment-Specific Configurations

#### Development
```bash
# Local development - accessible only from localhost
google-chrome \
  --remote-debugging-port=9222 \
  --headless=new
```

#### Staging
```bash
# Staging - accessible from internal network
google-chrome \
  --remote-debugging-port=9222 \
  --remote-debugging-address=0.0.0.0 \
  --headless=new \
  --no-sandbox \
  --disable-dev-shm-usage
# + Firewall rules to allow only staging subnet
```

#### Production
```bash
# Production - behind reverse proxy with auth
google-chrome \
  --remote-debugging-port=9222 \
  --remote-debugging-address=127.0.0.1 \
  --headless=new \
  --no-sandbox \
  --disable-dev-shm-usage \
  --disable-gpu
# + Nginx reverse proxy with SSL and authentication
# + Monitoring and auto-restart
# + Resource limits (cgroups/Docker)
```

!!! danger "Production Security Checklist"
    Before deploying to production:
    
    - [ ] Chrome not exposed directly to the internet
    - [ ] Reverse proxy with authentication in place
    - [ ] Firewall rules configured (allow only known IPs)
    - [ ] SSL/TLS encryption enabled
    - [ ] Resource limits configured
    - [ ] Monitoring and alerts set up
    - [ ] Regular security updates applied
    - [ ] Logs being collected and reviewed

## Connection Methods

Pydoll provides two approaches for remote connections, each suited for different scenarios.

### Method 1: Browser-Level Connection

Connect to a running browser using its WebSocket endpoint and get access to all opened tabs:

```python
import asyncio
from pydoll.browser.chromium import Chrome

async def connect_to_remote_browser():
    chrome = Chrome()
    
    # Connect to remote browser via WebSocket
    tab = await chrome.connect('ws://localhost:9222/devtools/browser/XXXX')
    
    # The tab returned is the first available tab
    print(f"Connected to tab: {await tab.execute_script('return document.title')}")
    
    # You can get all other tabs too
    all_tabs = await chrome.get_opened_tabs()
    print(f"Total tabs available: {len(all_tabs)}")
    
    # Use the tab normally
    await tab.go_to('https://example.com')
    element = await tab.find(id='main-content')
    text = await element.text
    print(f"Content: {text}")

asyncio.run(connect_to_remote_browser())
```

!!! tip "Getting the WebSocket URL"
    Start Chrome with debugging enabled:
    ```bash
    # Linux/Mac
    google-chrome --remote-debugging-port=9222
    
    # Windows
    "C:\Program Files\Google\Chrome\Application\chrome.exe" --remote-debugging-port=9222
    ```
    
    Then visit `http://localhost:9222/json/version` to get the WebSocket URL in the `webSocketDebuggerUrl` field.

### Method 2: Direct Element Control (Hybrid Approach)

If you already have your own CDP integration or low-level tooling, you can wrap existing elements with Pydoll's high-level API:

```python
import asyncio
from pydoll.connection.connection_handler import ConnectionHandler
from pydoll.elements.web_element import WebElement

async def hybrid_element_control():
    # Your existing CDP WebSocket endpoint and element objectId
    ws_endpoint = 'ws://localhost:9222/devtools/page/ABCDEF...'
    element_object_id = 'REMOTE_ELEMENT_OBJECT_ID'
    
    # Create connection handler
    connection = ConnectionHandler(ws_address=ws_endpoint)
    
    # Wrap the remote element with Pydoll's WebElement API
    element = WebElement(
        object_id=element_object_id,
        connection_handler=connection
    )
    
    # Now use Pydoll's full element API
    is_visible = await element.is_visible()
    print(f"Element visible: {is_visible}")
    
    await element.wait_until(is_interactable=True, timeout=10)
    await element.click()
    
    text = await element.text
    print(f"Element text: {text}")
    
    # Get element properties
    bounds = await element.bounds
    print(f"Element position: {bounds}")

asyncio.run(hybrid_element_control())
```

!!! info "Best of Both Worlds"
    This hybrid approach lets you leverage your existing CDP infrastructure while benefiting from Pydoll's ergonomic element API for interactions, waits, and property access.

## Practical Examples

### CI/CD: Selenium Grid Integration

Connect to browser containers in a Selenium Grid or similar infrastructure:

```python
import asyncio
from pydoll.browser.chromium import Chrome

async def selenium_grid_example():
    """Connect to a browser in Selenium Grid."""
    # Grid provides the WebSocket URL after session creation
    grid_ws_url = 'ws://selenium-hub:4444/session/abc123/cdp'
    
    chrome = Chrome()
    tab = await chrome.connect(grid_ws_url)
    
    # Run your automation
    await tab.go_to('https://example.com/test')
    
    # Extract dynamic content
    results = await tab.find(class_name='test-result', find_all=True)
    for result in results:
        status = await result.get_attribute('data-status')
        print(f"Test status: {status}")
    
    # No cleanup needed - Grid manages the browser

asyncio.run(selenium_grid_example())
```

### Docker: Multi-Container Setup

Automate browsers running in separate Docker containers:

```python
import asyncio
from pydoll.browser.chromium import Chrome

async def docker_multi_container():
    """Connect to browser in a Docker container."""
    # Browser runs in 'chrome-container' exposing port 9222
    docker_ws_url = 'ws://chrome-container:9222/devtools/browser/XXXX'
    
    chrome = Chrome()
    tab = await chrome.connect(docker_ws_url)
    
    # Run automation in containerized browser
    await tab.go_to('https://api.example.com/status')
    
    # Extract API response from page
    response_text = await tab.execute_script('''
        return document.querySelector('pre').textContent;
    ''')
    
    print(f"API Status: {response_text}")

asyncio.run(docker_multi_container())
```

!!! tip "Docker Compose Setup"
    ```yaml
    version: '3.8'
    services:
      chrome:
        image: chromium/chromium
        command: chromium --remote-debugging-port=9222 --remote-debugging-address=0.0.0.0
        ports:
          - "9222:9222"
      
      automation:
        build: .
        depends_on:
          - chrome
        environment:
          - CHROME_WS=ws://chrome:9222/devtools/browser
    ```

### Remote Debugging: Attach to Local Browser

Connect to your local browser for quick testing:

```python
import asyncio
import subprocess
import time
from pydoll.browser.chromium import Chrome

async def attach_to_local_browser():
    """Attach to your running local Chrome for debugging."""
    # This assumes Chrome is already running with debugging enabled
    # If not, uncomment the next lines to start it:
    # subprocess.Popen([
    #     'google-chrome',
    #     '--remote-debugging-port=9222',
    #     '--user-data-dir=/tmp/chrome-debug'
    # ])
    # time.sleep(3)  # Wait for Chrome to start
    
    chrome = Chrome()
    
    # Connect to local debugging port
    tab = await chrome.connect('ws://localhost:9222/devtools/browser')
    
    # See what's currently open
    current_url = await tab.execute_script('return window.location.href')
    print(f"Current page: {current_url}")
    
    # Interact with the page
    title = await tab.execute_script('return document.title')
    print(f"Page title: {title}")
    
    # Take a screenshot of what you're seeing
    await tab.take_screenshot('/tmp/debug-screenshot.png')
    print("Screenshot saved!")

asyncio.run(attach_to_local_browser())
```

!!! warning "User Data Directory"
    If you want to use your existing profile (with logins, extensions, etc.), **do not** specify `--user-data-dir`. But be careful: automating your main profile can interfere with manual browsing!

### Hybrid Automation: Custom CDP + Pydoll

Integrate Pydoll with your existing CDP tooling:

```python
import asyncio
import json
from pydoll.connection.connection_handler import ConnectionHandler
from pydoll.elements.web_element import WebElement

async def custom_cdp_integration():
    """Use Pydoll alongside your custom CDP implementation."""
    # Your existing CDP setup has found an element
    page_ws = 'ws://localhost:9222/devtools/page/ABC123'
    
    # You've used Runtime.evaluate to find an element
    # and got its objectId
    element_object_id = '{\"injectedScriptId\":1,\"id\":1}'
    
    # Create Pydoll connection
    connection = ConnectionHandler(ws_address=page_ws)
    
    # Wrap the element
    button = WebElement(
        object_id=element_object_id,
        connection_handler=connection
    )
    
    # Use Pydoll's high-level methods
    await button.wait_until(is_visible=True, timeout=5)
    await button.wait_until(is_interactable=True)
    
    # Click with realistic offset
    await button.click(offset_x=5, offset_y=5)
    
    # Get computed properties easily
    is_enabled = await button.is_enabled()
    bounds = await button.bounds
    
    print(f"Button clicked! Enabled: {is_enabled}, Bounds: {bounds}")

asyncio.run(custom_cdp_integration())
```

!!! tip "Object ID Format"
    The `objectId` is a string returned by CDP commands like `Runtime.evaluate` or `DOM.resolveNode`. It's usually a JSON string with fields like `injectedScriptId` and `id`.

## Connection Lifecycle

### Browser-Level Connection

```python
import asyncio
from pydoll.browser.chromium import Chrome

async def connection_lifecycle():
    chrome = Chrome()
    
    # 1. Connect to remote browser
    tab = await chrome.connect('ws://localhost:9222/devtools/browser/XXXX')
    
    # 2. Use normally
    await tab.go_to('https://example.com')
    
    # 3. Connection stays open until explicitly closed
    # The browser itself is NOT managed by Pydoll
    
    # 4. Close connection when done (browser keeps running)
    await chrome.close()

asyncio.run(connection_lifecycle())
```

!!! warning "No Process Management"
    When using `connect()`, Pydoll **does not manage** the browser process. Starting and stopping the browser is your responsibility. Calling `chrome.close()` only closes the WebSocket connection, not the browser.

### Element-Level Connection

```python
import asyncio
from pydoll.connection.connection_handler import ConnectionHandler
from pydoll.elements.web_element import WebElement

async def element_connection_lifecycle():
    # Create connection
    connection = ConnectionHandler(ws_address='ws://localhost:9222/devtools/page/ABC')
    
    # Create element
    element = WebElement(object_id='...', connection_handler=connection)
    
    # Use element
    await element.click()
    
    # Close connection when done
    await connection.close()

asyncio.run(element_connection_lifecycle())
```

## Best Practices

### 1. Connection Validation

Always validate that the connection is working:

```python
import asyncio
from pydoll.browser.chromium import Chrome

async def validate_connection():
    chrome = Chrome()
    
    try:
        tab = await chrome.connect('ws://localhost:9222/devtools/browser/XXXX')
        
        # Validate connection by executing a simple command
        await tab.execute_script('return true')
        
        print("✅ Connection validated!")
        return tab
    except Exception as e:
        print(f"❌ Connection failed: {e}")
        raise

asyncio.run(validate_connection())
```

### 2. Handle Connection Errors Gracefully

```python
import asyncio
from pydoll.browser.chromium import Chrome
from pydoll.exceptions import WebSocketConnectionClosed

async def handle_connection_errors():
    chrome = Chrome()
    
    try:
        tab = await chrome.connect('ws://remote-host:9222/devtools/browser/XXXX')
        
        # Your automation
        await tab.go_to('https://example.com')
        
    except WebSocketConnectionClosed:
        print("Connection was closed by remote browser")
        # Implement retry logic or fallback
    except ConnectionRefusedError:
        print("Cannot connect to remote browser - is it running?")
    except asyncio.TimeoutError:
        print("Connection timeout - remote browser is not responding")
    finally:
        await chrome.close()

asyncio.run(handle_connection_errors())
```

### 3. Use Context Managers for Cleanup

```python
import asyncio
from contextlib import asynccontextmanager
from pydoll.browser.chromium import Chrome

@asynccontextmanager
async def remote_browser(ws_url: str):
    """Context manager for remote browser connections."""
    chrome = Chrome()
    try:
        tab = await chrome.connect(ws_url)
        yield tab
    finally:
        await chrome.close()

async def main():
    ws_url = 'ws://localhost:9222/devtools/browser/XXXX'
    
    async with remote_browser(ws_url) as tab:
        await tab.go_to('https://example.com')
        # Connection automatically closed when exiting context

asyncio.run(main())
```

### 4. Separate Concerns in Hybrid Setups

```python
import asyncio
from pydoll.connection.connection_handler import ConnectionHandler
from pydoll.elements.web_element import WebElement

async def hybrid_separation_example():
    """Keep discovery and interaction separate."""
    page_ws = 'ws://localhost:9222/devtools/page/ABC'
    
    # Phase 1: Use your CDP tooling for discovery
    element_ids = await your_custom_discovery_logic(page_ws)
    
    # Phase 2: Use Pydoll for interaction
    connection = ConnectionHandler(ws_address=page_ws)
    
    for obj_id in element_ids:
        element = WebElement(object_id=obj_id, connection_handler=connection)
        
        # Pydoll handles the complex interaction logic
        await element.wait_until(is_visible=True)
        await element.click()
        
    await connection.close()

async def your_custom_discovery_logic(ws_url):
    """Your existing CDP implementation."""
    # Your code to find elements and return objectIds
    return ['obj1', 'obj2', 'obj3']

asyncio.run(hybrid_separation_example())
```

## Security Considerations

!!! danger "Production Environments"
    Remote debugging ports expose **full control** over the browser, including:
    
    - Access to all pages and data
    - Ability to execute arbitrary JavaScript
    - Cookie and session access
    - File system access via downloads
    
    **Never expose debugging ports to the internet without proper authentication and network security!**

### Secure Remote Connections

```python
import asyncio
from pydoll.browser.chromium import Chrome

async def secure_connection():
    """Connect through SSH tunnel or VPN."""
    # Good: Use SSH tunnel
    # ssh -L 9222:localhost:9222 user@remote-server
    tab = await Chrome().connect('ws://localhost:9222/devtools/browser/XXXX')
    
    # Bad: Direct connection over internet
    # tab = await Chrome().connect('ws://public-ip:9222/devtools/browser/XXXX')  # DON'T!
    
    await tab.go_to('https://example.com')

asyncio.run(secure_connection())
```

### Recommended Security Practices

| Practice | Why | How |
|----------|-----|-----|
| **SSH Tunnels** | Encrypt traffic and authenticate | `ssh -L 9222:localhost:9222 user@host` |
| **VPN** | Network-level security | Connect via corporate/private VPN |
| **Firewall Rules** | Restrict access | Allow only specific IPs |
| **Docker Networks** | Container isolation | Use private Docker networks |
| **No Public Exposure** | Prevent attacks | Never bind to `0.0.0.0` in production |

## Troubleshooting

### Connection Refused

```
ConnectionRefusedError: [Errno 111] Connection refused
```

**Causes:**
- Browser not running with debugging enabled
- Wrong port number
- Firewall blocking connection
- Browser crashed

**Solutions:**
```bash
# 1. Check if browser is running with correct flags
ps aux | grep "remote-debugging-port"

# 2. Verify port is listening
netstat -tulpn | grep 9222

# 3. Test WebSocket connectivity
curl http://localhost:9222/json
```

### Invalid WebSocket URL

```
websockets.exceptions.InvalidURI: ws://localhost:9222 isn't a valid URI
```

**Cause:** Missing the `/devtools/browser/XXXX` path

**Solution:**
```python
# ❌ Bad
tab = await chrome.connect('ws://localhost:9222')

# ✅ Good - get from /json endpoint
import aiohttp

async with aiohttp.ClientSession() as session:
    async with session.get('http://localhost:9222/json/version') as resp:
        data = await resp.json()
        ws_url = data['webSocketDebuggerUrl']
        tab = await chrome.connect(ws_url)
```

### Connection Closed Unexpectedly

```
WebSocketConnectionClosed: WebSocket connection closed
```

**Causes:**
- Browser crashed or was closed manually
- Network interruption
- Browser was restarted
- Tab was closed (for page-level connections)

**Solution: Implement reconnection logic**
```python
import asyncio
from pydoll.browser.chromium import Chrome
from pydoll.exceptions import WebSocketConnectionClosed

async def with_reconnect(ws_url: str, max_retries: int = 3):
    """Reconnect automatically on connection loss."""
    chrome = Chrome()
    retries = 0
    
    while retries < max_retries:
        try:
            tab = await chrome.connect(ws_url)
            
            # Your automation
            await tab.go_to('https://example.com')
            
            break  # Success!
            
        except WebSocketConnectionClosed:
            retries += 1
            print(f"Connection lost. Retry {retries}/{max_retries}...")
            await asyncio.sleep(2)
            
        except Exception as e:
            print(f"Unrecoverable error: {e}")
            break
    
    await chrome.close()

asyncio.run(with_reconnect('ws://localhost:9222/devtools/browser/XXXX'))
```

### Element ObjectId Not Found

```
KeyError: 'objectId'
```

**Cause:** The element was removed from the DOM or the objectId is invalid

**Solution: Refresh element reference**
```python
from pydoll.connection.connection_handler import ConnectionHandler
from pydoll.elements.web_element import WebElement

# Your CDP code must re-evaluate to get new objectId
# objectId becomes invalid if element is removed and re-added to DOM

async def refresh_element_reference(connection, old_object_id):
    """Re-find element if objectId becomes stale."""
    try:
        element = WebElement(object_id=old_object_id, connection_handler=connection)
        await element.click()
    except KeyError:
        # Element is stale, need to re-find it using your CDP logic
        new_object_id = await your_find_element_logic()
        element = WebElement(object_id=new_object_id, connection_handler=connection)
        await element.click()
```

## Comparison: Local vs Remote

| Aspect | Local (`browser.start()`) | Remote (`browser.connect()`) |
|--------|---------------------------|------------------------------|
| **Process Management** | Pydoll manages browser process | You manage browser process |
| **Startup Time** | Must start browser (~1-2s) | Instant connection |
| **Browser Options** | Full control via `ChromiumOptions` | Limited (browser already configured) |
| **Context Manager** | Closes browser on exit | Only closes connection |
| **Use Case** | Full automation control | CI/CD, debugging, hybrid setups |
| **Cleanup** | Automatic | Manual browser management |
| **Extensions** | Can be configured | Already loaded (or not) |
| **User Data** | Can specify directory | Fixed when browser started |

## Connection Reference

### Browser.connect() Method

```python
async def connect(self, ws_address: str) -> Tab
```

**Parameters:**
- `ws_address` (str): Full WebSocket URL including path
  - Format: `ws://host:port/devtools/browser/XXXX` or `ws://host:port/devtools/page/XXXX`

**Returns:**
- `Tab`: First available tab in the browser

**Raises:**
- `ConnectionRefusedError`: Cannot connect to WebSocket
- `websockets.exceptions.InvalidURI`: Invalid WebSocket URL format
- `asyncio.TimeoutError`: Connection timeout

**Example:**
```python
chrome = Chrome()
tab = await chrome.connect('ws://localhost:9222/devtools/browser/abc123')
```

### ConnectionHandler Constructor

```python
def __init__(
    self,
    connection_port: Optional[int] = None,
    page_id: Optional[str] = None,
    ws_address: Optional[str] = None,
)
```

**Parameters:**
- `ws_address` (str, optional): Full WebSocket URL (highest priority)
- `connection_port` (int, optional): Debugging port (if `ws_address` not provided)
- `page_id` (str, optional): Target page ID

**Example:**
```python
# Direct WebSocket connection
connection = ConnectionHandler(ws_address='ws://localhost:9222/devtools/page/ABC')

# Or by port and page ID
connection = ConnectionHandler(connection_port=9222, page_id='ABC')
```

## Further Reading

- **[Event System](event-system.md)** - Monitor remote browser events
- **[Network Monitoring](../network/monitoring.md)** - Track requests in remote browsers
- **[Browser Options](../configuration/browser-options.md)** - Configure local browsers before starting

!!! tip "Start Local, Scale Remote"
    Develop your automation locally with `browser.start()` for quick iterations, then deploy with `browser.connect()` for production CI/CD pipelines and containerized environments.
