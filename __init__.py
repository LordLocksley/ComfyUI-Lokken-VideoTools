# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (C) 2026 LordLocksley.
# Created 2026-10-21. See LICENSE and NOTICE.md.

from .post_processing import PostProcessing

NODE_CLASS_MAPPINGS = {
    "LokkenVideoPostProcessing": PostProcessing,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "LokkenVideoPostProcessing": "Video Post Processing — Lokken",
}

WEB_DIRECTORY = "./web"

__all__ = ["NODE_CLASS_MAPPINGS", "NODE_DISPLAY_NAME_MAPPINGS", "WEB_DIRECTORY"]
