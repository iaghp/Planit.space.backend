import express from 'express';
import 'dotenv/config'

import db from './db/conn.js';


const app = express()
const port = 3000

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

app.listen(port, () => {
  console.log(`Example app listening on port ${port}`)
})