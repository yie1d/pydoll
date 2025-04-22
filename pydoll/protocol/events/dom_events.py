class DomEvents:
    """
    A class to define the DOM events available through the
    Chrome DevTools Protocol (CDP). These events allow for monitoring
    changes and updates within the Document Object Model (DOM)
    of a web page, enabling developers to react to specific
    modifications and interactions with the DOM elements.
    """

    ATTRIBUTE_MODIFIED = 'DOM.attributeModified'
    """
    Event triggered when an attribute of a DOM node is modified.

    This event provides information about the node affected and the
    attribute that was changed. It is part of the CDP's capabilities
    for tracking DOM changes and allows developers to respond
    to attribute modifications in real time.
    """

    ATTRIBUTE_REMOVED = 'DOM.attributeRemoved'
    """
    Event triggered when an attribute of a DOM node is removed.

    This event indicates that an attribute has been deleted from a
    node, allowing developers to manage state or perform cleanup
    based on the changes. It is supported by the CDP to ensure
    developers can monitor DOM manipulations effectively.
    """

    CHARACTER_DATA_MODIFIED = 'DOM.characterDataModified'
    """
    Event triggered when the character data of a DOM node is modified.

    This event informs listeners about changes in the text content
    of a node, which is essential for applications that need to
    reflect real-time updates in the UI based on data changes.
    """

    CHILD_NODE_COUNT_UPDATED = 'DOM.childNodeCountUpdated'
    """
    Event triggered when the number of child nodes of a DOM node is updated.

    This event alerts developers when the number of children changes,
    allowing them to react to structural changes in the DOM tree.
    """

    CHILD_NODE_INSERTED = 'DOM.childNodeInserted'
    """
    Event triggered when a new child node is inserted into a DOM node.

    This event notifies listeners of new additions to the DOM,
    enabling actions such as updating UI components or handling
    related data.
    """

    CHILD_NODE_REMOVED = 'DOM.childNodeRemoved'
    """
    Event triggered when a child node is removed from a DOM node.

    This event indicates that a child has been deleted, allowing
    developers to manage their state or trigger updates based on
    the removal of elements in the DOM.
    """

    DOCUMENT_UPDATED = 'DOM.documentUpdated'
    """
    Event triggered when the DOM document is updated.

    This event signifies that changes have occurred at the document
    level, prompting developers to refresh or update their views
    accordingly.
    """

    SCROLLABLE_FLAG_UPDATED = 'DOM.scrollableFlagUpdated'
    """
    Event triggered when the scrollable flag of a DOM node is updated.

    This event is useful for determining which elements in the DOM
    can be scrolled, allowing for enhanced user interactions and
    responsive designs.
    """

    SHADOW_ROOT_POPPED = 'DOM.shadowRootPopped'
    """
    Event triggered when a shadow root is popped from the stack.

    This event indicates that a shadow DOM context has been removed,
    which is relevant for applications utilizing shadow DOM features
    for encapsulated styling and markup.
    """

    SHADOW_ROOT_PUSHED = 'DOM.shadowRootPushed'
    """
    Event triggered when a shadow root is pushed onto the stack.

    This event signifies that a new shadow DOM context has been
    created, allowing developers to manage and respond to changes
    in encapsulated DOM structures.
    """

    TOP_LAYER_ELEMENTS_UPDATED = 'DOM.topLayerElementsUpdated'
    """
    Event triggered when the top layer elements in the DOM are updated.

    This event allows for monitoring changes in the most visible
    elements in the DOM, which is essential for managing UI states
    and rendering updates.
    """
