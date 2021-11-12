from .ecanvci import VciCanObj
import time


class CanRecord(bytearray):
    def add(self, msg:VciCanObj, current=None):
        try:
            current_ms = int(current * 1000)
        except:
            current_ms = int(time.time() * 1000)
        self += bytearray(msg)
        self[-3] = current_ms  & 0xFF
        self[-2] = (current_ms >> 8)  & 0xFF
        self[-1] = (current_ms >> 16)  & 0xFF
        # print(f"{msg.ID}, len(record)={len(self)}")
