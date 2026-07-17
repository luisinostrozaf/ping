# keep_alive.py
import requests
import logging
import os
import sys

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')


def ping_database():
    """Hace una consulta ligera a la base de datos para mantenerla activa"""
    supabase_url = os.getenv('SUPABASE_URL')
    supabase_key = os.getenv('SUPABASE_KEY')

    if not supabase_url or not supabase_key:
        logging.error('❌ Faltan variables de entorno SUPABASE_URL o SUPABASE_KEY')
        return False

    try:
        headers = {
            'apikey': supabase_key,
            'Authorization': f'Bearer {supabase_key}'
        }

        response = requests.get(
            f'{supabase_url}/rest/v1/ping_hosts?select=count',
            headers=headers,
            timeout=10
        )

        logging.info(f'📡 Status de la petición: {response.status_code}')
        logging.info(f'📄 Respuesta: {response.text[:500]}')

        if response.status_code == 200:
            logging.info('✅ Base de datos activa')
            return True

        logging.error(f'❌ La petición falló con status {response.status_code}')
        return False

    except Exception as e:
        logging.error(f'❌ Error de conexión: {e}')
        return False


if __name__ == '__main__':
    logging.info('🚀 Ejecutando keep-alive para Supabase')
    success = ping_database()
    if not success:
        sys.exit(1)