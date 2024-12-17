from __future__ import annotations

from typing import TYPE_CHECKING, Any, Literal

import fsspec

from app.config.app import settings

if TYPE_CHECKING:
    from asyncio import AbstractEventLoop


DEFAULT_OPTIONS: dict[str, Any] = {}


class StorageConfig:
    """Class to store and configure storage backends."""

    def __init__(self, fs_type: Literal["file", "gs"] = "file", fs_options: dict[str, Any] | None = None) -> None:
        """Storage Bucket."""
        self.fs_type = fs_type
        self.fs_options = fs_options or {}


config = StorageConfig(fs_type=settings.storage.FS_TYPE)  # , fs_options=settings.storage.FS_OPTIONS)


def get_fs(loop: AbstractEventLoop | None = None) -> fsspec.AbstractFileSystem:
    """Get a fsspec filesystem."""
    async_kwargs = {"asynchronous": True, "loop": loop} if loop else {}
    # if settings.storage.FS_TYPE == "gs":
    # return fsspec.filesystem(
    #     "gs",
    #     project=settings.gcp.PROJECT,
    #     requests_timeout=120,
    #     token=settings.gcp.CREDENTIALS,
    #     auto_mkdir=True,
    #     session_kwargs={"trust_env": True},
    #     **async_kwargs,
    # )
    # elif settings.storage.FS_TYPE == "minio":

    return fsspec.filesystem(
        "file",
        auto_mkdir=True,
        **async_kwargs,
    )
