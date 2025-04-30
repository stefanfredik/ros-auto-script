import routeros_api
import pandas as pd

def checkHotspotStatus(routerIp, username, password, serverName):
    try:
        connection = routeros_api.RouterOsApiPool(
            routerIp, username=username, password=password, port=8728, plaintext_login=True
        )
        api = connection.get_api()
        hotspotServers = api.get_resource('/ip/hotspot').get()

        for server in hotspotServers:
            if server.get('name') == serverName:
                status = server.get('disabled', 'false')
                connection.disconnect()
                return status == 'false'
            
        connection.disconnect()
        
        return None
    
    except Exception as e:
        print(f"Error connecting to {routerIp}: {e}")
        return None

try:
    filePath = 'datasuspendwithip.xlsx'
    data = pd.read_excel(filePath)
    
except Exception as e:
    exit("Error saat membaca file: ", e)

data['Hotspot Status'] = None

mikrotikUsername = 'admin'
mikrotikPassword = 'RexusBattlefire'
hotspotName = 'hotspot-pembayaran'

for index, row in data.iterrows():
    routerIp = row['IP Address']
    customerName = row['Nama Pelanggan']
    print(f"Checking hotspot status for {customerName} (IP: {routerIp})")
    
    status = checkHotspotStatus(routerIp, mikrotikUsername, mikrotikPassword, hotspotName)
    if status is None:
        result = 'Connection Failed'
    elif status:
        result = 'Suspend Ok'
    else:
        result = 'Suspend Gagal'
    
    data.at[index, 'Hotspot Status'] = result
    print(f"Result for {customerName} (IP {routerIp}): {result}")

outputFile = 'data-hasil-verifikasi.xlsx'

try:
    data.to_excel(outputFile, index=False)
except Exception as e:
    print(f"Error writing to excel file: {e}")
    exit()


print(f"Hasil verifikasi disimpan di {outputFile}")
