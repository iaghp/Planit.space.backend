import { query } from "../db/db.js"

export const getTestById = (id, consumer) => 
   query(`SELECT * FROM TEST WHERE id = ?`, [id], (r) => consumer(r.length > 0 ? r[0] : null));

export const getTestsByIds = (ids, consumer) => 
   query(`SELECT * FROM TEST WHERE id IN (${ids.map(() => '?').join(', ')})`, ids, consumer);


export default {
    getTestById,
    getTestsByIds
}