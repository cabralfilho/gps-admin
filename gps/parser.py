def parse_message(msg):
    split = msg.split(',')

    if len(split) == 6:
        # 1201010800,,000007V0000.0000N00000.0000E000.000140399,L,imei:355227042061358,8888

        coords = split[2]

        latitude_sign = 1 if coords[16] == 'N' else -1
        longitude_sign = 1 if coords[27] == 'E' else -1

        latitude = latitude_sign * (float(coords[7:9]) + (float(coords[9:16]) / 60))
        longitude = longitude_sign * (float(coords[17:20]) + (float(coords[20:27]) / 60))

        imei = split[4][5:]
    else:
        # 0000000000,+48693150059,GPRMC,172722.000,A,5226.2289,N,01656.0929,E,0.00,223.93,180713,,,A*6C,L,imei:359585015404392,106#Z

        latitude_sign = 1 if split[6] == 'N' else -1
        longitude_sign = 1 if split[8] == 'E' else -1

        latitude = latitude_sign * (float(split[5][0:2]) + (float(split[5][2:]) / 60))
        longitude = longitude_sign * (float(split[7][0:3]) + (float(split[7][3:]) / 60))

        imei = split[16][5:]

    return {
        'latitude': latitude,
        'longitude': longitude,
        'imei': imei,
    }
