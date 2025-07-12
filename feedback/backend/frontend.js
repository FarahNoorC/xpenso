require("dotenv").config();
const express = require("express");
const bodyParser = require("body-parser");
const nodemailer = require("nodemailer");
require("dotenv").config();
const cors = require("cors");
const app = express();

app.use(cors());
app.use(bodyParser.json());

app.post("/api/feedback", async (req, res) => {
  const { name, email, message } = req.body;

  const transporter = nodemailer.createTransport({
    service: "gmail",
    auth: {
      user: process.env.EMAIL,
      pass: process.env.PASSWORD,
    },
  });

  await transporter.sendMail({
    from: email,
    to: process.env.EMAIL,
    subject: `Feedback from ${name}`,
    text: message,
  });

  res.send({ message: "Feedback sent" });
});

app.listen(3000, () => console.log("Server running on port 3000"));
