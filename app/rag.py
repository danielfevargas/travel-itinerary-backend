import json
import os

def get_travel_context(presupuesto: str, ritmo: str, tipo_viajero: str) -> str:
    """Recupera el contexto de reglas del negocio desde el JSON"""
    base_dir = os.path.dirname(__file__)
    json_path = os.path.join(base_dir, "data", "destinations.json")
    
    with open(json_path, "r", encoding="utf-8") as f:
        rules = json.load(f)
    
    presupuesto_info = rules["presupuesto"].get(presupuesto, rules["presupuesto"]["moderado"])
    ritmo_info = rules["ritmo"].get(ritmo, rules["ritmo"]["equilibrado"])
    tipo_info = rules["tipo_viajero"].get(tipo_viajero, rules["tipo_viajero"]["solo"])
    
    context = f"""
- Presupuesto ({presupuesto}): {presupuesto_info}
- Ritmo ({ritmo}): {ritmo_info}
- Tipo de viajero ({tipo_viajero}): {tipo_info}
"""
    return context