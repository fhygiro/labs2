import qrcode

text = input('Введите текст или URL: ')

qr = qrcode.make(text)
qr.save('qrcode.png')

print('QR-код успешно сохранён в файл qrcode.png')