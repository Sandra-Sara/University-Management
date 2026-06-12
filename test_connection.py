from database.mongodb import mongodb

client = mongodb.client
print("Databases:", client.list_database_names())

db = mongodb.db
print("Collections:", db.list_collection_names())

students = mongodb.get_collection("students")
print("Count:", students.count_documents({}))
