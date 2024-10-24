import array
import pandas as pd
import sys

# def read_excel(file_path):
#     # Membaca kolom IP dari file Excel
#     try:
#         data = pd.read_excel(file_path)
#     except Exception as e:
#         print(f"Gagal membaca file, pastikan data input excel sudah dibuat dan nama file sudah benar. {file_path} : \n {e}")
#         sys.exit(1)
        
#     return data['IP Address'].tolist()

def readExcelColumn(file_path,column:array): 
    # Membaca kolom IP Address dan New Identity dari file Excel
    try:
        data = pd.read_excel(file_path)
    except Exception as e:
        print(f"Gagal membaca file, pastikan data input excel sudah dibuat dan nama file sudah benar. {file_path} : \n {e}")
        sys.exit(1)
    
    # Mengembalikan data sebagai list of dictionaries
    return data[column].to_dict(orient='records')


def readExcelAllColumn(file_path): 
    # Membaca semua kolom dari file Excel
    try:
        data = pd.read_excel(file_path)
    except Exception as e:
        print(f"Gagal membaca file, pastikan data input excel sudah dibuat dan nama file sudah benar. {file_path} : \n {e}")
        sys.exit(1)
    
    # Mengembalikan semua data sebagai list of dictionaries
    return data.to_dict(orient='records')

def save_to_excel(data, output_file):
    # Membuat DataFrame dari hasil data
    df = pd.DataFrame(data)

    # Menambahkan kolom nomor urut
    df.insert(0, 'No', range(1, len(df) + 1))

    # Menyimpan ke file Excel
    df.to_excel(output_file, index=False)
