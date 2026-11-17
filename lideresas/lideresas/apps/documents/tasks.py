from collections.abc import Iterable
from pathlib import Path

from django.core.files.base import File


def recursive_mkdir(base_path: Path, joins: Iterable[str]) -> Path:
    """Recursive mkdir.

    Description: This function is used to recursively create a directory.

    Args:
        base_path (Path): The base path to create the directory.
        joins (Iterable[str]): The joins to create the directory.

    Returns:
        Path: The path to the directory.

    Example:
        >>> from lideresas.documents.tasks import recursive_mkdir
        >>> recursive_mkdir(base_path=Path("C:/"), joins=["Documents", "Test"])
        WindowsPath('C:/Documents/Test')

        >>> recursive_mkdir(base_path=Path("/"), joins=["Documents", "Test"])   # noqa: E501
        PosixPath('/Documents/Test')
    """

    path = base_path
    for join in joins:
        path = path / join
        path.mkdir(exist_ok=True)
    return path


def bytes_to_file(path: Path, file: File) -> Path | None:
    """Bytes to file.

    Description: This function is used to convert bytes to a file.

    Args:
        path (Path): The path to the file.
        file (File): The file to convert. is a in ram file

    Returns:
        Path | None: The path to the file or None if the conversion failed.

    Example:
        >>> from lideresas.documents.tasks import bytes_to_file
        >>> bytes_to_file(path=Path("C:/test.pdf"), file=File(open("test.pdf", "rb")))
        WindowsPath('C:/test.pdf')

        >>> bytes_to_file(path=Path("/"), file=File(open("test.pdf", "rb")))   # noqa: E501
        PosixPath('/test.pdf')
    """

    try:
        with path.open("wb") as new_file:
            for chunk in file.chunks():
                new_file.write(chunk)
                new_file.flush()
            new_file.close()
            return path
    except Exception:  # noqa: BLE001
        return None
