import psycopg2

def connect_db():
    try:
        db_name = "postgres"
        db_user = "postgres.qbuasbakuzpbyqhmbvtp"
        db_pass = "}8Z$I0v]Yt4m"
        db_host = "aws-0-us-east-1.pooler.supabase.com"
        db_port = "6543"
        connection = psycopg2.connect(dbname=db_name, user=db_user, password=db_pass, host=db_host, port=db_port)
        return connection
    except Exception as e:
        print(f"Error al conectar a la base de datos: {e}")
        return None

def close_db(connection):
    if connection:
        try:
            connection.close()
        except Exception as e:
            print(f"Error al cerrar a la base de datos: {e}")
