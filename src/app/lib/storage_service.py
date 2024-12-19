from __future__ import annotations

import asyncio
import contextlib
from collections.abc import AsyncIterator
from typing import TYPE_CHECKING, TypeVar

from litestar.utils.sync import AsyncCallable

from app.lib import storage
from app.lib.exceptions import ApplicationError

if TYPE_CHECKING:
    from litestar.datastructures import UploadFile

FileStorageServiceT = TypeVar("FileStorageServiceT", bound="FileStorageService")


class FileExtensionNotAllowedError(ApplicationError):
    """File Extension not allowed."""


class FileIncompleteError(ApplicationError):
    """File Incomplete due to errors during extraction."""


class FileExceedsMaxSizeError(ApplicationError):
    """File Extension not allowed."""


class FileStorageService:
    """File Handler.

    Uploads and downloads to the defined backend

    """

    def __init__(self, uploads_dir: str, allow_extensions: list[str] | None = None, max_size: int = 1024**3) -> None:
        """Upload Files to a storage backend.

        Args:
            uploads_dir (str): _description_
            allow_extensions (list[str] | None, optional): _description_. Defaults to None.
            max_size (int, optional): _description_. Defaults to 1024**3.
        """
        self.max_size = max_size
        self.allow_extensions = allow_extensions
        self.uploads_dir = uploads_dir

    def remove(self, path: str) -> None:
        """Remove a file or directory."""
        fs = storage.get_fs()
        fs.rm(path=path, recursive=True)

    async def upload(self, files: list[UploadFile], path: str | None = None) -> list[str]:
        """Upload file."""
        upload_tasks: list[asyncio.Task[str]] = []
        if path is None:
            path = ""
        for f in files:
            filename = f"{self.uploads_dir}/{path}/{f.filename}"

            upload_tasks.append(asyncio.create_task(self._upload_file(filename, f)))
        return await asyncio.gather(*upload_tasks)

    async def _upload_file(self, filename: str, file: UploadFile) -> str:
        """Upload file."""
        valid_file_ext = False
        if self.allow_extensions:
            for ext in self.allow_extensions:
                if file.filename.endswith(ext):
                    valid_file_ext = True
                    break
        if not valid_file_ext:
            msg = f"File extension is not allowed.  It must be of one of the following: {','.join(self.allow_extensions or [])}"
            raise FileExtensionNotAllowedError(
                msg,
            )
        file_size = len(await file.read())
        await file.seek(0)  # reset file for the upload
        if file_size > self.max_size:
            msg = f"File size {file_size} exceeds max size {self.max_size}"
            raise FileExceedsMaxSizeError(
                msg,
            )
        fs = storage.get_fs()
        content = await file.read()
        await AsyncCallable(fs.pipe_file)(filename, content)
        return filename

    @classmethod
    @contextlib.asynccontextmanager
    async def new(
        cls: type[FileStorageServiceT],
        uploads_dir: str = "data/uploads",
        allow_extensions: list[str] = ["zip", "tar.gz", "tgz", "tar"],  # noqa: B006
    ) -> AsyncIterator[FileStorageServiceT]:
        """Context manager that returns instance of file storage service.

        Returns:
            The service object instance.
        """
        try:
            yield cls(uploads_dir, allow_extensions)
        finally:
            ...
