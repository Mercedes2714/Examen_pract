from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3

app = Flask(__name__)
app.secret_key = 'tu_clave_secreta_cambia_esto'

# Función para conectar a la base de datos
def get_db_connection():
    conn = sqlite3.connect('inventario.db')
    conn.row_factory = sqlite3.Row  # Permite acceder a columnas por nombre
    return conn

# Ruta principal - LISTAR productos
@app.route('/')
def index():
    conn = get_db_connection()
    productos = conn.execute('SELECT * FROM productos').fetchall()
    conn.close()
    return render_template('index.html', productos=productos)

# Ruta para mostrar formulario de CREAR
@app.route('/crear', methods=['GET'])
def crear_form():
    return render_template('crear.html')

# Ruta para procesar el guardado de nuevo producto
@app.route('/guardar', methods=['POST'])
def guardar():
    nombre = request.form['nombre']
    categoria = request.form['categoria']
    precio = float(request.form['precio'])
    stock = int(request.form['stock'])
    
    # Validación básica
    if not nombre or not categoria:
        flash('Nombre y categoría son obligatorios', 'error')
        return redirect(url_for('crear_form'))
    
    conn = get_db_connection()
    conn.execute(
        'INSERT INTO productos (nombre, categoria, precio, stock) VALUES (?, ?, ?, ?)',
        (nombre, categoria, precio, stock)
    )
    conn.commit()
    conn.close()
    
    flash('Producto agregado exitosamente', 'success')
    return redirect(url_for('index'))

# Ruta para EDITAR - mostrar formulario con datos
@app.route('/editar/<int:id>', methods=['GET'])
def editar_form(id):
    conn = get_db_connection()
    producto = conn.execute('SELECT * FROM productos WHERE id = ?', (id,)).fetchone()
    conn.close()
    
    if producto is None:
        flash('Producto no encontrado', 'error')
        return redirect(url_for('index'))
    
    return render_template('editar.html', producto=producto)

# Ruta para procesar actualización
@app.route('/actualizar/<int:id>', methods=['POST'])
def actualizar(id):
    nombre = request.form['nombre']
    categoria = request.form['categoria']
    precio = float(request.form['precio'])
    stock = int(request.form['stock'])
    
    conn = get_db_connection()
    conn.execute(
        'UPDATE productos SET nombre = ?, categoria = ?, precio = ?, stock = ? WHERE id = ?',
        (nombre, categoria, precio, stock, id)
    )
    conn.commit()
    conn.close()
    
    flash('Producto actualizado exitosamente', 'success')
    return redirect(url_for('index'))

# Ruta para ELIMINAR
@app.route('/eliminar/<int:id>')
def eliminar(id):
    conn = get_db_connection()
    conn.execute('DELETE FROM productos WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    
    flash('Producto eliminado exitosamente', 'success')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)