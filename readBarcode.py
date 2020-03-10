# -*- coding: UTF-8 -*-
import zxing


reader = zxing.BarCodeReader()
barcode = reader.decode("Data/barcode.gif")
# barcode = reader.decode("Data/qrcode.png")
print(barcode.parsed)
