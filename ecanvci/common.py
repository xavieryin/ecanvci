from ctypes import Structure, LittleEndianStructure, memmove, addressof, sizeof


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