console.log("background is running!");
var interval = 259200000; // this is 10 sec. 3 days: 259200000
var startTime = Date.now() - interval;

function searchQueryFetch() {
    chrome.history.search({text: '', startTime: Date.now() - startTime, endTime: Date.now(), maxResults: 1000}, function(data) {
        var urls = "";
        var pageTitles = "";
        var timestamps = "";
        for (var i = 0; i < data.length; i++) {
            urls += data[i].url + ",";
            pageTitles += data[i].title + ",";
            timestamps += data[i].visitTime + ",";
        }
        lst = ['arvind6902@gmail.com', urls, pageTitles, timestamps]
        postToAPI(lst)
    });
}

searchQueryFetch()
// setInterval(searchQueryFetch, interval);

async function postToAPI(lst) {
    const dict = {
        'username': lst[0],
        'urls': lst[1],
        'titles': lst[2],
        'timestamps': lst[3]
    }
    
    const rawResponse = await fetch('http://127.0.0.1:5000/send-browser-history', {
        Method: 'POST',
        Headers: {
            Accept: 'application.json',
            'Content-Type': 'application/json'
        },
        Body: JSON.stringify(dict),
    })
    console.log(rawResponse.json())
}
