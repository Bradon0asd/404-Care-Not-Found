"""Stress detection and the employer notice it triggers.

Its own module, and not part of `chat`, because two callers need it: Tab 03 chat
and Tab 02's private diaries. Folding it into `chat` would make Tab 02 import
Tab 03; folding it into `line` would put business logic inside the messaging
channel. Both callers depend on this module instead, and it depends on neither.

There is no Blueprint here on purpose: nothing about stress is exposed to the
caregiver, and the employer-facing manual push already lives at
`POST /api/line/stress-signals`. This module is called from other services only.
"""
