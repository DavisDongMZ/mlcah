const express = require('express');
const { exec } = require('child_process');
const app = express();

app.use(express.static('frontend'));

// ignore this function
app.get('/run', (req, res) => {
    exec('python3 backend/parse_tree.py', (error, stdout, stderr) => {
      if (error) return res.status(500).send(stderr);
      try {
        const json = JSON.parse(stdout);
        res.json(json);
      } catch (err) {
        res.status(500).send("Invalid JSON from Python");
      }
    });
  });


app.listen(3000, () => {
  console.log('Server running at http://localhost:3000');
});