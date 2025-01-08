from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
import mysql.connector

# 🛠️ Konfigurasi Database
db_config = {
    "host": "localhost", 
    "user": "root",
    "password": "",
    "database": "food_db"
}

# 🚀 Inisialisasi Aplikasi FastAPI
app = FastAPI(
    title="Food Menu API",
    description="API untuk mengelola daftar menu makanan.",
    version="1.0.0"
)

# 📝 Model Pydantic
class FoodItem(BaseModel):
    id: int = None  # Primary Key, Auto Increment
    name: str
    description: str
    price: float

class FoodItemCreate(BaseModel):
    name: str
    description: str
    price: float

# 🛡️ Fungsi koneksi database
def get_db_connection():
    return mysql.connector.connect(**db_config)

# 🍔 **Tambah Menu Makanan**
@app.post("/foods", response_model=FoodItem)
def create_food(item: FoodItemCreate):
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    query = "INSERT INTO foods (name, description, price) VALUES (%s, %s, %s)"
    cursor.execute(query, (item.name, item.description, item.price))
    connection.commit()
    food_id = cursor.lastrowid
    cursor.close()
    connection.close()
    return {**item.dict(), "id": food_id}

# 📜 **Lihat Semua Menu Makanan**
@app.get("/foods", response_model=List[FoodItem])
def read_foods():
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    query = "SELECT * FROM foods"
    cursor.execute(query)
    foods = cursor.fetchall()
    cursor.close()
    connection.close()
    return foods

# 🔍 **Lihat Makanan Berdasarkan ID**
@app.get("/foods/{food_id}", response_model=FoodItem)
def read_food(food_id: int):
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    query = "SELECT * FROM foods WHERE id = %s"
    cursor.execute(query, (food_id,))
    food = cursor.fetchone()
    cursor.close()
    connection.close()
    if not food:
        raise HTTPException(status_code=404, detail="Makanan tidak ditemukan")
    return food

# 🛠️ **Perbarui Menu Makanan**
@app.put("/foods/{food_id}", response_model=FoodItem)
def update_food(food_id: int, item: FoodItemCreate):
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    query = "UPDATE foods SET name = %s, description = %s, price = %s WHERE id = %s"
    cursor.execute(query, (item.name, item.description, item.price, food_id))
    connection.commit()
    cursor.close()
    connection.close()
    if cursor.rowcount == 0:
        raise HTTPException(status_code=404, detail="Makanan tidak ditemukan")
    return {**item.dict(), "id": food_id}

# 🗑️ **Hapus Menu Makanan**
@app.delete("/foods/{food_id}")
def delete_food(food_id: int):
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    query = "DELETE FROM foods WHERE id = %s"
    cursor.execute(query, (food_id,))
    connection.commit()
    cursor.close()
    connection.close()
    if cursor.rowcount == 0:
        raise HTTPException(status_code=404, detail="Makanan tidak ditemukan")
    return {"message": "Makanan berhasil dihapus"}

# 🚦 **Jalankan Server**
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("server:app", host="192.168.0.111", port=8000, reload=True)
