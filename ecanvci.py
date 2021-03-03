from ctypes import *


class StructureEx(Structure):
    '''Add easy-to-use method to set values to ctypes.structure
    '''
    def from_iterable(self, iter):
        assert(len(iter) == sizeof(self))
        for (field_name, field_type), value in zip(self._fields_, iter):
            setattr(self, field_name, value)

    def from_array(self, arr):
        memmove(addressof(self), addressof(arr), sizeof(self))


class VciInitConfig(StructureEx):
    _fields_ = [("AccCode", c_ulong),
                ("AccMask", c_ulong),
                ("Reserved", c_ulong),
                ("Filter", c_ubyte),
                ("Timing0", c_ubyte),
                ("Timing1", c_ubyte),
                ("Mode", c_ubyte)]  # 0: Normal, 1: Listen-only, 2: Self

    def __init__(self, AccCode=0x00000000, AccMask=0xffffffff, Reserved=0, Filter=0, Timing0=0x01, Timing1=0x1C, Mode=0):
        super(VciInitConfig, self).__init__(AccCode, AccMask, Reserved, Filter, Timing0, Timing1, Mode)


class VciCanObj(StructureEx):
    _fields_ = [("ID", c_uint),
                ("TimeStamp", c_uint),
                ("TimeFlag", c_ubyte),  # is TimeStamp valid
                ("SendType", c_ubyte),  # only meaningful when tranmitting; 0: Normal, 1: Single, 2: Self, 3: Single self
                ("RemoteFlag", c_ubyte),
                ("ExtendFlag", c_ubyte),
                ("DataLen", c_ubyte),
                ("Data", c_ubyte * 8),
                ("Reserved", c_ubyte * 3)]

    def __init__(self, ID=0, TimeStamp=0xffffffff, TimeFlag=0, SendType=1, RemoteFlag=0, ExtendFlag=1, DataLen=8, Data=(0,)*8, Reserved=(0,)*3):
        super(VciCanObj, self).__init__(ID, TimeStamp, TimeFlag, SendType, RemoteFlag, ExtendFlag, DataLen, Data, Reserved)


class VciDevice(WinDLL):
    # nDeviceType => 3: USNCAN-1, 4:USBCAN-2
    def __init__(self, name='./ECanVci64.dll', nDeviceIdx=0, nDeviceType=3, nDeviceInd=0, nReserved=0, config=VciInitConfig()):
        super(VciDevice, self).__init__(name)
        assert(self.OpenDevice(nDeviceType, nDeviceInd, nReserved) == 1)
        assert(self.InitCAN(nDeviceType, nDeviceInd, 0, byref(config)) == 1)
        assert(self.StartCAN(nDeviceType, nDeviceInd, 0) == 1)
        self.nDeviceIdx = nDeviceIdx
        self.nDeviceType = nDeviceType
        self.nDeviceInd = nDeviceInd
        self.nReserved = nReserved

    def close(self):
        assert(self.CloseDevice(self.nDeviceType, self.nDeviceInd) == 1)

    def transmit(self, obj, waittime=0):
        return self.Transmit(self.nDeviceType, self.nDeviceInd, self.nDeviceIdx, byref(obj), 1, waittime)

    def transmit_by_ref(self, obj_ref, len=1, waittime=0):
        return self.Transmit(self.nDeviceType, self.nDeviceInd, self.nDeviceIdx, obj_ref, len, waittime)
    
    def receive(self, waittime=0):
        recv_msg = VciCanObj(SendType=0)
        ret = self.Receive(self.nDeviceType, self.nDeviceInd, self.nDeviceIdx, byref(recv_msg), 1, waittime)
        return ret, recv_msg

    def receiveN(self, len=2, waittime=0):
        recv_msg = VciCanObj * len
        for i in range(len):
            recv_msg[i].SendType = 0
        ret = self.Receive(self.nDeviceType, self.nDeviceInd, self.nDeviceIdx, byref(recv_msg[0]), len, waittime)
        return ret, recv_msg

    def receive_by_ref(self, obj_ref, len=1, waittime=0):
        return self.Receive(self.nDeviceType, self.nDeviceInd, self.nDeviceIdx, obj_ref, len, waittime)




# A simple usage demo
if __name__ == "__main__":
    device = VciDevice(config=VciInitConfig(Mode=2))    # Mode=2 means CAN bus self-loop
    
    obj = VciCanObj()
    for i in range(5):
        obj.Data[0] = i
        device.transmit(obj)
        ret, recv_msg = device.receive(waittime=-1)
        print(ret, recv_msg.ID, bytearray(recv_msg.Data), bytearray(obj.Data))
    device.close()