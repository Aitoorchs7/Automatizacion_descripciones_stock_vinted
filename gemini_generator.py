import json
from google import genai
from google.genai import types

class GeminiGenerator:
    def __init__(self, api_key):
        self.client = genai.Client(api_key=api_key)
        
    def generate_descriptions(self, brand, item, size, cond, keywords):
        base_prompt = """Contexto: Actúa como un experto en reventa de moda premium y vintage en plataformas como Vinted. Tu objetivo es generar descripciones optimizadas, títulos magnéticos y organizar mi inventario.

Reglas de Formato para Descripciones:
Para cada prenda que te proporcione, debes generar una estructura fija:

Título Optimizado: Debe tener entre 90 y 100 caracteres exactos. Debe incluir: Marca + Modelo/Tipo + Talla + Color + Estética principal (ej. Old Money, Bloke Core, Grunge) + Keywords clave.
Sección ✨ Esencia: Breve párrafo que venda el "vibe" o concepto de la prenda.
Sección 🎨 Color: Descripción detallada del tono y contrastes.
Sección 📏 Talla: Especificar talla y tipo de corte (Classic Fit, Slim Fit, Baggy, etc.).
Sección 🧵 Detalles de Confección: Lista con puntos sobre materiales, logotipos bordados, herrajes y acabados técnicos.
Sección 💎 Estética: Sugerir estilos específicos (Quiet Luxury, Preppy, Y2K, Indie Sleaze) y cómo combinar la prenda.
Sección 🌟 Estado: Descripción del estado de conservación.
Bloque de Hashtags: Generar una lista de 10-12 hashtags relevantes incluyendo marca, talla, estética y país.

Reglas de Gestión de Inventario:
Al final, muestra una Tabla de Inventario Actualizado con las columnas: | Marca/Prenda | Talla | Estética | Título Sugerido |.

INSTRUCCIÓN CRÍTICA:
Genera exactamente 5 variaciones de descripción INCREÍBLES e independientes basadas en estos datos:
- Marca: {brand}
- Prenda (Modelo/Tipo): {item}
- Talla y Corte: {size}
- Estado: {cond}
- Keywords/Estética(s) y Detalles: {keywords}

Cada variación debe sentirse *única* y utilizar tonos ligeramente distintos (e.g. 1. Técnica, 2. Storytelling / Vibe, 3. Directa y al grano, 4. Enfocada a Estética Vintage, 5. Premium Quiet Luxury) pero respetando siempe las "Reglas de Formato". Cada variación debe incluir la tabla final obligatoriamente.

DEVUELVE EL RESULTADO ÚNICAMENTE EN FORMATO JSON puro, siguiendo EXACTAMENTE esta estructura:
{{
  "variacion_1": "Título y toda la descripción completas...",
  "variacion_2": "Título y toda la descripción completas...",
  "variacion_3": "...",
  "variacion_4": "...",
  "variacion_5": "..."
}}
"""
        prompt = base_prompt.format(brand=brand, item=item, size=size, cond=cond, keywords=keywords)
        
        try:
            response = self.client.models.generate_content(
                model='gemini-2.5-flash',
                contents=prompt
            )
            text_res = response.text
            # Limpieza de código por si la IA devuelve formato markdown (```json o ```)
            text_res = text_res.replace("```json", "").replace("```", "").strip()
            # Parseamos para asegurar de que es un JSON estructurado
            return json.loads(text_res)
        except json.JSONDecodeError as e:
            return {"error": f"Error al parsear el resultado de Gemini: {str(e)}", "raw": text_res}
        except Exception as ex:
            return {"error": f"Error de conexión con Gemini API: {str(ex)}", "raw": ""}
