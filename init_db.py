import sqlite3

# Conectar a la base de datos (la crea si no existe)
conn = sqlite3.connect('inventario.db')
cursor = conn.cursor()

# Crear tabla productos
cursor.execute('''
    CREATE TABLE IF NOT EXISTS productos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL,
        categoria TEXT NOT NULL,
        precio REAL NOT NULL,
        stock INTEGER NOT NULL
    )
''')

# Insertar algunos datos de ejemplo
cursor.execute('''
    INSERT INTO productos (nombre, categoria, precio, stock)
    VALUES 
        ('Laptop Dell Inspiron', 'Computadoras', 899.99, 15),
        ('Mouse Logitech MX', 'Accesorios', 49.99, 50),
        ('Teclado Mecánico RGB', 'Accesorios', 129.99, 30),
        ('Monitor Samsung 27"', 'Monitores', 299.99, 20),
        ('Disco SSD 1TB', 'Almacenamiento', 89.99, 40)
''')

conn.commit()
conn.close()

print("✓ Base de datos creada exitosamente con datos de ejemplo")