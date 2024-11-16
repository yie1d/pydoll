class TargetCommands:
    ACTIVATE_TARGET = {'method': 'Target.activateTarget', 'params': {}}
    ATTACH_TO_TARGET = {'method': 'Target.attachToTarget', 'params': {}}
    CLOSE_TARGET = {'method': 'Target.closeTarget', 'params': {}}
    CREATE_TARGET = {'method': 'Target.createTarget', 'params': {}}
    GET_TARGETS = {'method': 'Target.getTargets', 'params': {}}
    GET_TARGET_INFO = {'method': 'Target.getTargetInfo', 'params': {}}

    @classmethod
    def activate_target(cls, target_id: str) -> dict:
        activate_target = cls.ATTACH_TO_TARGET.copy()
        activate_target['params']['targetId'] = target_id
        return activate_target

    @classmethod
    def attach_to_target(cls, target_id: str) -> dict:
        attach_to_target = cls.ATTACH_TO_TARGET.copy()
        attach_to_target['params']['targetId'] = target_id
        return attach_to_target

    @classmethod
    def close_target(cls, target_id: str) -> dict:
        close_target = cls.CLOSE_TARGET.copy()
        close_target['params']['targetId'] = target_id
        return close_target

    @classmethod
    def create_target(cls, url: str) -> dict:
        create_target = cls.CREATE_TARGET.copy()
        create_target['params']['url'] = url
        return create_target

    @classmethod
    def get_targets(cls) -> dict:
        return cls.GET_TARGETS
