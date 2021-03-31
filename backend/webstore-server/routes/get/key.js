const express = require("express");
const router = express.Router();

// @route   POST api/users
// @desc    Test route
// @access  Public
router.post("/", async (req, res) => {
    res.send("");
});

module.exports = router;
