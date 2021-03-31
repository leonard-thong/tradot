const { json } = require("express");
const express = require("express");
const connectDB = require("./config/db");
var cookieParser = require("cookie-parser");

const app = express();

// Connect Database
connectDB();

// Init Middleware
app.use(express.json({ extended: json }));
app.use(cookieParser());

app.get("/", (req, res) => res.send("API Running"));

// Define Routes
app.use("/api/users", require("./routes/api/users"));
app.use("/api/auth", require("./routes/api/auth"));

// Get Methods
app.use("/get/key", require("./routes/get/key"));
app.use("/get/items", require("./routes/get/items"));
app.use("/get/categories", require("./routes/get/categories"));

// Cart Methods
app.use("/add-to-cart", require("./routes/get/categories"));

const PORT = process.env.PORT || 6000;

app.listen(PORT, console.log(`Server started on port ${PORT}`));
