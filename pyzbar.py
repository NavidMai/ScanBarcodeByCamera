import csv


def addToFile(file, what):
  open(file, 'a').write(what)

# Open .csv file
with open('yourOutput.csv', 'w', newline='') as csvFile:
  # Create writer
  writer = csv.writer(csvFile)

  # Title
  writer.writerow(['Time','Barcode Content','Image'])

  data_row = ['葉大雄', 18, '0911-123-123']
  # data_row =['林靜香',26, '0911-456-456']
  addToFile('yourOutput.csv', data_row)

# def write_csv():
#   path = "yourOutput.csv"
#   with open(path, 'a+') as f:
#     csv_write = csv.writer(f)
#     data_row = ['葉大雄', 18, '0911-123-123', '台北市火車站大廳']
#     # data_row =['林靜香',26, '0911-456-456', '台北市中山北路二段']
#     csv_write.writerow(data_row)



  # Data
  # writer.writerow(['葉大雄',18, '0911-123-123', '台北市火車站大廳'])
  # writer.writerow(['林靜香',26, '0911-456-456', '台北市中山北路二段'])

# write_csv()



# # Open .csv file
    # with open('Record.csv', 'w', newline='') as csvFile:
    #     # Create writer
    #     writer = csv.writer(csvFile)
    #     # Title
    #     writer.writerow(['Time', 'Barcode Content', 'Image'])
    #     # Data
    #     writer.writerow([nowTime, barcode.parsed, image_of_tag])