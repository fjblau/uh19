var blynkLib = require('blynk-library');
var XMLHttpRequest = require("xmlhttprequest").XMLHttpRequest;
const SDS011Client = require("sds011-client");
const sensor = new SDS011Client("/dev/ttyUSB0");
process.setMaxListeners(20);

var elasticsearch = require('elasticsearch');
var client = new elasticsearch.Client({
  host: '172.104.235.199:9200',
  log: 'error'
});

var AUTH = '1556e875382044bfbbb866b9eff5e558';
var blynk = new blynkLib.Blynk(AUTH);

var aqi10val = 0
var aqi25val = 0
var aqi10Category = ""
var aqi25Category = ""
var pm10Corr = 0
var pm25Corr = 0
var aqi10Corrval = 0
var aqi25Corrval = 0
var aqi10CorrCategory = ""
var aqi25CorrCategory = ""
		
function Get(yourUrl){
    var Httpreq = new XMLHttpRequest(); // a new request
    Httpreq.open("GET",yourUrl,false);
    Httpreq.send(null);
    return Httpreq.responseText;
}

function calcCorr(hum, pm) {
	return hum <= 80 ? (.47 * pm) + 5.08
         : hum > 80 && hum <= 90 ? (.41 * pm) + 3.32
         : hum > 90 ? (.37 * pm) + 2.63
         : pm;
}
         
let canQuit = false;
let aqibot = require('aqi-bot');

function listenForReading() {
    sensor.on('reading', r => {
        console.log('Got reading: '+ new Date());
        console.log(r);
		
		try {
        	var json_obj = JSON.parse(Get('http://api.weatherlink.com/v1/NoaaExt.json?user=001D0A0100EE&pass=2Ellbelt!&apiToken=B1A41C82525B4BB7AB170F5915D7C316'));
        } catch(e) {
        	console.log(e);
        }
        
        try {
        	var inTemp = json_obj.temp_c;
        	var inHum = json_obj.relative_humidity;
        	var dewpoint =  json_obj.dewpoint_c;
        } catch(e) {
        	var inTemp = 0;
        	var inHum = 0;
        	var dewpoint = 0;
        }
		
		var pm10Corr = calcCorr(parseFloat(inHum), r.pm10).toFixed(1);
		var pm25Corr = calcCorr(parseFloat(inHum), r.pm2p5).toFixed(1);
		
		aqibot.AQICalculator.getAQIResult("PM10", r.pm10).then((result) => {
    		//console.log(result.aqi)
    		aqi10val = result.aqi
    		aqi10Category = result.category;
  		}).catch(err => {
    		console.log(err);
  		})
		
		aqibot.AQICalculator.getAQIResult("PM2.5", r.pm2p5).then((result) => {
    		//console.log(result.aqi)
    		aqi25val = result.aqi
    		aqi25Category = result.category;
  		}).catch(err => {
    		console.log(err);
  		})
  		
  		aqibot.AQICalculator.getAQIResult("PM2.5", pm25Corr).then((result) => {
    		//console.log(result.aqi)
    		aqi25Corrval = result.aqi
    		aqi25CorrCategory = result.category;
  		}).catch(err => {
    		console.log(err);
  		})
		
		aqibot.AQICalculator.getAQIResult("PM10", pm10Corr).then((result) => {
    		//console.log(result.aqi)
    		aqi10Corrval = result.aqi
    		aqi10CorrCategory = result.category;
  		}).catch(err => {
    		console.log(err);
  		})
  		
  		blynk.virtualWrite(2, pm25Corr)
        blynk.virtualWrite(3, pm10Corr)
        blynk.virtualWrite(1, inTemp);
        blynk.virtualWrite(4, inHum);
		blynk.virtualWrite(5, aqi10Corrval);
        blynk.virtualWrite(6, aqi25Corrval);
        blynk.virtualWrite(7, aqi10CorrCategory);
        blynk.virtualWrite(8, aqi25CorrCategory);
		
		console.log("Humidity: ", inHum, " Corrected: ", "PM25: ", pm25Corr, "PM10: ", pm10Corr);

		client.create({
  		index: 'sds011',
  		id: 'sds011'+Date.now().toString(),
  		type: 'sensor',
  		
  		body: {
  			timestamp: new Date(),
    		pm25: r.pm2p5,
    		pm10: r.pm10,
    		aqi10: aqi10val,
    		aqi25: aqi25val,
    		aqi10Cat: aqi10Category,
    		aqi25Cat: aqi25Category,
    		tempFl: parseFloat(inTemp),
    		humFl: parseFloat(inHum),
    		dewpointFl: parseFloat(dewpoint),
    		corrpm10Fl: parseFloat(pm10Corr),
    		corrpm25Fl: parseFloat(pm25Corr),
    		aqi10CorrvalFl: parseFloat(aqi10Corrval),
			aqi25CorrvalFl:  parseFloat(aqi25Corrval),
			aqi10CorrCategory: aqi10CorrCategory,
			aqi25CorrCategory: aqi25CorrCategory
  			}
		});
        canQuit = true;
    });
}

Promise
    .all([sensor.setReportingMode('active'), sensor.setWorkingPeriod(1)])
    .catch(err => {
            console.log(err);
        })
    .then(() => {
        // everything's set
        listenForReading();
    });

let waitCount = 0;

function waitToQuit() {
    waitCount++;
    if (canQuit || waitCount > 10)
    	//return process.kill(process.pid);
        return;
    console.log('Waiting for reading');
    setTimeout(() => {
        waitToQuit();
    },1000);
}

waitToQuit();
