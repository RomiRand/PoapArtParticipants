import cv2
import numpy as np
import requests

palette = ["FFFFFF","F3F3F4","E7E7EA","DBDBDF","CFCFD4","C3C3C9","B7B7BF","ABABB4","9F9FA9","93939E","878794","7B7B89","6F6F7E","636373","575769","4B4B5E","F9F9F9","E8E8E8","D8D8D8","C7C7C7","B7B7B7","A6A6A6","959595","858585","747474","646464","535353","424242","323232","212121","111111","000000","FFF0DC","FEEAD5","FDE5CE","FCDFC7","FADABF","F9D4B8","F8CFB1","F7C9AA","F1BB9E","EAAE93","E4A088","DE937C","D78571","D17765","CA6A5A","C45C4E","EADCDA","DEC9C5","D1B6B1","C5A39C","B88F88","AC7C73","9F695F","93564A","885045","7C4940","71433B","663D36","5A3630","4F302B","432926","382321","FFD4D4","FDB6B6","FC9797","FA7979","F95B5B","F73D3D","F61E1E","F40000","E00000","CB0000","B70000","A30101","8E0101","7A0101","650101","510101","FFE1CC","FFD0AF","FFBE92","FFAD75","FF9B57","FF8A3A","FF781D","FF6700","EF6202","DF5D04","CF5805","BF5307","AF4E09","9F490B","8F440C","7F3F0E","FFF8E1","FFF3C7","FFEEAD","FFE993","FFE57A","FFE060","FFDB46","FFD62C","EEC72A","DEB928","CDAA26","BD9C24","AC8D21","9B7E1F","8B701D","7A611B","FFFACF","FFF9BE","FFF9AE","FFF89D","FEF78C","FEF67B","FEF66B","FFF200","EDE002","DCCE04","CABC06","B9AA08","A79709","95850B","84730D","72610F","F1FFCF","E7FFB1","DCFF94","D2FF76","C7FF59","BDFF3B","B2FF1E","A8FF00","9BEA01","8ED401","81BF02","74AA02","669403","597F03","4C6904","3F5404","C5FFC5","AEFAAE","96F596","7FF07F","68EC68","51E751","39E239","22DD22","20CB20","1DBA1D","1BA81B","189618","168416","147314","116111","0F4F0F","CAFFF6","ADFFF2","90FFEE","73FFEA","57FFE6","3AFFE2","1DFFDE","00FFDA","01E7C5","01CFB1","02B79C","039F88","038773","046F5E","04574A","053F35","E1FEFF","CBF9FF","B5F5FF","9FF0FF","8AEBFF","74E6FF","5EE2FF","48DDFF","40CCEB","38BCD7","2FABC3","279BB0","1F8A9C","167988","0E6974","065860","D4DEFF","B6C2FF","97A6FF","798AFF","5B6DFF","3D51FF","1E35FF","0019FF","0016EB","0113D7","0110C3","010EB0","010B9C","020888","020574","020260","F0E3FF","E3C3FF","D6A2FF","C982FF","BC61FF","AF41FF","A220FF","9500FF","8700E9","7900D3","6B00BD","5E00A7","500091","42007B","340065","26004F","FFE3FC","FFD0F8","FFBDF4","FFAAF0","FF98ED","FF85E9","FF72E5","FF5FE1","F056D3","E04DC6","D144B8","C23BAB","B2329D","A3298F","932082","841774","F9E1ED","FAC8DE","FBAFCF","FC96C0","FC7CB2","FD63A3","FE4A94","FF3185","EB2D7B","D72A71","C32667","B0225E","9C1E54","881A4A","741740","601336"]


def getAddressAtPos(x, y):
    url = 'https://api.poap.art/canvas/ethereum-protocol-upgrade-london/pixel/' + str(x) + ',' + str(y)
    page = requests.get(url)
    if page.status_code != 200:
        return ""
    if page.json()["ens"]:
        addr = page.json()["ens"]
    else:
        addr = page.json()["wallet"]
    return addr


def scanArea(x, y, last_x, last_y):
    addresses = set()
    for cur_h in range(y, last_y + 1):
        for cur_w in range(x, last_x + 1):
            a = getAddressAtPos(cur_w, cur_h)
            if a != "":
                addresses.add(a)
    return addresses


def getCanvas():
    url = "https://api.poap.art/canvas/ethereum-protocol-upgrade-london"
    info_json = requests.get(url).json()
    resolution = info_json["rows"], info_json["cols"], info_json["chunkSize"]
    return resolution


global img

def getChunk(row, col, res):
    url = "https://api.poap.art/canvas/ethereum-protocol-upgrade-london/chunk/" + str(row) + ":" + str(col)
    content = requests.get(url).content
    counter = 0
    for b in content:
        color = palette[b]
        new_pixel = tuple(int(color[i:i + 2], 16) for i in (4, 2, 0))
        img[int(counter / res) + row * res, counter % res + col * res] = new_pixel
        counter += 1


#global mousedown


def onMouseEvent(event, x, y, flags, param):
    global img
    # if event == cv2.EVENT_RBUTTONDOWN:
    #    mousedown = True
    # if event == cv2.EVENT_RBUTTONUP:
    #    mousedown = False
    if event == cv2.EVENT_MOUSEMOVE and key == 's':
        img[y, x] = [0, 0, 255]
        return
        # print(str(x) + ", " + str(y))


global key


def draw():
    global img, key
    mousedown = False
    info = getCanvas()
    img = np.full((info[0] * info[2], info[1] * info[2], 3), 255, np.uint8)
    for col in range(info[1]):
        for row in range(info[0]):
            getChunk(row, col, info[2])

    cv2.namedWindow('bild', cv2.WINDOW_NORMAL)
    cv2.setMouseCallback('bild', onMouseEvent)
    key = ''
    while key != 'q':
        k = cv2.waitKey(1)
        cv2.imshow('bild', img)
        if k != -1:
            key = chr(k)
        else:
            key = ''
    cv2.destroyAllWindows()


if __name__ == '__main__':
    draw()
    addr = set()
    # addr = addr.union(scanArea(114, 7, 132, 127))  # tower
    # addr = addr.union(scanArea(61, 89, 94, 121))  # dog

    print("\n".join(str(a) for a in addr))

# more detailed tower:
# addr = addr.union(scanArea(111, 36, 111, 38))  # left-left
# addr = addr.union(scanArea(112, 19, 113, 40))  # left
# addr = addr.union(scanArea(113, 41, 113, 41))  # left-left-bottom
# addr = addr.union(scanArea(133, 7, 134, 40))  # right
# addr = addr.union(scanArea(135, 36, 135, 38))  # right-right
# addr = addr.union(scanArea(133, 41, 133, 42))  # right-right-bottom
# addr = addr.union(scanArea(121, 7, 142, 18))  # top
# addr = addr.union(scanArea(111, 127, 135, 127))  # bottom-bottom
# addr = addr.union(scanArea(112, 126, 134, 126))  # bottom-2x
# addr = addr.union(scanArea(113, 124, 113, 125))  # bottom-left
# addr = addr.union(scanArea(133, 124, 133, 125))  # bottom-right
# addr = addr.union(scanArea(114, 14, 132, 127))  # main