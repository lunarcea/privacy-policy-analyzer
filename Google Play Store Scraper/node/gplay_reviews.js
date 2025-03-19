var gplay = require('google-play-scraper');


const passed_variable 	= process.argv[2];
const num_reviews 		= process.argv[3];
let page_token 			= process.argv[4];

if(page_token == "first"){
	page_token = null;
}

gplay.reviews({
	appId: passed_variable,
	num: num_reviews,
	nextPaginationToken: page_token
}).then((data)=>{
	// let new_data = JSON.parse(JSON.stringify(data));
	let new_data = JSON.stringify(data);
	console.log(new_data);
	// console.log(eval('{'+data+'}'));
});

