import tkinter as tk
from tkinter import messagebox
import json

class Persona:
    def __init__(self, nombre, email):
        self.nombre = nombre
        self.email = email

class Cliente(Persona):
    def __init__(self, nombre, email, volumen_compras):
        super().__init__(nombre, email)
        self.volumen_compras = volumen_compras

class Organizador(Persona):
    def __init__(self, nombre, email, eventos):
        super().__init__(nombre, email)
        self.eventos = eventos

class Evento:
    def __init__(self, nombre, fecha, precio):
        self.nombre = nombre
        self.fecha = fecha
        self.precio = precio

    def mostrar_detalle(self):
        pass

class EventoParrillada(Evento):
    def __init__(self, nombre, fecha, precio, cantidad_parrillas):
        super().__init__(nombre, fecha, precio)
        self.cantidad_parrillas = cantidad_parrillas

    def mostrar_detalle(self):
        return f"Evento de Parrillada: {self.nombre}, Fecha: {self.fecha}, Precio: {self.precio}, Cantidad de Parrillas: {self.cantidad_parrillas}"

class EventoVIP(Evento):
    def __init__(self, nombre, fecha, precio, beneficios_vip):
        super().__init__(nombre, fecha, precio)
        self.beneficios_vip = beneficios_vip

    def mostrar_detalle(self):
        return f"Evento VIP: {self.nombre}, Fecha: {self.fecha}, Precio: {self.precio}, Beneficios VIP: {self.beneficios_vip}"

class Venta:
    def __init__(self, cliente, evento, cantidad):
        self.cliente = cliente
        self.evento = evento
        self.cantidad = cantidad

    def calcular_descuento(self):
        if isinstance(self.cliente, Cliente) and self.cliente.volumen_compras >= 5:
            descuento = 0.1
        elif isinstance(self.evento, EventoVIP):
            descuento = 0.05
        else:
            descuento = 0
        return self.evento.precio * (1 - descuento) * self.cantidad

class GestorVentas:
    def __init__(self, archivo_json):
        self.archivo_json = archivo_json

    def cargar_ventas(self):
        try:
            with open(self.archivo_json, 'r') as f:
                ventas = json.load(f)
        except FileNotFoundError:
            ventas = []
        return ventas

    def guardar_ventas(self, ventas):
        with open(self.archivo_json, 'w') as f:
            json.dump(ventas, f)

    def agregar_venta(self, cliente, evento, cantidad):
        venta = Venta(cliente, evento, cantidad)
        ventas = self.cargar_ventas()
        ventas.append({
            'cliente': {
                'nombre': venta.cliente.nombre,
                'email': venta.cliente.email,
                'volumen_compras': venta.cliente.volumen_compras
            },
            'evento': {
                'nombre': venta.evento.nombre,
                'fecha': venta.evento.fecha,
                'precio': venta.evento.precio
            },
            'cantidad': venta.cantidad
        })
        self.guardar_ventas(ventas)

    def reporte_ventas_evento(self, evento):
        ventas = self.cargar_ventas()
        total_ventas = 0
        for venta in ventas:
            if venta['evento']['nombre'] == evento.nombre:
                total_ventas += venta['cantidad']
        return total_ventas

    def reporte_ventas_totales(self):
        ventas = self.cargar_ventas()
        total_ventas = 0
        for venta in ventas:
            total_ventas += venta['cantidad']
        return total_ventas

class ExcepcionEventoAgotado(Exception):
    pass

class ExcepcionDatosInvalidos(Exception):
    pass

class ExcepcionCargaGuardadoArchivo(Exception):
    pass

class VentanaPrincipal:
    def __init__(self, master):
        self.master = master
        self.master.title("Sistema de Gestión de Ventas de Parrilladas")

        self.frame = tk.Frame(self.master)
        self.frame.pack()

        self.boton_comprar = tk.Button(self.frame, text="Comprar ticket", command=self.abrir_ventana_comprar)
        self.boton_comprar.pack()

        self.boton_reporte_evento = tk.Button(self.frame, text="Reporte de ventas por evento", command=self.abrir_ventana_reporte_evento)
        self.boton_reporte_evento.pack()

        self.boton_reporte_totales = tk.Button(self.frame, text="Reporte de ventas totales", command=self.reporte_ventas_totales)
        self.boton_reporte_totales.pack()

        self.boton_salir = tk.Button(self.frame, text="Salir", command=self.master.quit)
        self.boton_salir.pack()

    def abrir_ventana_comprar(self):
        ventana_comprar = tk.Toplevel(self.master)
        ComprarTicket(ventana_comprar)

    def abrir_ventana_reporte_evento(self):
        ventana_reporte_evento = tk.Toplevel(self.master)
        ReporteVentasEvento(ventana_reporte_evento)

    def reporte_ventas_totales(self):
        try:
            gestor_ventas = GestorVentas('ventas.json')
            total_ventas = gestor_ventas.reporte_ventas_totales()
            messagebox.showinfo("Reporte de ventas totales", f"Total de ventas totales: {total_ventas}")
        except ExcepcionCargaGuardadoArchivo as e:
            messagebox.showerror("Error", "Error al cargar/guardar el archivo de ventas")

