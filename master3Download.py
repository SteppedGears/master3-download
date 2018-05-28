import serial
import serial.tools.list_ports

def getSerialPortList():
    coms = serial.tools.list_ports.comports()
    comList = list()
    for c in coms:
        comList.append(c.device)
    return comList

def getMasterSerialNumber(ser):
    ser.write(b"?V\r\n")
    answer = ser.readline()
    answer = answer.decode("utf-8")
    tokens = answer.split(',')
    return tokens[1]

def rewindData(ser):
    ser.write(b"?F\r\n")
    answer = ser.readline()
    print(answer)

def readDataFromMasterIter(ser):
    readData = ""
    while True:
        ser.write(b"?D\r\n")
        reply = ser.readline().decode("utf-8")
        if(reply[0] == "N"):
            break
        readData += reply
    return readData

def dataFromMaster(ser):
    while True:
        ser.write(b"?D\r\n")
        reply = ser.readline().decode("utf-8")
        if(reply[0] == "N"):
            break
        yield reply

def readDataFromMaster(ser, file):
    for row in dataFromMaster(ser):
        f.write(row)

if __name__ == "__main__":
    print("Master³ data download utility\r\n")
    comList = getSerialPortList()
    print("Available ports:\r\n")
    for c in comList:
        print (c + "\r\n")
    ser = serial.Serial(comList[0], 19200, timeout = 1)
    serialNum = getMasterSerialNumber(ser)
    f = open("Master3-"+serialNum+".txt", "w+", newline='')
    rewindData(ser)
    readDataFromMaster(ser, f)
    f.close()
