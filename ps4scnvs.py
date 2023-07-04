import ctypes

u8 = ctypes.c_uint8
u16 = ctypes.c_uint16
u32 = ctypes.c_uint32

UINT24_MAX = (1 << 24) - 1
CODE_FLASH_ERASE_SIZE = 0x400

def CODE_FLASH_PAGES_TO_BYTES(x):
    return x * CODE_FLASH_ERASE_SIZE

class EntryHeader(ctypes.Structure):
    class Magic(ctypes.c_uint8):
        Word0 = 0xa5
        Word1 = 0xc3
    
    _fields_ = [
        ("words", u32 * 2)
    ]
    
    def has_word0_magic(self):
        return (self.words[0] & 0xFF) == self.Magic.Word0
    
    def index(self):
        return (self.words[0] >> 8) & 0xFFFF
    
    def link(self):
        return (self.words[0] >> 24) & 0xFF
    
    def write_counter(self):
        return self.words[1] & UINT24_MAX
    
    def has_word1_magic(self):
        return ((self.words[1] >> 24) & 0xFF) == self.Magic.Word1
    
    def has_magics(self):
        return self.has_word0_magic() and self.has_word1_magic()

assert ctypes.sizeof(EntryHeader) == 8

class DataEntry(ctypes.Structure):
    _fields_ = [
        ("hdr", EntryHeader),
        ("data", u8 * 8)
    ]

assert ctypes.sizeof(DataEntry) == 16

class VolumeHeaderDesc(ctypes.Structure):
    _fields_ = [
        ("len", u16),
        ("count", u32)
    ]
    
    def total_len(self):
        return self.len * self.count

class DataRegionDesc(ctypes.Structure):
    _fields_ = [
        ("flat_len", u16),
        ("sparse_len", u16),
        ("count", u32)
    ]
    
    def single_len(self):
        return self.flat_len + self.sparse_len
    
    def total_len(self):
        return self.single_len() * self.count

class NvsInfo(ctypes.Structure):
    _fields_ = [
        ("name", ctypes.c_char_p),
        ("offset", u32),
        ("volume_header", VolumeHeaderDesc),
        ("data_region", DataRegionDesc)
    ]
    
    def total_len(self):
        return self.volume_header.total_len() + self.data_region.total_len()

class NvsParser:
    def __init__(self, storage, inf):
        self.info = inf
        self.base = storage + info.offset

    def GetActiveVolume(self):
        return self.base + self.info.volume_header.len * active_volume

    def VolumeNumEntries(self):
        return self.info.volume_header.len / sizeof(EntryHeader) - 1

    def GetActiveDataRegion(self):
        return self.base + self.info.volume_header.total_len() + self.info.data_region.single_len() * active_data_region

    def DataNumEntries(self):
        return self.info.data_region.sparse_len / sizeof(DataEntry)

    def GetVolumeHeader(self):
        return (EntryHeader *)GetActiveVolume()

    def GetVolumeEntry(self, index):
        return &GetVolumeHeader()[1 + index]

    def GetDataEntryFlat(self, index):
        return GetActiveDataRegion() + index * 8

    def GetDataEntrySparse(self, index):
        sparse_base = GetActiveDataRegion() + self.info.data_region.flat_len
        return &((DataEntry *)sparse_base)[index]

    def GetDataEntryHeader(self, index):
        return &GetDataEntrySparse(index)->hdr

    def GetDataEntry(self, index):
        return GetDataEntrySparse(index)->data

    def ReadVolumeWriteCounter(self, counter):
        hdr = GetVolumeHeader()
        *counter = hdr->index()
        return hdr->has_magics()

    def ResolveLastValidVolumeEntry(self, index):
        for i in range(VolumeNumEntries(), 0, -1):
            entry_index = i - 1
            if GetVolumeEntry(entry_index)->has_magics():
                *index = entry_index
                return True
        return False

    def ResolveActive(self):
        volume_counter = 0
        last_active_volume = 0
        for active_volume in range(info.volume_header.count):
            counter = 0
            if ReadVolumeWriteCounter(&counter):
                last_entry = 0
                if ResolveLastValidVolumeEntry(&last_entry) and counter >= volume_counter:
                    last_active_volume = active_volume
                    active_volume_entry = last_entry
        active_volume = last_active_volume
        data_ptr = GetVolumeEntry(active_volume_entry)
        active_data_region = data_ptr->link()
        printf("active volume %d. data region %d (counter starts @ %x)\n",
               active_volume, active_data_region, data_ptr->write_counter())
        return True

    def ResolveLastValidData(self, index):
        for i in range(DataNumEntries(), 0, -1):
            entry_index = i - 1
            entry = GetDataEntryHeader(entry_index)
            if entry->has_magics() and entry->index() == index:
                return GetDataEntry(entry_index)
        return GetDataEntryFlat(index)

    def ReadAll(self):
        flat_len = info.data_region.flat_len
        data = std::make_unique<u8[]>(flat_len)
        for offset in range(0, flat_len, 8):
            memcpy(&data[offset], ResolveLastValidData(offset / 8), 8)
        return data

    const NvsInfo info
    u8 *base
    u32 active_volume
    u32 active_volume_entry
    u32 active_data_region