import { query } from "../db/db.js"


export const getScheduleById = (id, consumer) => 
   query(`SELECT * FROM SCHEDULES WHERE ID = ?`, [id], (r) => consumer(r.length > 0 ? r[0] : null));

export const createSchedule = (userId, scheduleId, name, consumer) => {
    const sql = `
        INSERT INTO SCHEDULES (ID, USERID, NAME)
        VALUES (?, ?, ?)
    `;

    query(sql, [scheduleId, userId, name], consumer)
}

export default {
    getScheduleById,
    createSchedule
}