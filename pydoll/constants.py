from enum import Enum


class By(str, Enum):
    CSS = 'css'
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
