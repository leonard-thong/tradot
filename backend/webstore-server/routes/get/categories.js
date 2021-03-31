const express = require("express");
const router = express.Router();
var request = require("request");

// @route   GET api/auth
// @desc    Test route
// @access  Public
router.get("/", async (req, res) => {
    try {
        var options = {
            method: "GET",
            url: "http://localhost:5000/catalog/items",
            headers: {
                "Content-Type": "application/json",
                Authorization:
                    "AccessKey 8637f896dfbc4d70a5fd07948e63db58:W1rpW7da92bqaC2FJdMBnzDbcgYmqCKOg1GMInVj62OH4geoqWj0IL6dtVxtvvmI0VSjMt4/aiPRgeyOBxxk2Q==",
                "nep-organization": "d2ca6f1390504943a1705b6d7fb8a70a",
                Date: "Sun, 18 Oct 2020 00:59:00 GMT",
                Accept: "application/json",
                "Accept-Language": "en-us",
            },
        };
        request(options, function (error, response) {
            if (error) throw new Error(error);
            let array = [];
            let ans = JSON.parse(response.body);

            // array of items : ans.pageContent
            let list = ans.pageContent;

            list.forEach((e) => {
                if (e.status === "ACTIVE") {
                    array.push(e);
                }
            });

            res.send(array);
        });
    } catch (error) {
        console.error(error.message);
        res.status(500).send("Server error");
    }
});

module.exports = router;
