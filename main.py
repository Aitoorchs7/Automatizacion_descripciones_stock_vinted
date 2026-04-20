import customtkinter as ctk
from dotenv import load_dotenv
import os
from utils import extract_vinted_id
from sheet_manager import SheetManager
from gemini_generator import GeminiGenerator
from tkinter import messagebox
import threading

load_dotenv()

class VintedApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self.title("Sistema de Gestión Vinted - Generador de Descripciones y Tracker de Ventas")
        self.geometry("950x750")
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        # Setup core modules
        try:
            self.sheet_manager = SheetManager(
                credentials_path=os.getenv("GOOGLE_APPLICATION_CREDENTIALS", "automatizador-descripciones-st-bc5fb2764a4d.json"),
                spreadsheet_id=os.getenv("SPREADSHEET_ID")
            )
        except Exception as e:
            self.sheet_manager = None
            print("Error SheetManager:", e)
            messagebox.showwarning("Cuidado", f"SheetManager no se cargó: {e}")
            
        try:
            self.gemini_generator = GeminiGenerator(api_key=os.getenv("GEMINI_API_KEY"))
        except Exception as e:
            self.gemini_generator = None
            print("Error GeminiGenerator:", e)
            messagebox.showwarning("Cuidado", f"Gemini Generator no se cargó: {e}")

        # Create Tabview
        self.tabview = ctk.CTkTabview(self, width=900, height=700)
        self.tabview.pack(padx=20, pady=20, fill="both", expand=True)
        
        self.tab_desc = self.tabview.add("Generador de Variaciones")
        self.tab_sales = self.tabview.add("Tracker de Ventas")
        
        self._setup_generator_tab()
        self._setup_sales_tab()
        
    def _setup_generator_tab(self):
        frame_inputs = ctk.CTkFrame(self.tab_desc)
        frame_inputs.pack(pady=10, padx=10, fill="x")
        
        # Grid layout for inputs
        ctk.CTkLabel(frame_inputs, text="Marca:", font=("Arial", 12, "bold")).grid(row=0, column=0, padx=10, pady=10, sticky="e")
        self.entry_brand = ctk.CTkEntry(frame_inputs, width=250)
        self.entry_brand.grid(row=0, column=1, padx=10, pady=10)
        
        ctk.CTkLabel(frame_inputs, text="Prenda:", font=("Arial", 12, "bold")).grid(row=0, column=2, padx=10, pady=10, sticky="e")
        self.entry_item = ctk.CTkEntry(frame_inputs, width=250)
        self.entry_item.grid(row=0, column=3, padx=10, pady=10)
        
        ctk.CTkLabel(frame_inputs, text="Talla:", font=("Arial", 12, "bold")).grid(row=1, column=0, padx=10, pady=10, sticky="e")
        self.entry_size = ctk.CTkEntry(frame_inputs, width=250)
        self.entry_size.grid(row=1, column=1, padx=10, pady=10)
        
        ctk.CTkLabel(frame_inputs, text="Estado:", font=("Arial", 12, "bold")).grid(row=1, column=2, padx=10, pady=10, sticky="e")
        self.entry_condition = ctk.CTkEntry(frame_inputs, width=250)
        self.entry_condition.grid(row=1, column=3, padx=10, pady=10)
        
        ctk.CTkLabel(frame_inputs, text="Palabras Clave (3):", font=("Arial", 12, "bold")).grid(row=2, column=0, padx=10, pady=10, sticky="e")
        self.entry_keywords = ctk.CTkEntry(frame_inputs, width=630)
        self.entry_keywords.grid(row=2, column=1, columnspan=3, padx=10, pady=10, sticky="w")
        
        self.btn_generate = ctk.CTkButton(frame_inputs, text="✨ Generar 5 Versiones para Multicuenta ✨", 
                                          command=self.generate_desc, 
                                          fg_color="#2B8C52", hover_color="#1E663B", font=("Arial", 14, "bold"))
        self.btn_generate.grid(row=3, column=0, columnspan=4, pady=20)
        
        # Output area
        self.textbox_desc = ctk.CTkTextbox(self.tab_desc, width=860, height=450, font=("Arial", 13))
        self.textbox_desc.pack(padx=10, pady=10, fill="both", expand=True)

    def generate_desc(self):
        if not self.gemini_generator:
            messagebox.showerror("Error", "Gemini no inicializado. Revisa .env y tu GEMINI_API_KEY")
            return
            
        brand = self.entry_brand.get()
        item = self.entry_item.get()
        size = self.entry_size.get()
        cond = self.entry_condition.get()
        kw = self.entry_keywords.get()
        
        if not all([brand, item, size, cond, kw]):
            messagebox.showwarning("Faltan Datos", "Por favor completa todos los campos (Marca, Prenda, Talla, Estado y Keywords).")
            return
            
        self.btn_generate.configure(state="disabled", text="Generando descripciones (conectando a la IA)...")
        self.textbox_desc.delete("0.0", "end")
        self.textbox_desc.insert("0.0", "Conectando con Gemini 1.5 y aplicando el Prompt Maestro. Esto tardará alrededor de 10 segundos...\n")
        
        def worker():
            try:
                result = self.gemini_generator.generate_descriptions(brand, item, size, cond, kw)
                self.textbox_desc.delete("0.0", "end")
                if "error" in result:
                    self.textbox_desc.insert("0.0", f"❌ Ha ocurrido un error en la generación:\n{result.get('error')}\n\nRespuesta cruda de Gemini:\n{result.get('raw')}")
                else:
                    self.textbox_desc.insert("end", "✅ GENERACIÓN COMPLETADA CON ÉXITO\nPuedes copiar y pegar cada bloque en tus cuentas.\n\n" + "="*80 + "\n\n")
                    for key, val in result.items():
                        self.textbox_desc.insert("end", f"✨ {key.replace('_', ' ').upper()} ✨\n\n{val}\n\n{'='*80}\n\n")
            except Exception as e:
                self.textbox_desc.delete("0.0", "end")
                self.textbox_desc.insert("0.0", f"Error inesperado procesando el texto: {str(e)}")
            finally:
                self.btn_generate.configure(state="normal", text="✨ Generar 5 Versiones para Multicuenta ✨")
                
        threading.Thread(target=worker, daemon=True).start()

    def _setup_sales_tab(self):
        frame_sales = ctk.CTkFrame(self.tab_sales)
        frame_sales.pack(pady=40, padx=20, fill="x")
        
        ctk.CTkLabel(frame_sales, text="🔗 URL del Artículo Vendido:", font=("Arial", 14, "bold")).grid(row=0, column=0, padx=20, pady=20, sticky="e")
        self.entry_url = ctk.CTkEntry(frame_sales, width=450, placeholder_text="https://www.vinted.es/items/...")
        self.entry_url.grid(row=0, column=1, columnspan=3, padx=10, pady=20, sticky="w")
        
        ctk.CTkLabel(frame_sales, text="💰 Precio Venta (€):", font=("Arial", 14, "bold")).grid(row=1, column=0, padx=20, pady=20, sticky="e")
        self.entry_price = ctk.CTkEntry(frame_sales, width=150)
        self.entry_price.grid(row=1, column=1, padx=10, pady=20, sticky="w")
        
        ctk.CTkLabel(frame_sales, text="🏷️ Coste Estimado (€):", font=("Arial", 14, "bold")).grid(row=1, column=2, padx=20, pady=20, sticky="e")
        self.entry_cost = ctk.CTkEntry(frame_sales, width=150)
        self.entry_cost.grid(row=1, column=3, padx=10, pady=20, sticky="w")
        
        self.btn_save_sale = ctk.CTkButton(frame_sales, text="📊 Registrar Venta en Sheets", 
                                           command=self.save_sale,
                                           fg_color="#005A9C", hover_color="#003B6D", font=("Arial", 16, "bold"), height=40)
        self.btn_save_sale.grid(row=2, column=0, columnspan=4, pady=30)
        
        self.label_status = ctk.CTkLabel(self.tab_sales, text="", text_color="green", font=("Arial", 16, "bold"))
        self.label_status.pack(pady=20)

    def save_sale(self):
        if not self.sheet_manager:
            messagebox.showerror("Error", "SheetManager no inicializado. Revisa Google Credentials .json y el ID en .env")
            return
            
        url = self.entry_url.get().strip()
        price = self.entry_price.get().strip()
        cost = self.entry_cost.get().strip()
        
        if not all([url, price, cost]):
            messagebox.showwarning("Atención", "Rellena todos los campos: URL, Precio Venta y Coste.")
            return
            
        item_id = extract_vinted_id(url)
        if not item_id:
            messagebox.showerror("Error de URL", "No se pudo extraer el ID de la URL. Asegúrate de que el formato sea correcto (ej: .../items/123456-nombre)")
            return
            
        try:
            float(price.replace(',', '.'))
            float(cost.replace(',', '.'))
        except ValueError:
            messagebox.showerror("Error numérico", "Los campos Precio y Coste deben ser números (usar punto o coma para decimales).")
            return
            
        # Standardize decimal separator
        price = price.replace(',', '.')
        cost = cost.replace(',', '.')

        self.btn_save_sale.configure(state="disabled", text="Registrando...")
        self.label_status.configure(text="Conectando con Google Sheets...", text_color="yellow")

        # Ejecutamos la tarea de red en background para que la GUI no se congele
        def worker():
            try:
                success, msg = self.sheet_manager.check_and_insert_sale(item_id, price, cost)
                if success:
                    self.label_status.configure(text=f"✅ {msg} (ID: {item_id})", text_color="green")
                    self.entry_url.delete(0, "end")
                    self.entry_price.delete(0, "end")
                    self.entry_cost.delete(0, "end")
                else:
                    self.label_status.configure(text=f"❌ {msg}", text_color="red")
            except Exception as e:
                self.label_status.configure(text=f"⚠️ Error al conectar con Google Sheets: {e}", text_color="red")
            finally:
                self.btn_save_sale.configure(state="normal", text="📊 Registrar Venta en Sheets")

        threading.Thread(target=worker, daemon=True).start()

if __name__ == "__main__":
    app = VintedApp()
    app.mainloop()
