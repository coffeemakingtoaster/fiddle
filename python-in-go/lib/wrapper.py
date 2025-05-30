import ctypes
__lib = ctypes.cdll.LoadLibrary('./lib/library.so')

def setup():
    # Declare return types
    __lib.get_context.restype = ctypes.c_char_p

def get_context() -> str:
    result = __lib.get_context()
    return result.decode('utf-8')

if __name__ != "__main__":
    setup()
