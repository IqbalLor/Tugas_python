import requests
import json

API_BASE_URL = "http://192.168.0.111:8000"

def print_response(response):
    """Format dan cetak respons dari server."""
    if response.status_code in [200, 201]:
        print(json.dumps(response.json(), indent=4))
    else:
        print(f"Error {response.status_code}: {response.text}")

def create_food():
    """Kirim POST request untuk menambahkan makanan baru."""
    print("\n🍔 Tambah Menu Makanan Baru:")
    name = input("Nama Makanan: ")
    description = input("Deskripsi: ")
    price = float(input("Harga: "))
    payload = {
        "name": name,
        "description": description,
        "price": price
    }
    response = requests.post(f"{API_BASE_URL}/foods", json=payload)
    print_response(response)

def read_all_foods():
    """Kirim GET request untuk mendapatkan semua makanan."""
    print("\n📜 Daftar Semua Menu Makanan:")
    response = requests.get(f"{API_BASE_URL}/foods")
    print_response(response)

def read_food_by_id():
    """Kirim GET request untuk mendapatkan makanan berdasarkan ID."""
    print("\n🔍 Cari Menu Makanan Berdasarkan ID:")
    food_id = input("ID Makanan: ")
    response = requests.get(f"{API_BASE_URL}/foods/{food_id}")
    print_response(response)

def update_food():
    """Kirim PUT request untuk memperbarui data makanan."""
    print("\n🛠️ Perbarui Menu Makanan:")
    food_id = input("ID Makanan: ")
    name = input("Nama Baru: ")
    description = input("Deskripsi Baru: ")
    price = float(input("Harga Baru: "))
    payload = {
        "name": name,
        "description": description,
        "price": price
    }
    response = requests.put(f"{API_BASE_URL}/foods/{food_id}", json=payload)
    print_response(response)

def delete_food():
    """Kirim DELETE request untuk menghapus makanan."""
    print("\n🗑️ Hapus Menu Makanan:")
    food_id = input("ID Makanan: ")
    response = requests.delete(f"{API_BASE_URL}/foods/{food_id}")
    print_response(response)

def main():
    """Menu utama untuk operasi CRUD."""
    while True:
        print("\n🍽️ **Menu Manajemen Makanan** 🍽️")
        print("1. Tambah Menu Makanan")
        print("2. Lihat Semua Menu Makanan")
        print("3. Lihat Makanan Berdasarkan ID")
        print("4. Perbarui Menu Makanan")
        print("5. Hapus Menu Makanan")
        print("6. Keluar")
        
        choice = input("Pilih opsi (1-6): ")
        
        if choice == "1":
            create_food()
        elif choice == "2":
            read_all_foods()
        elif choice == "3":
            read_food_by_id()
        elif choice == "4":
            update_food()
        elif choice == "5":
            delete_food()
        elif choice == "6":
            print("👋 Keluar dari aplikasi. Sampai jumpa!")
            break
        else:
            print("❌ Pilihan tidak valid. Silakan coba lagi.")

if __name__ == "__main__":
    main()
