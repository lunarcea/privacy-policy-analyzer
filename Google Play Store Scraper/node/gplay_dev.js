var gplay = require('google-play-scraper');


const passed_variable = process.argv[2];
gplay.developer({devId: passed_variable}).then((data)=>{
	// let new_data = JSON.parse(JSON.stringify(data));
	let new_data = JSON.stringify(data);
	console.log(new_data);
	// console.log(eval('{'+data+'}'));
});

