import express from 'express';
import 'dotenv/config'

import db from './db/conn.js';
import gemini from './services/gemini.js';


const app = express()
const port = 3000

app.use(express.json());

app.get('/', (req, res) => {
  res.send('Hello World!')
})


app.get('/test', (req, res) => {
  db.insertOne('users', {
    name: "Bob",
    schedule: "3424324234fsdfjisd"
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