"""Shared pytest fixtures for all tests."""

import pytest

from pydoll.browser.options import ChromiumOptions as Options


@pytest.fixture
def ci_chrome_options():
    """Chrome options optimized for CI environments."""
    options = Options()
    options.headless = True
    options.start_timeout = 60  # Increased timeout for CI

    # CI-specific arguments - essentials only
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-gpu')
    options.add_argument('--disable-extensions')
    
    # Stability improvements
    options.add_argument('--disable-software-rasterizer')
    options.add_argument('--disable-setuid-sandbox')
    
    # Allow local file access for test HTMLs
    options.add_argument('--allow-file-access-from-files')
    options.add_argument('--enable-local-file-accesses')

    return options

