import { Router } from "express";
import tasksQueries from '../queries/tasks.js' 
import { v4 as uuidv4 } from 'uuid';

export const tasksRouter = Router();

const getTasksInRange = (startTime, endTime, sId, res) => {
    tasksQueries.getTasksInDateRange(sId, startTime, endTime, (items) => {
        const pages = items.map(t => ({
            id: t.ID,
            name: t.NAME,
            startTime: t.STARTTIME,
            endTime: t.ENDTIME,
            description: t.DESCRIPTION,
            status: t.STATUS,
            parent: {
                id: t.TASKID,
                name: t.TASKNAME,
                deadline: t.DEADLINE,
                start: t.TASKSTART
            }
        }))
        res.status(200).json(pages)
    })
}
tasksRouter.get("/:scheduleId/tasks", async (req, res) => {
    const { startTime, endTime } = req.query;
    getTasksInRange(startTime,endTime,req.params.scheduleId,res);
})

tasksRouter.get("/:scheduleId/dailyTasks", async (req, res) => {
    const d = new Date(Date.now());

    const startTime = new Date(d);
    startTime.setHours(0, 0, 0, 0);

    const endTime = new Date(d);
    endTime.setHours(23, 59, 59, 999);

    getTasksInRange(startTime,endTime,req.params.scheduleId,res);
})

tasksRouter.patch("/:scheduleId/task/:taskId/update", async (req, res) => {
    const { scheduleId, taskId } = req.params;
    const toChange = Object.entries(req.body)
    tasksQueries.updateTaskById(scheduleId, taskId, toChange, () => {
        res.status(200).send('Task updated')
    })
}) 

tasksRouter.patch("/:scheduleId/task/:taskId/subtask/:subtaskId/update", async (req, res) => {
    const { subtaskId, taskId } = req.params;
    const toChange = Object.entries(req.body)
    tasksQueries.updateSubtaskById(taskId, subtaskId, toChange, () => {
        res.status(200).send('Task updated')
    })
}) 

tasksRouter.post("/:scheduleId/task", async (req, res) => {
    const { scheduleId } = req.params;
    const task = req.body
    console.log("BODY")
    console.log(task)
    const taskId = uuidv4();
    tasksQueries.createTask(scheduleId, taskId, task, () => {
        res.status(200).json({ id: taskId })
    })
}) 

tasksRouter.post("/:scheduleId/task/:taskId/subtask", async (req, res) => {
    const { taskId } = req.params;
    const task = req.body
    console.log("BODY")
    console.log(task)
    const subtaskId = uuidv4();
    tasksQueries.createSubtask(taskId, subtaskId, task, () => {
        res.status(200).json({ id: subtaskId })
    })
}) 

tasksRouter.get("/:scheduleId/task/:taskId", async (req, res) => {
    const { taskId } = req.params;
    tasksQueries.getTaskById(taskId, (t) => {
        res.json({
            name: t.NAME,
            id: t.ID,
            context: t.CONTEXT,
            deadline: t.DEADLINE,
            start: t.TASKSTART,
            status: t.STATUS
        })
    })
})

tasksRouter.get("/:scheduleId/task/:taskId/subtask/:subtaskId", async (req, res) => {
    const { subtaskId } = req.params;
    tasksQueries.getSubtaskById(subtaskId, (t) => {
        res.json({
            name: t.NAME,
            id: t.ID,
            description: t.DESCRIPTION,
            startTime: t.STARTTIME,
            endTime: t.ENDTIME,
            status: t.STATUS,
            parent: t.TASKID
        })
    })
})


tasksRouter.delete("/:scheduleId/task/:taskId", (req, res) => {
    const { taskId } = req.params;
    tasksQueries.deleteTaskById(taskId, () => {
        tasksQueries.deleteSubtasksByTaskId(taskId, () => res.send('Deleted task'))
    })

})

tasksRouter.delete("/:scheduleId/task/:taskId/subtask/:subtaskId", (req, res) => {
    const { subtaskId } = req.params;
    tasksQueries.deleteSubtaskById(subtaskId, () => res.send('Deleted subtask'))
})