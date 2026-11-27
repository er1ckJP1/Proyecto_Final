import oracledb
import tkinter as tk
from tkinter import ttk, messagebox

# CONEXION
def ejecutar_sql(sql, params=(), fetch=False):
    conexion = None
    cursor = None
    try:
        conexion = oracledb.connect(user="mes_admin", password="1234", dsn="localhost:1521/FREEPDB1")
        cursor = conexion.cursor()
        cursor.execute(sql, params)
        if fetch:
            return cursor.fetchall()
        conexion.commit()
        return True
    except oracledb.DatabaseError as e:
        messagebox.showerror("MES", str(e))
        return None
    finally:
        if cursor:
            cursor.close()
        if conexion:
            conexion.close()

# INTERFAZ 
class AppMES:
    def __init__(self, root):
        self.root = root
        self.root.title("MES")
        self.root.geometry("760x460")
        self.root.configure(bg="#121212")

        self.usuario = None   
        self.lineas = {}      
        self.motivos = {}     
        self.id_paro = None   
        self.pantalla_login()

    def limpiar(self):
        for w in self.root.winfo_children():
            w.destroy()

    def entrada(self, padre, ancho=35, **kwargs):
        return tk.Entry(padre, width=ancho, bg="#262626", fg="white", insertbackground="white", **kwargs)

    def boton(self, padre, texto, cmd, ancho=25, **kwargs):
        return tk.Button(padre, text=texto, width=ancho, bg="#333333", fg="white", command=cmd, **kwargs)

    # LOGIN 
    def pantalla_login(self):
        self.limpiar()
        self.usuario = None

        f = tk.Frame(self.root, bg="#121212")
        f.place(relx=0.5, rely=0.5, anchor="center")

        tk.Label(f, text="MES", font=("Arial", 22, "bold"), bg="#121212", fg="white").pack(pady=10)
        tk.Label(f, text="Número de Empleado:", font=("Arial", 11), bg="#121212", fg="white").pack(pady=5)

        self.txt_gafete = self.entrada(f, ancho=22, font=("Arial", 12), justify="center")
        self.txt_gafete.pack(pady=5)
        self.txt_gafete.focus()
        self.txt_gafete.bind("<Return>", lambda e: self.validar_login())  

        self.boton(f, "INGRESAR", self.validar_login, ancho=20).pack(pady=15)

    def validar_login(self):
        gafete = self.txt_gafete.get().strip()
        if not gafete.isdigit():
            return messagebox.showwarning("MES", "Ingresa un número de empleado válido.")

        sql = """
            SELECT e.num_empleado, e.nombre_completo, e.turno, e.activo, r.nivel_jerarquia
            FROM EMPLEADOS e JOIN ROLES r ON e.id_rol = r.id_rol
            WHERE e.num_empleado = :1
        """
        filas = ejecutar_sql(sql, (int(gafete),), fetch=True)
        if not filas:
            return messagebox.showerror("MES", "Empleado no encontrado.")
        if filas[0][3] != "S":
            return messagebox.showerror("MES", "Empleado inactivo.")

        self.usuario = (filas[0][0], filas[0][1], filas[0][2], filas[0][4])
        self.pantalla_principal()

    # PANTALLA PRINCIPAL 
    def pantalla_principal(self):
        self.limpiar()

        barra = tk.Frame(self.root, bg="#1e1e1e", bd=1, relief="solid")
        barra.pack(fill="x", padx=10, pady=8)
        tk.Label(barra, text=f"{self.usuario[1]}  |  Turno: {self.usuario[2]}",
                 font=("Arial", 10, "bold"), bg="#1e1e1e", fg="white").pack(side="left", padx=10, pady=6)
        self.boton(barra, "Cerrar Sesión", self.pantalla_login, ancho=14).pack(side="right", padx=10, pady=4)

        centro = tk.Frame(self.root, bg="#121212")
        centro.place(relx=0.5, rely=0.54, anchor="center")

        izq = tk.LabelFrame(centro, text="Captura de Producción", padx=20, pady=15, bg="#181818", fg="white")
        izq.pack(side="left", padx=15)

        tk.Label(izq, text="Seleccionar línea de producción:", bg="#181818", fg="white").pack(anchor="w")
        self.cb_linea = ttk.Combobox(izq, width=32, state="readonly")
        self.cb_linea.pack(pady=(2, 10))

        tk.Label(izq, text="Ingresar Lote:", bg="#181818", fg="white").pack(anchor="w")
        self.txt_lote = self.entrada(izq)
        self.txt_lote.pack(pady=(2, 10))

        tk.Label(izq, text="Ingresar Modelo:", bg="#181818", fg="white").pack(anchor="w")
        self.txt_modelo = self.entrada(izq)
        self.txt_modelo.pack(pady=(2, 10))

        tk.Label(izq, text="Capturar Piezas:", bg="#181818", fg="white").pack(anchor="w")
        self.txt_piezas = self.entrada(izq)
        self.txt_piezas.pack(pady=(2, 15))

        self.btn_guardar = self.boton(izq, "Guardar", self.guardar_piezas, ancho=30)
        self.btn_guardar.pack()

        der = tk.LabelFrame(centro, text="Opciones", padx=20, pady=15, bg="#181818", fg="white")
        der.pack(side="right", padx=15, fill="y")

        self.btn_tm = self.boton(der, "Iniciar Tiempo Muerto", self.iniciar_paro)
        self.btn_tm.pack(pady=6)
        self.btn_scrap = self.boton(der, "Captura de Scrap", self.abrir_scrap)
        self.btn_scrap.pack(pady=6)

        estado_del = "normal" if self.usuario[3] >= 2 else "disabled"
        self.btn_del = self.boton(der, "Eliminar Orden", self.abrir_eliminar, state=estado_del)
        self.btn_del.pack(pady=6)
        self.boton(der, "Ver Producción", self.ver_produccion).pack(pady=6)

        self.panel_paro = tk.Frame(der, bg="#181818")
        tk.Label(self.panel_paro, text="Razón del Tiempo Muerto:", bg="#181818", fg="white").pack(anchor="w", pady=(10, 2))
        self.cb_razon = ttk.Combobox(self.panel_paro, width=25, state="readonly")
        self.cb_razon.pack(pady=(0, 8))
        self.boton(self.panel_paro, "Cerrar Tiempo Muerto", self.cerrar_paro).pack()

        self.cargar_catalogos()

    # CARGA DE CATALOGOS
    def cargar_catalogos(self):
        rows_l = ejecutar_sql("SELECT id_linea, codigo_linea, nombre_linea FROM LINEAS_PRODUCCION", fetch=True) or []
        self.lineas = {f"{r[1]} - {r[2]}": r[0] for r in rows_l}
        self.cb_linea["values"] = list(self.lineas.keys())
        if self.lineas:
            self.cb_linea.current(0)

        rows_m = ejecutar_sql("SELECT id_motivo, codigo_paro, descripcion FROM CATALOGO_MOTIVOS_PARO", fetch=True) or []
        self.motivos = {f"{r[1]} - {r[2]}": r[0] for r in rows_m}
        self.cb_razon["values"] = list(self.motivos.keys())
        if self.motivos:
            self.cb_razon.current(0)

    def obtener_id_orden(self):
        linea, lote, modelo = self.cb_linea.get(), self.txt_lote.get().strip().upper(), self.txt_modelo.get().strip().upper()
        if not linea or not lote or not modelo:
            messagebox.showwarning("MES", "Selecciona línea e ingresa Lote y Modelo.")
            return None

        res = ejecutar_sql("SELECT id_produccion FROM ORDENES_PRODUCCION WHERE numero_lote = :1", (lote,), fetch=True)
        if res:
            return res[0][0]

        ok = ejecutar_sql(
            "INSERT INTO ORDENES_PRODUCCION (numero_lote, numero_parte, id_linea, num_empleado) VALUES (:1, :2, :3, :4)",
            (lote, modelo, self.lineas[linea], self.usuario[0])
        )
        if ok:
            res = ejecutar_sql("SELECT id_produccion FROM ORDENES_PRODUCCION WHERE numero_lote = :1", (lote,), fetch=True)
            return res[0][0] if res else None
        return None

    # PIEZAS BUENAS 
    def guardar_piezas(self):
        cant = self.txt_piezas.get().strip()
        if not cant.isdigit() or int(cant) <= 0:
            return messagebox.showwarning("MES", "Ingresa una cantidad válida.")
        id_prod = self.obtener_id_orden()
        if not id_prod:
            return

        sql = "UPDATE ORDENES_PRODUCCION SET total_piezas_finales = total_piezas_finales + :1, num_empleado = :2 WHERE id_produccion = :3"
        if ejecutar_sql(sql, (int(cant), self.usuario[0], id_prod)):
            messagebox.showinfo("MES", f"Se guardaron {cant} piezas.")
            self.txt_piezas.delete(0, "end")

    # SCRAP
    def abrir_scrap(self):
        id_prod = self.obtener_id_orden()
        if not id_prod:
            return

        win = tk.Toplevel(self.root)
        win.title("MES")
        win.geometry("320x200")
        win.configure(bg="#121212")
        win.grab_set()

        tk.Label(win, text="Numero de Piezas de Scrap:", bg="#121212", fg="white").pack(anchor="w", padx=25, pady=(18, 2))
        txt_cant = self.entrada(win, ancho=32)
        txt_cant.pack(padx=25)
        txt_cant.focus()

        tk.Label(win, text="Motivo:", bg="#121212", fg="white").pack(anchor="w", padx=25, pady=(10, 2))
        txt_mot = self.entrada(win, ancho=32)
        txt_mot.pack(padx=25)

        def guardar():
            c, m = txt_cant.get().strip(), txt_mot.get().strip()
            if not c.isdigit() or int(c) <= 0 or not m:
                return messagebox.showwarning("MES", "Ingresa cantidad válida y motivo.")
            sql = "UPDATE ORDENES_PRODUCCION SET total_piezas_scrap = total_piezas_scrap + :1, motivo_scrap = :2, num_empleado = :3 WHERE id_produccion = :4"
            if ejecutar_sql(sql, (int(c), m, self.usuario[0], id_prod)):
                win.destroy()
                messagebox.showinfo("MES", f"Se guardaron {c} piezas de scrap.")

        self.boton(win, "Guardar Scrap", guardar).pack(pady=18)

    # ELIMINAR ORDEN
    def abrir_eliminar(self):
        if self.usuario[3] < 2:
            return
        ordenes = ejecutar_sql("SELECT id_produccion, numero_lote, numero_parte FROM ORDENES_PRODUCCION ORDER BY id_produccion DESC", fetch=True)
        if not ordenes:
            return messagebox.showinfo("MES", "No hay órdenes registradas.")

        ord_dict = {f"ID {o[0]} - Lote: {o[1]} | Modelo: {o[2]}": o[0] for o in ordenes}
        win = tk.Toplevel(self.root)
        win.title("MES")
        win.geometry("360x160")
        win.configure(bg="#121212")
        win.grab_set()

        tk.Label(win, text="Seleccionar Orden a Eliminar:", bg="#121212", fg="white").pack(anchor="w", padx=25, pady=(18, 5))
        cb = ttk.Combobox(win, values=list(ord_dict.keys()), width=38, state="readonly")
        cb.pack(padx=25)
        cb.current(0)

        def confirmar():
            id_p = ord_dict[cb.get()]
            if messagebox.askyesno("MES", "¿Eliminar esta orden?"):
                ejecutar_sql("DELETE FROM TIEMPOS_MUERTOS WHERE id_produccion = :1", (id_p,))
                if ejecutar_sql("DELETE FROM ORDENES_PRODUCCION WHERE id_produccion = :1", (id_p,)):
                    win.destroy()
                    messagebox.showinfo("MES", "Orden eliminada")

        self.boton(win, "Eliminar Orden", confirmar).pack(pady=18)

    # TABLA DE PRODUCCIÓN
    def ver_produccion(self):
        sql = """
            SELECT o.id_produccion, l.codigo_linea, o.numero_lote, o.numero_parte,
                   o.total_piezas_finales, TO_CHAR(o.fecha_inicio, 'DD/MM/YYYY HH24:MI'),
                   e.nombre_completo, e.turno, o.total_piezas_scrap
            FROM ORDENES_PRODUCCION o
            JOIN LINEAS_PRODUCCION l ON o.id_linea = l.id_linea
            JOIN EMPLEADOS e ON o.num_empleado = e.num_empleado
            ORDER BY o.id_produccion DESC
        """
        filas = ejecutar_sql(sql, fetch=True) or []

        win = tk.Toplevel(self.root)
        win.title("MES")
        win.geometry("1020x360")
        win.configure(bg="#121212")
        win.grab_set()

        style = ttk.Style()
        style.theme_use("default")
        style.configure("Treeview", background="#181818", foreground="white", fieldbackground="#181818", rowheight=25)
        style.configure("Treeview.Heading", background="#262626", foreground="white")

        cols = ("ID", "LINEA", "LOTE", "MODELO", "PIEZAS", "FECHA", "EMPLEADO", "TURNO", "SCRAP")
        anchos = (45, 95, 80, 90, 70, 130, 210, 100, 70)
        tabla = ttk.Treeview(win, columns=cols, show="headings")
        for c, w in zip(cols, anchos):
            tabla.heading(c, text=c)
            tabla.column(c, width=w, anchor="center")
        tabla.pack(fill="both", expand=True, padx=10, pady=10)
        for f in filas:
            tabla.insert("", "end", values=f)

    # TIEMPOS MUERTOS
    def iniciar_paro(self):
        id_prod = self.obtener_id_orden()
        if not id_prod:
            return
        if ejecutar_sql("INSERT INTO TIEMPOS_MUERTOS (id_produccion, num_empleado_inicio) VALUES (:1, :2)", (id_prod, self.usuario[0])):
            self.id_paro = id_prod
            for b in (self.btn_guardar, self.btn_tm, self.btn_scrap, self.btn_del):
                b.config(state="disabled")
            self.panel_paro.pack(pady=10)

    def cerrar_paro(self):
        sql = "UPDATE TIEMPOS_MUERTOS SET hora_fin = SYSTIMESTAMP, id_motivo = :1, num_empleado_fin = :2 WHERE id_produccion = :3 AND hora_fin IS NULL"
        if ejecutar_sql(sql, (self.motivos[self.cb_razon.get()], self.usuario[0], self.id_paro)):
            self.id_paro = None
            self.panel_paro.pack_forget()
            for b in (self.btn_guardar, self.btn_tm, self.btn_scrap):
                b.config(state="normal")
            if self.usuario[3] >= 2:
                self.btn_del.config(state="normal")
            messagebox.showinfo("MES", "Tiempo muerto cerrado")

# ARRANQUE DE LA APLICACIÓN
if __name__ == "__main__":
    root = tk.Tk()
    AppMES(root)
    root.mainloop()