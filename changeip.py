from mikrotik.api import changeIpAddress
from utils.excel import  readExcelColumn
import config

def main():

    column = ["IP Address","New IP"]
    ipList = readExcelColumn(config.INPUT_FILE,column)

    for entry in ipList:
        ip = entry['IP Address']
        newIpAddress = entry['New IP']

        changeIpAddress(ip, config.USERNAME, config.PASSWORD, newIpAddress,"/27")

if __name__ == '__main__':
    main()
