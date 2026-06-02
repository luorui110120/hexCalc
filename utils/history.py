# -*- coding: utf-8 -*-
import json
import os
import time
from collections import deque

from PyQt5.QtCore import QTimer


HISTORY_DIR = os.path.expanduser('~/.hexcalc')
HISTORY_FILE = os.path.join(HISTORY_DIR, 'history.json')
MAX_RECORDS = 100
SAVE_DEBOUNCE_MS = 500


class HistoryManager:
    _instance = None

    @classmethod
    def instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def __init__(self):
        self._records = deque(maxlen=MAX_RECORDS)
        self._save_timer = QTimer()
        self._save_timer.setSingleShot(True)
        self._save_timer.setInterval(SAVE_DEBOUNCE_MS)
        self._save_timer.timeout.connect(self._flush)

    def load(self):
        if not os.path.isfile(HISTORY_FILE):
            return
        try:
            with open(HISTORY_FILE, 'r', encoding='utf-8') as f:
                data = json.load(f)
            if isinstance(data, list):
                self._records.clear()
                for rec in data[-MAX_RECORDS:]:
                    if self._valid(rec):
                        self._records.append(rec)
        except Exception:
            pass

    def all(self):
        return list(self._records)

    def add(self, op, label, inputs, result, outputs=None):
        inputs = [str(x) for x in inputs]
        record = {
            'op': op,
            'label': label,
            'inputs': inputs,
            'result': str(result),
            'outputs': outputs or {},
            'ts': int(time.time()),
        }
        if self._records:
            last = self._records[-1]
            if last['op'] == op and self._is_prefix_continuation(last['inputs'], inputs):
                self._records[-1] = record
                self._schedule_save()
                return True
            if last['op'] == op and last['inputs'] == inputs and last['result'] == record['result']:
                return False
        self._records.append(record)
        self._schedule_save()
        return True

    def clear(self):
        self._records.clear()
        self._flush()

    @staticmethod
    def _valid(rec):
        return (
            isinstance(rec, dict)
            and isinstance(rec.get('op'), str)
            and isinstance(rec.get('inputs'), list)
            and isinstance(rec.get('result'), str)
        )

    @staticmethod
    def _is_prefix_continuation(old_inputs, new_inputs):
        if len(old_inputs) != len(new_inputs):
            return False
        if old_inputs == new_inputs:
            return True
        any_extension = False
        for a, b in zip(old_inputs, new_inputs):
            if a == b:
                continue
            if b.startswith(a) and len(b) > len(a):
                any_extension = True
                continue
            if a.startswith(b) and len(a) > len(b):
                any_extension = True
                continue
            return False
        return any_extension

    def _schedule_save(self):
        self._save_timer.start()

    def _flush(self):
        try:
            os.makedirs(HISTORY_DIR, exist_ok=True)
            tmp = HISTORY_FILE + '.tmp'
            with open(tmp, 'w', encoding='utf-8') as f:
                json.dump(list(self._records), f, ensure_ascii=False, indent=2)
            os.replace(tmp, HISTORY_FILE)
        except Exception:
            pass
