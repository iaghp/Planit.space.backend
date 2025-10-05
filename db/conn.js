import { MongoClient } from "mongodb";

export const client = new MongoClient(process.env.MONGODB_CONNECTION_STRING);
const database = client.db(process.env.MONGODB_DATABASE_NAME);

export const findOne = async (collection, q) => {
    const col = database.collection(collection);
    return col.findOne(q)
}

export const find = async (collection, q) => {
    const col = database.collection(collection);
    return col.find(q)
}

export const insertOne = async (c, d) => {
    const col = database.collection(c);
    const r = await col.insertOne(d);
    console.log(r)
    console.log(
        `A document was inserted with the _id: ${r.insertedId}`,
    );
    return r;
}

export const insertMany = async (c, d) => {
    try {
        const col = database.collection(c);
        const insertManyresult = await col.insertMany(d);
        let ids = insertManyresult.insertedIds;
        console.log(`${insertManyresult.insertedCount} documents were inserted.`);
        for (let id of Object.values(ids)) {
            console.log(`Inserted a document with id ${id}`);
        }
    } catch(e) {
        console.log(`A MongoBulkWriteException occurred, but there are successfully processed documents.`);
        let ids = e.result.result.insertedIds;
        for (let id of Object.values(ids)) {
            console.log(`Processed a document with id ${id._id}`);
        }
        console.log(`Number of documents inserted: ${e.result.result.nInserted}`);
    }
}

export default {
    findOne,
    find,
    insertOne,
    insertMany
}