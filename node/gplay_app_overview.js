// gplay_app_overview.js
// Retrieves app overview information from Google Play Store
const gplay = require('google-play-scraper');

const appId = process.argv[2];

gplay.app({appId: appId})
  .then((data) => {
    const jsonData = JSON.stringify(data);
    console.log(jsonData);
  })
  .catch(err => {
    console.error('Error fetching app data:', err);
    process.exit(1);
  });

// -----------------------------------------------------------------

// gplay_data_safety.js
// Retrieves app data safety information from Google Play Store
const gplay = require('google-play-scraper');

const appId = process.argv[2];

gplay.datasafety({appId: appId})
  .then(data => {
    console.log(JSON.stringify(data));
  })
  .catch(err => {
    console.error('Error fetching data safety information:', err);
    process.exit(1);
  });

// -----------------------------------------------------------------

// gplay_dev.js
// Retrieves developer information from Google Play Store
const gplay = require('google-play-scraper');

const devId = process.argv[2];

gplay.developer({devId: devId})
  .then((data) => {
    const jsonData = JSON.stringify(data);
    console.log(jsonData);
  })
  .catch(err => {
    console.error('Error fetching developer data:', err);
    process.exit(1);
  });

// -----------------------------------------------------------------

// gplay_permissions.js
// Retrieves app permissions information from Google Play Store
const gplay = require('google-play-scraper');

const appId = process.argv[2];

gplay.permissions({appId: appId})
  .then((data) => {
    const jsonData = JSON.stringify(data);
    console.log(jsonData);
  })
  .catch(err => {
    console.error('Error fetching app permissions:', err);
    process.exit(1);
  });

// -----------------------------------------------------------------

// gplay_reviews.js
// Retrieves app reviews from Google Play Store
const gplay = require('google-play-scraper');

const appId = process.argv[2];
const numReviews = process.argv[3];
let pageToken = process.argv[4];

// Handle first page case
if (pageToken === "first") {
  pageToken = null;
}

gplay.reviews({
  appId: appId,
  num: numReviews,
  nextPaginationToken: pageToken
})
  .then((data) => {
    const jsonData = JSON.stringify(data);
    console.log(jsonData);
  })
  .catch(err => {
    console.error('Error fetching app reviews:', err);
    process.exit(1);
  });