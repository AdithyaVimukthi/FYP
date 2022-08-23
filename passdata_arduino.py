import serial

arduinoData = serial.Serial('com6',115200)

while True:
    cmd = input('Enter Your Command: ')
    if cmd == 'q':
        break
    cmd = cmd+'\r'
    arduinoData.write(cmd.encode())
