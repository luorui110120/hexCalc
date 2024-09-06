import time,sys,hashlib,struct,random,base64,json

def get_current_time():
    return "%d" % int(round(time.time() * 1000))

def strToList(strbuf):
    strByteList=[]
    for i in strbuf:
        strByteList.append(ord(i))
    return strByteList

def stringTobytes(str):
    if sys.version > '3':
        return bytes(str,encoding='utf8')
    else:
        return str
def bytesToString(bs):
    if sys.version > '3':
        return bytes.decode(bs,encoding='utf8')
    else:
        return bs;

def bytesToHexString(bs):
    if sys.version > '3':
        return ''.join(['%02X' % b for b in bs])
    else:
        return bs.encode('hex')

def hexStringTobytes(str):
    if sys.version > '3':
        str = str.replace(" ", "")
        return bytes.fromhex(str)
    else:
        return str.decode('hex')


def stringToHexString(str):
    strbyte = str
    if sys.version > '3':
        strbyte = stringTobytes(str)
    else:
        strbyte = strbyte
    return bytesToHexString(strbyte)
def listToStrHex(listbyte):
    retstr=bytes()
    for i in listbyte:
        retstr += struct.pack("B",i &0xff)
    return retstr.hex()
def byteToList(bs):
    if sys.version > '3':
        return list(bs)
    else:
        strByteList=[]
        for i in bs:
            strByteList.append(ord(i))
        return strByteList
    #return list(bs)
def listToBytes(l):
    if sys.version > '3':
        newlist=[]
        for i in l:
            newlist.append(i &0xff)
        return bytes(newlist)
    else:
        import struct
        retstr=bytes()
        for i in l:
            retstr += struct.pack("B",i &0xff)
        return retstr


def list_to_hex(inlist):
    retout = ''
    for val in inlist:
        if val < 0x10:
            retout = retout + '0' + ('%x' % val)
        else:
            retout = retout + ('%x' % val)
    return retout


def is_dic_key(indic, inkey):
    if sys.version >'3':
        return inkey in indic
    else:
        return indic.has_key(inkey)

###获取随机的hex值
def get_rand_hex(n):
    """
    输入hex 的长度n
    :return:
    """
    c_length = int(n)
    source = '0123456789abcdef'
    length = len(source) - 1
    result = ''
    for i in range(c_length):
        result += source[random.randint(0, length)]
    return result
def get_md5(instr):
    md5hash = hashlib.md5()
    md5hash.update(instr.encode('utf8'))
    return md5hash.digest()

def get_md5hex(instr):
    md5hash = hashlib.md5()
    md5hash.update(instr.encode('utf8'))
    return md5hash.hexdigest()

def inputlistdata(inhandle, intype, insrc, indes, inbods):
    outdir={}
    outdir['handle'] = '%d' % inhandle
    outdir['type'] = intype
    outdir['src'] = '%s:%d' % insrc
    outdir['des'] = '%s:%d' % indes
    # bodys = b''
    # if inhandle % 5 > 0:
    #     for i in range(3):
    #         bodys += get_md5(get_current_time() + get_rand_hex(10))
    # else:
    #     for i in range(0x20):
    #         bodys += get_md5(get_current_time() + get_rand_hex(10))
    #hexdata = hexdump.hexdump(stringTobytes(databuf), 'return')
    outdir['bodybase64'] = bytesToString(base64.b64encode(inbods))
    return json.dumps(outdir)

def int_to_bytes(value, length):
    result = []
    for i in range(0, length):
        result.append(value >> (i * 8) & 0xff)
    #result.reverse()
    return listToBytes(result)

def bytes_to_int(inbytes):
    result = 0
    index = 0
    for b in inbytes:
        if sys.version > '3':
            result = result + (int(b) << index)
        else:
            import struct
            result = result +  ((struct.unpack("B",b)[0]) << index)
        index += 8
    return result
###将有符号转化为无符号
def int_to_uint(inval:int):
    s_hex_neg = struct.pack('l', inval)
    return int.from_bytes(s_hex_neg, byteorder='little', signed=False)

###将无符号转化为有符号
def uint_to_int(uinval:int):
    s_hex_neg = struct.pack('L', uinval)
    return int.from_bytes(s_hex_neg, byteorder='little', signed=True)

#### uleb128 ->uint
def uleb128_to_uint(content):
    value = 0
    for i in range(5):
        tmp = content[i] & 0x7f
        value = tmp << (i * 7) | value
        if (content[i] & 0x80) != 0x80:
            break
    if i == 4 and (tmp & 0xf0) != 0:
        print("parse a error uleb128 number")
        return -1
    return value


####  uint->uleb128
def uint_to_uleb128(incount):
    listout = []

    for i in range(5):
        if (incount >> 7) > 0:
            tmp1 = incount & 0x7f | 0x80
            listout.append(tmp1)
            incount = incount >> 7
        else:
            if (incount & 0x7f) > 0:
                listout.append(incount & 0x7f)
            break;
    return bytes(listout);


#### int ->leb128
def int_to_leb128(x):
    listout = []
    i = 1
    while i:
        t = x & 0x7f
        x >>= 7
        if ((x == 0) and (t & 0x40) == 0) or (x == -1 and (t & 0x40)):
            i = 0
        else:
            t |= 0x80
        listout.append(t)
    return bytes(listout)


#### leb128 ->int
def leb128_to_int(content):
    value = 0

    mask = [0xffffff80, 0xffffc000, 0xffe00000, 0xf0000000, 0]
    bitmask = [0x40, 0x40, 0x40, 0x40, 0x8]
    value = 0
    for i in range(5):
        tmp = (content[i]) & 0x7f
        value = tmp << (i * 7) | value
        if ((content[i]) & 0x80) != 0x80:
            if bitmask[i] & tmp:
                value |= mask[i]
            break
    if i == 4 and (tmp & 0xf0) != 0:
        print("parse a error uleb128 number")
        return -1
    buffer = struct.pack("I", value)
    value, = struct.unpack("i", buffer)
    return value


def floatToHex(floatValue):  # float转16进制
    return struct.pack('<f', floatValue).hex()


def hexToFloat(hexString):  # 16进制转float
    return struct.unpack('<f', bytes.fromhex(hexString))[0]


def doubleToHex(doubleValue):  # double转16进制
    return struct.pack('<d', doubleValue).hex()


def hexToDouble(hexString):  # 16进制转double
    return struct.unpack('<d', bytes.fromhex(hexString))[0]