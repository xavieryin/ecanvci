from .ecanvci import VciInitConfig, VciDevice, VciCanObj
from ctypes import byref
import threading
import queue
import signal
import time


class ECanVciHelper:
    def __init__(self, config=VciInitConfig(), log=False):
        def signal_handler(sig, frame):
            print('You pressed Ctrl+C!')
            self.stop()

        signal.signal(signal.SIGINT, signal_handler)

        self.log = log
        self.device = VciDevice(config=config)
        self.evt = threading.Event()
        self.q = queue.Queue()
        self.t = threading.Thread(target=self.thread_main, daemon=True)
        self.out_q = queue.Queue()
        self.t.start()

    def thread_main(self):
        while not self.evt.is_set():
            recv_msg = VciCanObj(SendType=0)
            while self.device.receive_by_ref(byref(recv_msg), 1, 0):
                if self.log:
                    print(f">>> {hex(recv_msg.ID)} {list(recv_msg.Data[:recv_msg.DataLen])}")
                self.out_q.put(recv_msg)
            try:
                msg = self.q.get(timeout=0.1)
                assert(self.device.transmit_by_ref(byref(msg), 1) == 1)
                if self.log:
                    print(f"<<< {hex(msg.ID)} {list(msg.Data[:msg.DataLen])}")
            except queue.Empty:
                pass
        print("thread exit")

    def stop(self):
        print("stopping")
        self.evt.set()
        while self.t.is_alive():
            self.t.join(timeout=1)
        self.device.close()

    def send(self, id=0, data=(0,)*8):
        self.q.put(VciCanObj(ID=id, Data=data, DataLen=len(data)))

    def send_vcicanobj(self, obj):
        self.q.put(obj)

    def recv(self, block=True, timeout=None):
        return self.out_q.get(block, timeout)

    def clear_recv_queue(self):
        try:
            while self.out_q.get_nowait():
                pass
        except:
            pass

    def wait_for_send(self):
        while not self.q.empty():
            time.sleep(0.1)

    def keep_running(self):
        while self.t.is_alive():
            self.t.join(timeout=0.1)


'''
def _simple_demo():
    import time

    config=VciInitConfig(Mode=2)
    can = ECanVciHelper(config=config)    # Mode=2 means CAN bus self-loop

    print("press CTRL+C to exit")

    for i in range(5):
        can.send(id=i)
        time.sleep(1)

    for i in range(5):
        recv_msg = can.recv()
        print(recv_msg.ID, bytearray(recv_msg.Data))

    can.keep_running()

    print("main exit")


if __name__ == "__main__":
    _simple_demo()
'''