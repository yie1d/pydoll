class TargetCommands:
    """
    A class for managing browser targets using Chrome DevTools Protocol.

    This class provides methods to create commands for interacting with
    browser targets, including creating, activating, attaching to, and closing
    targets through CDP commands.

    Attributes:
        ACTIVATE_TARGET (dict): Template for the
            Target.activateTarget command.
        ATTACH_TO_TARGET (dict): Template for the
            Target.attachToTarget command.
        CLOSE_TARGET (dict): Template for the
            Target.closeTarget command.
        CREATE_TARGET (dict): Template for the
            Target.createTarget command.
        GET_TARGETS (dict): Template for the
            Target.getTargets command.
        GET_TARGET_INFO (dict): Template for the
            Target.getTargetInfo command.
    """

    ACTIVATE_TARGET = {'method': 'Target.activateTarget', 'params': {}}
    ATTACH_TO_TARGET = {'method': 'Target.attachToTarget', 'params': {}}
    CLOSE_TARGET = {'method': 'Target.closeTarget', 'params': {}}
    CREATE_TARGET = {'method': 'Target.createTarget', 'params': {}}
    GET_TARGETS = {'method': 'Target.getTargets', 'params': {}}
    GET_TARGET_INFO = {'method': 'Target.getTargetInfo', 'params': {}}

    @classmethod
    def activate_target(cls, target_id: str) -> dict:
        """
        Generates a command to activate a specific browser target.

        Args:
            target_id (str): The ID of the target to activate.

        Returns:
            dict: The CDP command to activate the target.
        """
        activate_target = cls.ATTACH_TO_TARGET.copy()
        activate_target['params']['targetId'] = target_id
        return activate_target

    @classmethod
    def attach_to_target(cls, target_id: str) -> dict:
        """
        Generates a command to attach to a specific browser target.

        Args:
            target_id (str): The ID of the target to attach to.

        Returns:
            dict: The CDP command to attach to the target.
        """
        attach_to_target = cls.ATTACH_TO_TARGET.copy()
        attach_to_target['params']['targetId'] = target_id
        return attach_to_target

    @classmethod
    def close_target(cls, target_id: str) -> dict:
        """
        Generates a command to close a specific browser target.

        Args:
            target_id (str): The ID of the target to close.

        Returns:
            dict: The CDP command to close the target.
        """
        close_target = cls.CLOSE_TARGET.copy()
        close_target['params']['targetId'] = target_id
        return close_target

    @classmethod
    def create_target(cls, url: str) -> dict:
        """
        Generates a command to create a new browser target with the
        specified URL.

        Args:
            url (str): The URL to navigate to in the new target.

        Returns:
            dict: The CDP command to create a new target.
        """
        create_target = cls.CREATE_TARGET.copy()
        create_target['params']['url'] = url
        return create_target

    @classmethod
    def get_targets(cls) -> dict:
        """
        Generates a command to retrieve information about all
        available targets.

        Returns:
            dict: The CDP command to get all targets.
        """
        return cls.GET_TARGETS
