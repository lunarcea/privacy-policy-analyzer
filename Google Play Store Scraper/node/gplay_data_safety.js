var gplay = require('google-play-scraper');


const passed_variable = process.argv[2];
gplay.datasafety({appId: passed_variable}).then(console.log);

