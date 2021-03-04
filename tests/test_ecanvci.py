import unittest

import ecanvci


class TestECanVci(unittest.TestCase):
    def test_is_string(self):
        device = ecanvci.VciDevice(config=ecanvci.VciInitConfig(Mode=2))    # Mode=2 means CAN bus self-loop
        obj = ecanvci.VciCanObj()
        for i in range(5):
            obj.Data[0] = i
            device.transmit(obj)
            ret, recv_msg = device.receive(waittime=-1)
            # print(ret, recv_msg.ID, bytearray(recv_msg.Data), bytearray(obj.Data))
            self.assertTrue(ret == 1)
            self.assertTrue(recv_msg.ID == obj.ID)
            self.assertTrue(bytearray(recv_msg.Data) == bytearray(obj.Data))
        device.close()


if __name__ == '__main__':
    unittest.main()