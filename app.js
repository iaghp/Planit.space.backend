import express from 'express';
import dotenv from 'dotenv'
import bodyParser from 'body-parser';

dotenv.config();

import tests from './queries/tests.js';
import { tasksRouter } from './routers/tasksRouter.js';

const app = express()
const port = process.env.PORT || 3000

app.use(bodyParser.json());
app.use(express.urlencoded({ extended: true }));

app.use(express.json());

app.get('/', (req, res) => {
  res.send('Hello World!')
})

app.get('/sf', (req, res) => {
  tests.getTestById('asdf23f2rf', (rows) => {
    console.log(rows)
  })
  res.send('Hello World!')
})

app.get('/generate', async (req, res) => {
  let newPlan = {
    name: req.body.name,
    context: req.body.context,
    deadline: req.body.deadline,
    currentTime: new Date().toISOString()
  }
  console.log(newPlan)
  const response = await gemini.generatePlan(newPlan);
  res.send(response)
}
)

app.listen(port, () => {
  console.log(`Example app listening on port ${port}`)
})

app.use("/api/plan/schedule", tasksRouter);
