import unittest
import time

import ecanvci

class TestECanVci(unittest.TestCase):
    def test_helper(self):

        config=ecanvci.VciInitConfig(Mode=2)
        can = ecanvci.ECanVciHelper(config=config)    # Mode=2 means CAN bus self-loop

        print("press CTRL+C to exit")

        for i in range(5):
            can.send(id=i)
            time.sleep(1)

        for i in range(5):
            recv_msg = can.recv()
            # print(recv_msg.ID, bytearray(recv_msg.Data))
            self.assertTrue(recv_msg.ID == i)

        # can.keep_running()
        can.stop()

        print("main exit")


if __name__ == '__main__':
    unittest.main()