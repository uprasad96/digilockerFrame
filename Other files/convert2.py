import base64

data = open("Aadhar.pdf", "rb").read().encode("base64")
f = open("Aadhar.txt", "w")
f.write(data)
f.close()
