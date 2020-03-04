import zxing
reader = zxing.BarCodeReader()
barcode = reader.decode("barcode.gif")
# barcode = reader.decode("QR_Code.png")
print(barcode.parsed)