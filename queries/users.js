import { query } from "../db/db.js"

export const getUserById = (id, consumer) => 
   query(`SELECT * FROM USERS WHERE id = ?`, [id], (r) => consumer(r.length > 0 ? r[0] : null));

export const getUsersByIds = (ids, consumer) => 
   query(`SELECT * FROM USERS WHERE id IN (${ids.map(() => '?').join(', ')})`, ids, consumer);


export default {
    getUserById,
    getUsersByIds
}