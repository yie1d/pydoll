import copy
from pathlib import Path
from typing import Union, List, Optional


class FileUploadCommands:
    SET_FILE_INPUT_FILES_TEMPLATE = {'method': 'DOM.setFileInputFiles', 'params': {}}

    @staticmethod
    def _ensure_file_exists(files: Union[str, Path, List[Union[str, Path]]]) -> List[str]:
        """
        Ensures that the file exists.
        
        Args:
            files (Union[str, Path, List[Union[str, Path]]]): Files to check.

        Returns:
            List[str]: List of file paths.
        """
        if isinstance(files, str):
            files = [Path(files).absolute()]
        elif isinstance(files, Path):
            files = [files]
        
        _has_ensure_files = []
        for filepath in files:
            if isinstance(filepath, str):
                filepath = Path(filepath).absolute()
            if filepath.is_file() is False:
                raise FileExistsError(f"{filepath} does not exist.")
            _has_ensure_files.append(str(filepath))
        
        return _has_ensure_files
    
    @classmethod
    def upload_files(
            cls,
            files: Union[str, Path, List[Union[str, Path]]],
            object_id: Optional[str] = None,
            backend_node_id: Optional[str] = None
    ) -> dict:
        """
        Sets the value of the file input to these file paths or files.
        
        Args:
            files (Union[str, Path, List[Union[str, Path]]): Files to upload.
            object_id (Optional[str]): JavaScript object id of the node wrapper.
            backend_node_id (Optional[str]): Identifier of the backend node.

        Returns:
            dict: The CDP command to set the file input files.
        """
        command = copy.deepcopy(cls.SET_FILE_INPUT_FILES_TEMPLATE)
        if object_id is None and backend_node_id is None:
            raise ValueError("Either object_id or backend_node_id is required.")
        if object_id is not None:
            command['params']['objectId'] = object_id
        if backend_node_id is not None:
            command['params']['backendNodeId'] = backend_node_id
        command['params']['files'] = cls._ensure_file_exists(files)

        return command
