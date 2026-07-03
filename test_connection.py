from database.mongodb import get_collection, get_database, get_mongodb

client = get_mongodb().client
print("Databases:", client.list_database_names())

db = get_database()
print("Collections:", db.list_collection_names())

students = get_collection("students")
print("Count:", students.count_documents({}))