class ComprarTicket:
    def __init__(self, master):
        self.master = master
        self.master.title("Comprar ticket")

        self.frame = tk.Frame(self.master)
        self.frame.pack()

        self.label_nombre_evento = tk.Label(self.frame, text="Nombre del evento:")
        self.label_nombre_evento.pack()
        self.entry_nombre_evento = tk.Entry(self.frame)
        self.entry_nombre_evento.pack()

        self.label_nombre = tk.Label(self.frame, text="Nombre:")
        self.label_nombre.pack()
        self.entry_nombre = tk.Entry(self.frame)
        self.entry_nombre.pack()

        self.label_email = tk.Label(self.frame, text="Email:")
        self.label_email.pack()
        self.entry_email = tk.Entry(self.frame)
        self.entry_email.pack()

        self.label_volumen_compras = tk.Label(self.frame, text="Volumen de compras:")
        self.label_volumen_compras.pack()
        self.entry_volumen_compras = tk.Entry(self.frame)
        self.entry_volumen_compras.pack()

        self.label_cantidad_tickets = tk.Label(self.frame, text="Cantidad de tickets:")
        self.label_cantidad_tickets.pack()
        self.entry_cantidad_tickets = tk.Entry(self.frame)
        self.entry_cantidad_tickets.pack()

        self.boton_comprar = tk.Button(self.frame, text="Comprar", command=self.comprar_ticket)
        self.boton_comprar.pack()

    def comprar_ticket(self):
        try:
            nombre_evento = self.entry_nombre_evento.get()
            nombre_cliente = self.entry_nombre.get()
            email_cliente = self.entry_email.get()
            volumen_compras_cliente = int(self.entry_volumen_compras.get())
            cantidad_tickets = int(self.entry_cantidad_tickets.get())
            
            cliente = Cliente(nombre_cliente, email_cliente, volumen_compras_cliente)
            evento = Evento(nombre_evento, "", 0)  # Modificar con los datos adecuados
            gestor_ventas = GestorVentas('ventas.json')
            gestor_ventas.agregar_venta(cliente, evento, cantidad_tickets)
            messagebox.showinfo("Compra exitosa", "Ticket comprado exitosamente.")
            self.master.destroy()
        except ValueError:
            messagebox.showerror("Error", "Por favor ingrese un volumen de compras y cantidad de tickets válidos.")
        except ExcepcionCargaGuardadoArchivo as e:
            messagebox.showerror("Error", "Error al cargar/guardar el archivo de ventas")

class ReporteVentasEvento:
    def __init__(self, master):
        self.master = master
        self.master.title("Reporte de ventas por evento")

        self.frame = tk.Frame(self.master)
        self.frame.pack()

        self.label_nombre_evento = tk.Label(self.frame, text="Nombre del evento:")
        self.label_nombre_evento.pack()
        self.entry_nombre_evento = tk.Entry(self.frame)
        self.entry_nombre_evento.pack()

        self.boton_generar_reporte = tk.Button(self.frame, text="Generar reporte", command=self.generar_reporte)
        self.boton_generar_reporte.pack()

    def generar_reporte(self):
        try:
            nombre_evento = self.entry_nombre_evento.get()
            evento = Evento(nombre_evento, "", 0)  # Modificar con los datos adecuados
            gestor_ventas = GestorVentas('ventas.json')
            total_ventas = gestor_ventas.reporte_ventas_evento(evento)
            messagebox.showinfo("Reporte de ventas por evento", f"Total de ventas para el evento {nombre_evento}: {total_ventas}")
        except ExcepcionCargaGuardadoArchivo as e:
            messagebox.showerror("Error", "Error al cargar/guardar el archivo de ventas")

def main():
    root = tk.Tk()
    app = VentanaPrincipal(root)
    root.mainloop()

if __name__ == "__main__":
    main()


