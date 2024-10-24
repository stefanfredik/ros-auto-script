from mikrotik.api import changeIdentity
from utils.excel import readExcelColumn
import config

def main():
    # Membaca daftar IP dan New Identity dari file Excel
    column = ["IP Address","New Identity"]
    listIp = readExcelColumn(config.INPUT_FILE,column)

    # return print(listIp)


    # Loop melalui setiap perangkat dan mengambil informasi
    for index in listIp:
        ip = index["IP Address"]
        new_identity_name = index['New Identity']

        # Ubah identity name sesuai dengan kolom New Identity dari file Excel
        changeIdentity(ip, config.USERNAME, config.PASSWORD, new_identity_name)

if __name__ == '__main__':
    main()
