import uuid
import random
from datetime import datetime, timedelta

# Connexion à MySQL (exemple avec mysql-connector-python)
import mysql.connector

try:
    # Paramètres de connexion
    db = mysql.connector.connect(
        host="localhost",  # Utilisez "localhost" ou l'IP de votre machine hôte
        port=3307,         # Spécifiez explicitement le port 3307 (mappé depuis Docker)
        user="olduser",
        password="oldpass",
        database="old_db"  # Correction : utilisez "old_db" comme dans votre configuration Docker, pas "database_mysql_old"
    )
    cursor = db.cursor()

    # Catégories existantes (leurs IDs)
    category_ids = [
        '550e8400-e29b-41d4-a716-446655440000',  # Electronics
        '550e8400-e29b-41d4-a716-446655440001',  # Clothing
        '550e8400-e29b-41d4-a716-446655440002',  # Books
        '550e8400-e29b-41d4-a716-446655440015',  # Furniture
        '550e8400-e29b-41d4-a716-446655440016',  # Sports
        '550e8400-e29b-41d4-a716-446655440017',  # Toys
        '550e8400-e29b-41d4-a716-446655440018',  # Jewelry
        '550e8400-e29b-41d4-a716-446655440019',  # Food
        '550e8400-e29b-41d4-a716-446655440020',  # Beauty
        '550e8400-e29b-41d4-a716-446655440021'   # Tools
    ]

    # Types de produits et descriptions
    product_types = ['Laptop', 'Shirt', 'Book', 'Chair', 'Shoes', 'Toy', 'Necklace', 'Coffee', 'Lipstick', 'Drill']
    descriptions = ['High-quality item', 'Durable and stylish', 'Best-selling product', 'Comfortable and ergonomic', 'Lightweight design']

    # Générer 100 produits
    for i in range(50000):
        product_id = str(uuid.uuid4())
        name = f"{random.choice(product_types)} {chr(65 + i // 10)}{i % 10}"  # Ex: Laptop A1, Laptop A2, etc.
        description = f"{random.choice(descriptions)} for everyday use"
        price = round(random.uniform(10.00, 1000.00), 2)
        is_actif = random.choice([True, False])
        created_at = datetime.now() - timedelta(days=random.randint(1, 365))
        updated_at = created_at

        # Insérer dans products
        cursor.execute("""
            INSERT INTO products (id, is_actif, name, description, price, created_at, updated_at)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (product_id, is_actif, name, description, price, created_at, updated_at))

        # Insérer dans inventories (quantity aléatoire)
        inventory_id = str(uuid.uuid4())
        quantity = random.randint(50, 500)
        cursor.execute("""
            INSERT INTO inventories (id, product_id, quantity)
            VALUES (%s, %s, %s)
        """, (inventory_id, product_id, quantity))

        # Associer 1-3 catégories aléatoires
        num_categories = random.randint(1, 3)
        selected_categories = random.sample(category_ids, num_categories)
        for cat_id in selected_categories:
            cursor.execute("""
                INSERT INTO products_categories (product_id, category_id)
                VALUES (%s, %s)
            """, (product_id, cat_id))

        # Insérer une image
        image_id = str(uuid.uuid4())
        url = f"https://example.com/images/{name.lower().replace(' ', '_')}.jpg"
        cursor.execute("""
            INSERT INTO images (id, product_id, url)
            VALUES (%s, %s, %s)
        """, (image_id, product_id, url))

        # Insérer un order_detail (exemple simple)
        order_detail_id = str(uuid.uuid4())
        order_id = str(uuid.uuid4())
        order_quantity = random.randint(1, 5)
        cursor.execute("""
            INSERT INTO order_details (id, product_id, quantity, order_id)
            VALUES (%s, %s, %s, %s)
        """, (order_detail_id, product_id, order_quantity, order_id))

    # Valider les changements
    db.commit()
    print("Données insérées avec succès !")
except mysql.connector.Error as err:
    print(f"Erreur : {err}")
finally:
    cursor.close()
    db.close()