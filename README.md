# 🏷️ E-Commerce Sales & Content Automator

[![Status](https://img.shields.io/badge/Status-En_Desarrollo-green.svg)]()
[![Interface](https://img.shields.io/badge/UI-Minimalista-blue.svg)]()

Optimiza el flujo de trabajo para vendedores en plataformas de segunda mano y e-commerce. Esta herramienta integra generación de contenido persuasivo mediante IA/Templates y automatización de registros contables en un solo entorno.

---

## 🚀 Funcionalidades Principales

El sistema se divide en dos módulos independientes pero complementarios:

### 1. Generador de Descripciones Inteligentes
A partir de atributos básicos de la prenda, el motor genera:
* **Variedad:** 5 propuestas de descripción con diferentes tonos (profesional, casual, persuasivo, etc.).
* **SEO & Visibilidad:** Selección dinámica de **hashtags estratégicos** para maximizar el alcance en buscadores internos.
* **Interfaz Simple:** Diseño orientado a la eficiencia del usuario (UX/UI).

### 2. Tracker de Ventas (Automatización de Excel)
Procesamiento de datos mediante el enlace de la prenda vendida:
* **Extracción Automática:** Obtención de ID de producto, precio de venta y fecha.
* **Cálculo de Métricas:** Determinación de **ganancia neta**, considerando ofertas aceptadas y comisiones.
* **Persistencia:** Exportación directa a un archivo centralizado en formato `.xlsx` (Excel).

---

## 📊 Estructura de Datos (Output Excel)

El registro en el archivo Excel sigue el siguiente esquema técnico:

| Columna | Descripción | Ejemplo |
| :--- | :--- | :--- |
| **ID_PRODUCTO** | Identificador único de la prenda | `VINT-99281` |
| **FECHA_VENTA** | Fecha del cierre de transacción | `2026-04-20` |
| **PRECIO_FINAL** | Importe pagado por el comprador | `45.00 €` |
| **OFERTA** | Indica si se aceptó una contraoferta | `Sí / No` |
| **GANANCIA** | Resultado neto tras gastos | `32.50 €` |

---

## 🛠️ Stack Tecnológico
* **Core:** Motor de lógica para procesamiento de strings y scraping.
* **UI:** Interfaz gráfica ligera para interacción de usuario.
* **Storage:** Integración con librerías de manipulación de hojas de cálculo (Excel).
* **Security:** Gestión de credenciales mediante variables de entorno aisladas.

---

## 📦 Instalación y Uso

1. **Clonar Repositorio:**
   ```bash
   git clone [https://github.com/Aitoorchs7/Automatizacion_descripciones_stock_vinted.git](https://github.com/Aitoorchs7/Automatizacion_descripciones_stock_vinted.git)
