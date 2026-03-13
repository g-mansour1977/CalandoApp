import qrcode

url = "http://192.168.1.27:5000/payer/CAL-001"  # ton IP locale

qr = qrcode.make(url)
qr.save("qr_calando_001.png")

print("QR Code généré !")