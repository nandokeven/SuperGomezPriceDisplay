import pandas as pd
import time
import os
from flask import Flask, render_template, jsonify
from threading import Thread

# Path to the Excel file
FILE_PATH = "C:/Users/GOMEZ/OneDrive/VERDURAS.xlsx"
CHECK_INTERVAL = 10  # 5 minutes in seconds

# List of products to track
TRACKED_PRODUCTS = [
    "JITOMATE", "CEBOLLA MED", "CEBOLLA GRD", "NARANJA", "PLATANO VALERY",
    "SANDIA PERSONAL", "TOMATE", "BETABEL", "EJOTES", "ZANAHORIA",
    "CALABACITA", "CHAYOTE", "PAPA", "AGUACATE", "AJO", 
    "MELON", "PIÑA MIEL", "PEPINO", "LIMON", "CEBOLLA MORADA", 
    "CEBOLLA TAQUERA", "LECHUGA", "COL (REPOLLO)", "PAPA", "CHILE SERRANO", 
    "CHILE JALAPEÑO", "COLIFLOR", "CILANTRO", "GUAYABA", "FRESA BURBUJA", 
    "ESPINACA POPEYE", "MANZANA GALA","MANZANA VERDE", "APIO", "RABANOS", 
    "CHILE PASILLA VERDE", "PERA", "BROCOLI", "MANDARINA"
]

app = Flask(__name__)
latest_data = []  # Store the latest data globally
last_modified = None  # Track the last modification time of the file

def get_product_prices():
    global latest_data, last_modified
    try:
        # Check file modification time
        current_modified = os.path.getmtime(FILE_PATH)
        if last_modified != current_modified:
            df = pd.read_excel(FILE_PATH)  
            df = df[["Producto", "P. Venta"]]  # Select relevant columns
            df = df[df["Producto"].isin(TRACKED_PRODUCTS)]  # Filter tracked products
            new_data = df.to_dict(orient='records')
            if new_data != latest_data:  # Only update if data changed
                latest_data = new_data
                last_modified = current_modified
                print(f"[UPDATE] Product prices updated from Excel file at {time.ctime(current_modified)}.")
            else:
                print(f"[INFO] Excel file modified at {time.ctime(current_modified)}, but no price changes detected.")
        else:
            print("[INFO] No modifications to Excel file detected.")
        return latest_data
    except Exception as e:
        print(f"[ERROR] Failed to read Excel file: {e}")
        return latest_data  # Return last known data if error occurs

@app.route('/')
def display_prices():
    return render_template("index.html")  # Initial page load

@app.route('/prices')
def get_prices():
    data = get_product_prices()
    return jsonify(data if data else [])  # Return JSON for AJAX updates

def update_data():
    while True:
        time.sleep(CHECK_INTERVAL)
        print("[CHECK] Checking for updates...")
        get_product_prices()

if __name__ == "__main__":
    print("[START] Product price monitoring started.")
    Thread(target=update_data, daemon=True).start()
    app.run(debug=True, host='0.0.0.0', port=5000)