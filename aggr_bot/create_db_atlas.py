from bson import decode_all

from tools.pymongo_clients import connect_atlas


def insert_data_in_atlas():
    print(f"Start insert data in MongoDB Atlas")
    client = connect_atlas()
    db = client.sampleDB
    coll = db.sample_collection

    with open('aggr_bot/sampleDB/sample_collection.bson', 'rb') as f:
        data = decode_all(f.read())

    coll.insert_many(data)
    print(f"Insert DONE | nums inserted docs: {coll.count_documents({})}")


if __name__ == "__main__":
    insert_data_in_atlas()
