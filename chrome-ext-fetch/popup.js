console.log("background is running!");
var interval = 30000; // this is 10 sec. 3 days: 259200000
var startTime = Date.now() - interval;

function searchQueryFetch() {
    chrome.history.search({text: '', startTime: startTime, endTime: Date.now(), maxResults: 1000}, function(data) {
        var urls = "";
        var pageTitles = "";
        var timestamps = "";
        for (var i = 0; i < data.length; i++) {
            urls += data[i].url + ",";
            pageTitles += data[i].title + ",";
            timestamps += data[i].visitTime + ",";
        }
        lst = ['user', urls, pageTitles, timestamps]
        // postToAPI(lst)
    });
}

setInterval(searchQueryFetch, interval);

async function postToAPI(lst) {
    const dict = {
        'username': lst[0],
        'urls': lst[1],
        'titles': lst[2],
        'timestamps': lst[3]
    }
    const contents = {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(dict)
      };
    // Send the POST request
    const response = await fetch('http://127.0.0.1:5000/send-browser-history', contents)
    .then(response => {
        console.log('Response status:', response.status);
        return response.json();
    })
    .then(data => {
        console.log('Response data:', data);
    })
    .catch(error => {
        console.error('Error:', error);
        console.log(contents.body);
    });      
    console.log(response);
  }

  