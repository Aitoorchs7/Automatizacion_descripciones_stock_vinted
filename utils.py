import re

def extract_vinted_id(url: str) -> str:
    """Extrae el ID numérico de una URL de Vinted.
    Ejemplo: https://www.vinted.es/items/88776655-sudadera-nike -> 88776655
    """
    match = re.search(r'/items/(\d+)', url)
    if match:
        return match.group(1)
    return None
