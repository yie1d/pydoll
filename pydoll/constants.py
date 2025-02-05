from enum import Enum


class By(str, Enum):
    CSS_SELECTOR = 'css'
    XPATH = 'xpath'
    CLASS_NAME = 'class_name'
    ID = 'id'
    TAG_NAME = 'tag_name'


class Scripts:
    ELEMENT_VISIBLE = """
    function() {
        const rect = this.getBoundingClientRect();
        return (
            rect.width > 0 && rect.height > 0
            && getComputedStyle(this).visibility !== 'hidden'
            && getComputedStyle(this).display !== 'none'
        )
    }
    """

    ELEMENT_ON_TOP = """
    function() {
        const rect = this.getBoundingClientRect();
        const elementFromPoint = document.elementFromPoint(
            rect.x + rect.width / 2,
            rect.y + rect.height / 2
        );
        return elementFromPoint === this;
    }
    """

    CLICK = """
    function(){
        clicked = false;
        this.addEventListener('click', function(){
            clicked = true;
        });
        this.click();
        return clicked;
    }
    """

    CLICK_OPTION_TAG = """
    document.querySelector('option[value="{self.value}"]').selected = true;
    var selectParentXpath = (
        '//option[@value="{self.value}"]//ancestor::select'
    );
    var select = document.evaluate(
        selectParentXpath,
        document,
        null,
        XPathResult.FIRST_ORDERED_NODE_TYPE,
        null
    ).singleNodeValue;
    var event = new Event('change', { bubbles: true });
    select.dispatchEvent(event);
    """

    BOUNDS = """
    function() {
        return JSON.stringify(this.getBoundingClientRect());
    }
    """

    FIND_RELATIVE_XPATH_ELEMENT = """
        function() {
            return document.evaluate(
                "{escaped_value}", this, null,
                XPathResult.FIRST_ORDERED_NODE_TYPE, null
            ).singleNodeValue;
        }
    """

    FIND_XPATH_ELEMENT = """
        var element = document.evaluate(
            "{escaped_value}", document, null,
            XPathResult.FIRST_ORDERED_NODE_TYPE, null
        ).singleNodeValue;
        element;
    """

    FIND_RELATIVE_XPATH_ELEMENTS = """
        function() {
            var elements = document.evaluate(
                "{escaped_value}", this, null,
                XPathResult.ORDERED_NODE_SNAPSHOT_TYPE, null
            );
            var results = [];
            for (var i = 0; i < elements.snapshotLength; i++) {
                results.push(elements.snapshotItem(i));
            }
            return results;
        }
    """

    FIND_XPATH_ELEMENTS = """
        var elements = document.evaluate(
            "{escaped_value}", document, null,
            XPathResult.ORDERED_NODE_SNAPSHOT_TYPE, null
        );
        var results = [];
        for (var i = 0; i < elements.snapshotLength; i++) {
            results.push(elements.snapshotItem(i));
        }
        results;
    """

    QUERY_SELECTOR = 'document.querySelector("{selector}");'

    RELATIVE_QUERY_SELECTOR = """
        function() {
            return this.querySelector("{selector}");
        }
    """

    QUERY_SELECTOR_ALL = 'document.querySelectorAll("{selector}");'

    RELATIVE_QUERY_SELECTOR_ALL = """
        function() {
            return this.querySelectorAll("{selector}");
        }
    """
