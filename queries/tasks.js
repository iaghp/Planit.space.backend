import { query } from "../db/db.js"

export const getTaskById = (id, consumer) => 
   query(`SELECT * FROM TASKS WHERE ID = ?`, [id], (r) => consumer(r.length > 0 ? r[0] : null));

export const getTasksByIds = (ids, consumer) => 
   query(`SELECT * FROM TASKS WHERE id IN (${ids.map(() => '?').join(', ')})`, ids, consumer);

export const getSubtaskById = (id, consumer) => 
   query(`SELECT SUBTASKS.*, TASKS.DEADLINE,TASKS.TASKSTART, TASKS.NAME as TASKNAME FROM TASKS INNER JOIN SUBTASKS ON TASKS.ID = SUBTASKS.TASKID  WHERE ID = ?`, [id], (r) => consumer(r.length > 0 ? r[0] : null));

export const getSubtasksByIds = (ids, consumer) => 
   query(`SELECT SUBTASKS.*, TASKS.DEADLINE,TASKS.TASKSTART, TASKS.NAME as TASKNAME FROM TASKS INNER JOIN SUBTASKS ON TASKS.ID = SUBTASKS.TASKID WHERE id IN (${ids.map(() => '?').join(', ')})`, ids, consumer);

export const getTasksInDateRange = (scheduleId, s, e, consumer) => 
   query(`SELECT SUBTASKS.*, TASKS.DEADLINE,TASKS.TASKSTART, TASKS.NAME as TASKNAME FROM TASKS INNER JOIN SUBTASKS ON TASKS.ID = SUBTASKS.TASKID WHERE SCHEDULEID = ? AND subtasks.startTime <= ? AND subtasks.endTime >= ? ORDER BY subtasks.startTime`, [scheduleId, e, s], consumer);

export const getSubtasksByTaskId = (taskId, consumer) =>
   query(`SELECT SUBTASKS.*, TASKS.DEADLINE,TASKS.TASKSTART, TASKS.NAME as TASKNAME FROM TASKS INNER JOIN SUBTASKS ON TASKS.ID = SUBTASKS.TASKID  WHERE TASKS.ID = ? ORDER BY SUBTASKS.endTime`, [taskId], consumer);
/*
export const getSubtasksInDateRange = (scheduleId, s, e, consumer) => 
   query(`SELECT * FROM SUBTASKS INNER JOIN TASKS ON TASKS.ID = SUBTASKS.TASKIDWHERE SCHEDULEID = ? AND startTime <= ? AND endTime >= ?`, [scheduleId, s, e], consumer);
*/
export const updateTaskById = (scheduleId, id, fields, consumer) => 
    query(`UPDATE TASKS SET ${fields.map((f) => `${f[0].toUpperCase()} = ?`).join(',')} WHERE SCHEDULEID = ? AND ID = ?`, [...fields.map(f => f[1]), scheduleId, id], consumer)

export const updateSubtaskById = (taskId, id, fields, consumer) => 
    query(`UPDATE SUBTASKS SET ${fields.map((f) => `${f[0].toUpperCase()} = ?`).join(',')}  WHERE TASKID = ? AND ID = ?`, [...fields.map(f => f[1]), taskId, id], consumer)

export const updateTasksByIds = (ids, fields, consumer) => 
    query(`UPDATE TASKS SET ${fields.map((f) => `${f[0].toUpperCase()} = ?`).join(',')} WHERE IN (${ids.map(() => '?').join(', ')})`, fields.map(f => f[1]).flat() + ids, consumer)

export const updateSubtasksByIds = (ids, fields, consumer) => 
    query(`UPDATE SUBTASKS SET ${fields.map((f) => `${f[0].toUpperCase()} = ?`).join(',')} WHERE IN (${ids.map(() => '?').join(', ')})`, fields.map(f => f[1]).flat() + ids, consumer)

export const deleteTaskById = (id, consumer) => 
    query(`DELETE FROM TASKS WHERE ID = ?`, [id], consumer)

export const deleteSubtaskById = (id, consumer) => 
    query(`DELETE FROM SUBTASKS WHERE ID = ?`, [id], consumer)

export const deleteTasksByIds = (ids, consumer) => 
   query(`DELETE FROM TASKS WHERE ID IN (${ids.map(() => '?').join(', ')})`, ids, consumer);

export const deleteSubtasksByIds = (ids, consumer) => 
   query(`DELETE FROM SUBTASKS WHERE ID IN (${ids.map(() => '?').join(', ')})`, ids, consumer);

export const deleteSubtasksByTaskId = (taskId, consumer) => 
    query(`DELETE FROM SUBTASKS WHERE TASKID = ?`, [taskId], consumer);


export const createTask = (scheduleId, id, task, consumer) => {
    const sql = `
        INSERT INTO TASKS (ID, NAME, SCHEDULEID, TASKSTART, DEADLINE, CONTEXT, STATUS)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    `;
    query(sql, [id, task.name, scheduleId, task.start, task.deadline, task.context, task.status ?? 'PLANNED'], consumer)
}

export const createSubtask = (taskId, id, task, consumer) => {
    const sql = `
        INSERT INTO SUBTASKS (ID, NAME, DESCRIPTION, STARTTIME, ENDTIME, TASKID, STATUS)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    `;
    query(sql, [id, task.name, task.description, task.startTime, task.endTime, taskId, task.status ?? 'PLANNED'], consumer)
}

export default {
    getTaskById,
    getTasksByIds,
    getSubtaskById,
    getSubtasksByIds,
    getTasksInDateRange,
    getSubtasksByTaskId,
    //getSubtasksInDateRange,
    updateTaskById,
    updateSubtaskById,
    updateTasksByIds,
    updateSubtasksByIds,
    deleteTaskById,
    deleteSubtaskById,
    deleteTasksByIds,
    deleteSubtasksByIds,
    deleteSubtasksByTaskId,
    createTask,
    createSubtask
}