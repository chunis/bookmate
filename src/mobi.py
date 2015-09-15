#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2015, Chunis Deng (<chunchengfh@gmail.com>)
#
# This file is part of BookMate and is released under the terms of
# GNU GPLv3 License, see doc/LICENSE for details.
#

import os, sys
from struct import unpack, pack, calcsize


# we just care about the interested info, ignore other items
MOBI_HDR_FIELDS = (
		("id", 16, "4s"),
		("header_len", 20, "I"),
		("mobi_type", 24, "I"),
		("encoding", 28, "I"),
		("UID", 32, "I"),
		("generator_version", 36, "I"),
		("reserved", 40, "40s"),
		("first_nonbook_idx", 80, "I"),
		("full_name_offs", 84, "I"),
		("full_name_len", 88, "I"),
		("ignored", 92, "36s"),
		("exth_flags", 128, "I"),
)

EXTH_RECORD_TYPES = {
		1: 'drm server id',
		2: 'drm commerce id',
		3: 'drm ebookbase book id',
		100: 'author',  # list
		101: 'publisher',  # list
		102: 'imprint',
		103: 'description',
		104: 'isbn',  # list
		105: 'subject',  # list
		106: 'publication date',
}

EXTH_FMT = ">4x2I"  # 4x = "EXTH", I = hlen, I = record count

