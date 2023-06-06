from pymongo import MongoClient
from neo4j import GraphDatabase

#Funcion de insercion de datos en MongoDB
def inser_mongo(doc, collec):
    result = collec.insert_one(doc)
    return result

# Connect to MongoDB
mongo_client = MongoClient("mongodb://localhost:27017")
mongo_db = mongo_client["mongo_neo"]
mongo_collection = mongo_db["mongo_neo"]

#Insercion de Datos en MongoDB
documento = {
    "name": "Marie Doe",
    "age": 30,
    "email": "Marie@example.com"
}

#nuevo_dato = inser_mongo(documento, mongo_collection)

# Retrieve data from MongoDB
data_from_mongodb = list(mongo_collection.find())

# Connect to Neo4j
neo4j_driver = GraphDatabase.driver("bolt://localhost:7687", auth=("neo4j", "mauricioapaza"))
neo4j_session = neo4j_driver.session()

# Visualize data in Neo4j
for item in data_from_mongodb:
    # Extract relevant data from MongoDB document
    nombre = item["name"]
    edad = item["age"]
    gmail = item["email"]
    
    # Create nodes and relationships in Neo4j
    cypher_query = "MERGE (ee:Person {name: $name, age: $age, email: $email})"
    neo4j_session.run(cypher_query, name=nombre, age=edad, email=gmail)

    # Create relationships in Neo4j
    cypher_query = "MATCH (a:Person {email: $email1}), (b:Person {email: $email2}) MERGE (a)-[:AMIGO_DE]->(b)"
    neo4j_session.run(cypher_query, email1=gmail, email2="johndoe@example.com")

# Close the connections
mongo_client.close()
neo4j_driver.close()

