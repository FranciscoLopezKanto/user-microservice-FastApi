from motor.motor_asyncio import AsyncIOMotorClient
import os

# URI de conexión a MongoDB
MONGO_DETAILS = os.getenv("MONGO_URI", "mongodb://admin:password@localhost:27017")

# Crear el cliente de conexión a MongoDB
client = AsyncIOMotorClient(MONGO_DETAILS)

# Seleccionar la base de datos
database = client['user_database']
users_collection = database['users']

# Función para eliminar duplicados
async def remove_duplicates():
    # Buscar los emails duplicados
    async for user in users_collection.aggregate([
        {"$group": {"_id": "$email", "count": {"$sum": 1}, "docs": {"$push": "$_id"}}},
        {"$match": {"count": {"$gt": 1}}}
    ]):
        # Eliminar duplicados, manteniendo solo uno
        docs_to_remove = user['docs'][1:]  # Mantener el primer documento y eliminar los demás
        await users_collection.delete_many({"_id": {"$in": docs_to_remove}})

# Crear un índice único en el campo 'email' para evitar correos repetidos
async def create_indexes():
    # Eliminar duplicados primero
    await remove_duplicates()
    
    # Crear un índice único en el campo 'email' para evitar correos repetidos
    await users_collection.create_index("email", unique=True)

# Llamar a esta función en el inicio de la aplicación para crear el índice
