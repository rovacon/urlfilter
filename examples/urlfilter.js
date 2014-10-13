var page = require('webpage').create(),
  system = require('system'),
  t, address;

if (system.args.length != 3) {
  console.log('Usage: loadspeed.js <some URL>');
  phantom.exit();
}

url=system.args[1];
image=system.args[2];
console.log(url);
console.log(image);
page.settings.userAgent = 'Mozilla/5.0 (Linux; Android 4.2.1; en-us; Nexus 4 Build/JOP40D) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.166 Mobile Safari/535.19';
page.open(url, function (status) {
    if (status !== 'success') {
        console.log('Unable to access the network!');
    } else {
        page.render('png/'+image+'.png');
    }
    phantom.exit();
});
