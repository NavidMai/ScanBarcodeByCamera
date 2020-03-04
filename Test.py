import zxing


reader = zxing.BarCodeReader()
barcode = reader.decode("barcode.gif")
# barcode = reader.decode("qrcode.png")
print(barcode.parsed)
