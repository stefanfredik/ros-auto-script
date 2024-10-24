import os

# Direktori untuk file input dan output
INPUT_DIR = 'input'
OUTPUT_DIR = 'output'

# Nama file input dan output
INPUT_FILE = os.path.join(INPUT_DIR, 'datainput.xlsx')
OUTPUT_FILE = os.path.join(OUTPUT_DIR, 'dataoutput.xlsx')

# Username dan password untuk login ke MikroTik
USERNAME = 'admin'
PASSWORD = 'Hephaistos'

# Buat folder jika belum ada
os.makedirs(INPUT_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)
