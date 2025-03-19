var gplay = require('google-play-scraper');

const passed_variable 	= process.argv[2];

gplay.permissions({appId: passed_variable}).then((data)=>{
	let new_data = JSON.stringify(data);
	console.log(new_data);
});

