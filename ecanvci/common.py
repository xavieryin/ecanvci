from ctypes import Structure, LittleEndianStructure, memmove, addressof, sizeof
import sys

ECANVCI_TIMING = {5: (0xBF, 0xFF),
                  10: (0x31, 0x1C),
                  20: (0x18, 0x1C),
                  40: (0x87, 0xFF),
                  50: (0x09, 0x1C),
                  80: (0x83, 0xFF),
                  100: (0x04, 0x1C), 
                  125: (0x03, 0x1C), 
                  200: (0x81, 0xFA), 
                  250: (0x01, 0x1C),
                  400: (0x80, 0xFA), 
                  500: (0x00, 0x1C),
                  666: (0x80, 0xB6), 
                  800: (0x00, 0x16), 
                  1000: (0x00, 0x14)}

# ECANVCI_TIMING0_100KBPS, ECANVCI_TIMING1_100KBPS = ECANVCI_TIMING[100]
# ECANVCI_TIMING0_250KBPS, ECANVCI_TIMING1_250KBPS = ECANVCI_TIMING[250]
# ECANVCI_TIMING0_500KBPS, ECANVCI_TIMING1_500KBPS = ECANVCI_TIMING[500]

this_module = sys.modules[__name__]
for kbps, timings in ECANVCI_TIMING.items():
    setattr(this_module, f"ECANVCI_TIMING0_{kbps}KBPS", timings[0])
    setattr(this_module, f"ECANVCI_TIMING1_{kbps}KBPS", timings[1])


class StructureEx(Structure):
    '''Add easy-to-use method to set values to ctypes.structure
    '''
    def from_iterable(self, iter):
        assert(len(iter) == sizeof(self))
        for (field_name, field_type), value in zip(self._fields_, iter):
            setattr(self, field_name, value)

    def from_array(self, arr):
        memmove(addressof(self), addressof(arr), sizeof(self))

        
class LEStructureEx(LittleEndianStructure):
    '''Add easy-to-use method to set values to ctypes.structure
    '''
    def from_iterable(self, iter):
        assert(len(iter) == sizeof(self))
        for (field_name, field_type), value in zip(self._fields_, iter):
            setattr(self, field_name, value)

    def from_array(self, arr):
        memmove(addressof(self), addressof(arr), sizeof(self))