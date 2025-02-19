import asyncio
from telegram import Update
from telegram.ext import Application, CommandHandler, CallbackContext
import mysql.connector

# Configuración de la base de datos
def connectionBD():
    try:
        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            passwd="",
            database="jugadoras_db"
        )
        print("Conexión exitosa a la base de datos.")
        return mydb
    except mysql.connector.Error as err:
        print(f"Error de conexión: {err}")
        return None

# Obtener información de jugadora por nombre
def obtener_jugadora_por_nombre(nombre):
    db = connectionBD()
    if db is None:
        return None

    cursor = None
    try:
        cursor = db.cursor(dictionary=True)
        print(f"Buscando jugadora con el nombre: {nombre}")
        cursor.execute("SELECT nombre, posicion, nacimiento, biografia FROM jugadoras WHERE nombre LIKE %s", (f"%{nombre}%",))
        jugadora = cursor.fetchone()
        print(f"Resultado de la búsqueda: {jugadora}")
    except mysql.connector.Error as err:
        print(f"Error al ejecutar la consulta: {err}")
        return None
    finally:
        if cursor:
            cursor.close()
        db.close()

    return jugadora

# Función de inicio del bot
async def start(update: Update, context: CallbackContext):
    await update.message.reply_text(
        "¡Hola! ¿De qué jugadora te gustaría saber más? Solo escribe el nombre de la jugadora después de /jugadora."
    )

# Mostrar información de la jugadora
async def mostrar_jugadora(update: Update, context: CallbackContext):
    nombre = " ".join(context.args)
    print(f"Nombre recibido: {nombre}")

    if not nombre:
        await update.message.reply_text("Por favor, escribe el nombre de la jugadora.")
        return

    jugadora = obtener_jugadora_por_nombre(nombre)

    if jugadora:
        message = f"Nombre: {jugadora['nombre']}\n"
        message += f"Posición: {jugadora['posicion']}\n"
        message += f"Fecha de Nacimiento: {jugadora['nacimiento']}\n"
        message += f"Biografía: {jugadora['biografia']}\n"
        await update.message.reply_text(message)

        # Guardar la consulta del usuario en la base de datos (ejemplo)
        guardar_consulta_usuario(update.message.from_user.id, nombre)

    else:
        print(f"No se encontró a la jugadora {nombre}")
        await update.message.reply_text(f"No se encontró a la jugadora {nombre}. Por favor, verifica el nombre e intenta nuevamente.")

# Configuración del bot
async def main():
    application = Application.builder().token("7209595429:AAGL3_uXMm9CetrWPApGBP5MUowmYNIdJXA").build()

    # Definir los comandos
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("jugadora", mostrar_jugadora))

    try:
        await application.run_polling()
    except Exception as e:
        print(f"Ocurrió un error en el polling: {e}")

if __name__ == '__main__':
    # Cambié la manera de correr el bot con asyncio.run(), evitando el problema de "Cannot close a running event loop"
    asyncio.run(main())
