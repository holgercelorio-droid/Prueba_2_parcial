import flet as ft
import sqlite3
import os
import tempfile

# Usa la carpeta temporal del sistema para evitar problemas con los espacios en las rutas
DB_FILE = os.path.join(tempfile.gettempdir(), "productos_parcial.db")

def init_db():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS productos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            precio TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

def cargar_datos():
    init_db()
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT nombre, precio FROM productos")
    filas = cursor.fetchall()
    conn.close()
    return [{"nombre": row[0], "precio": row[1]} for row in filas]

def guardar_datos(nombre, precio):
    init_db()
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO productos (nombre, precio) VALUES (?, ?)", (nombre, precio))
    conn.commit()
    conn.close()

def main(page: ft.Page):
    page.title = "Catálogo de Productos"
    page.padding = 20
    
    lista_productos = cargar_datos()

    txt_nombre = ft.TextField(label="Nombre del Producto", width=300)
    txt_precio = ft.TextField(label="Precio", width=150)
    col_lista = ft.Column()

    def actualizar_lista():
        col_lista.controls.clear()
        for p in lista_productos:
            col_lista.controls.append(ft.Text(f"• {p['nombre']} - ${p['precio']}"))
        page.update()

    def agregar_click(e):
        if txt_nombre.value and txt_precio.value:
            guardar_datos(txt_nombre.value, txt_precio.value)
            lista_productos.append({"nombre": txt_nombre.value, "precio": txt_precio.value})
            txt_nombre.value = ""
            txt_precio.value = ""
            actualizar_lista()

    btn_agregar = ft.ElevatedButton("Guardar Producto", on_click=agregar_click)

    page.add(
        ft.Text("Gestión de Catálogo", size=24, weight=ft.FontWeight.BOLD),
        ft.Row([txt_nombre, txt_precio]),
        btn_agregar,
        ft.Divider(),
        ft.Text("Productos Registrados:", size=18),
        col_lista
    )
    actualizar_lista()

ft.app(target=main)