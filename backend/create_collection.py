import os
from dotenv import load_dotenv
from pymilvus import (
    connections,
    FieldSchema,
    CollectionSchema,
    DataType,
    Collection,
    utility
)

load_dotenv()

ZILLIZ_URI = os.getenv("ZILLIZ_URI")
ZILLIZ_TOKEN = os.getenv("ZILLIZ_TOKEN")

connections.connect(
    alias="default",
    uri=ZILLIZ_URI,
    token=ZILLIZ_TOKEN
)

collection_name = "movies"

# Drop if exists (clean setup)
if utility.has_collection(collection_name):
    utility.drop_collection(collection_name)
    print("Old collection dropped.")

# Define schema (384-dim for MiniLM)
fields = [
    FieldSchema(name="id", dtype=DataType.INT64, is_primary=True),
    FieldSchema(name="embedding", dtype=DataType.FLOAT_VECTOR, dim=384)
]

schema = CollectionSchema(fields, description="Movie Embeddings")

collection = Collection(name=collection_name, schema=schema)

# Create index
index_params = {
    "metric_type": "L2",
    "index_type": "IVF_FLAT",
    "params": {"nlist": 128}
}

collection.create_index(
    field_name="embedding",
    index_params=index_params
)

print("✅ Collection and index created successfully!")