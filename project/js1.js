const express = require('express');
const mysql = require('mysql');
const bodyParser = require('body-parser');

const app = express();
const port = 3000;

// MySQL connection
const db = mysql.createConnection({
  host: 'localhost',
  user: 'kuvam',
  password: 'ABc()!?12=%',
  database: 'project1',
});

db.connect((err) => {
  if (err) {
    console.error('Error connecting to MySQL: ', err);
  } else {
    console.log('Connected to MySQL');
  }
});

// Middleware for parsing JSON and form data
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: true }));

// Routes
app.post('/submit-form', (req, res) => {
  const { eid, name, did, department } = req.body;
  const sql = 'INSERT INTO employee (eid, name, did, department) VALUES (?, ?, ?, ?)';
  
  // Use parameterized query to prevent SQL injection
  db.query(sql, [eid, name, did, department], (err, result) => {
    if (err) {
      console.error('Error inserting data: ', err);
      // Return detailed error message in the response
      res.status(500).json({ error: 'Internal Server Error', details: err.message });
    } else {
      res.status(200).json({ success: true, message: 'Form data submitted successfully' });
    }
  });
});

// Start the server
app.listen(port, () => {
  console.log(`Server running on http://localhost:${port}`);
});
