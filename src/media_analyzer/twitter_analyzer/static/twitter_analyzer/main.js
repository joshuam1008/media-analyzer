var categories = ['stream', 'sentiment']
var ids = []
let summary = {
    positive: 0,
    negative: 0,
    neutral: 0
}
// listen to button click and send value to api

stream_active = false;
fetch_every_second = null;

// google.charts.load('current', {packages: ['corechart']});
// google.charts.setOnLoadCallback(drawChart);


$(".stream-ctrl").click(async function () {
    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;

    //raw button value from its html 'value' property
    let button_value = $(this).val();
    //split the buttton value by its spacing (such as "stream 1" to [stream, 1])
    button_value_as_arr = button_value.split(" ");

    //the first element of the value property- its name
    button_value_name = button_value_as_arr[0];

    //the second element of the value property- the value
    button_value_integer = parseInt(button_value_as_arr[1]);

    // if stream being toggled, toggle stream_active
    if (button_value_integer == 0) {
        stream_active = !stream_active;
        // change button text to reflect stream status
        if (stream_active) {
            fetch_every_second = setInterval(fetch_result, 1000);
            $(this).text("Stop Analysis");
        } else {
            clearInterval(fetch_every_second);
            $(this).text("Start Analysis");
        }
    }

    //post a request to the server with the button details
    const response = await fetch('/twitter/toggle_modules', {
        method: 'POST',
        body: JSON.stringify({
            name: button_value_name,
            state: button_value_integer
        }),
        headers: {
            'Accept': 'application/json, text/plain, */*',
            'Content-Type': 'application/json',
            "X-CSRFToken": csrftoken
        }
    })
    // alert(`module is ${value[0]} value is ${value[1]}.`);
});

var add_tweet_to_ui = (tweet) => {
    const tweet_as_link = document.createElement("a");
    tweet_as_link.classList.add("list-group-item");
    tweet_as_link.classList.add("list-group-item-action");

    tweet_as_link.innerHTML = tweet.text;

    // make the tweet green if positive, red if negative, and gray if neutral for tweet.sentiment
    if (tweet.sentiment == "POSITIVE") {
        tweet_as_link.classList.add("list-group-item-success");
    } else if (tweet.sentiment == "NEGATIVE") {
        tweet_as_link.classList.add("list-group-item-danger");
    } else if (tweet.sentiment == "NEUTRAL") {
        tweet_as_link.classList.add("list-group-item-dark");
    }

    const list = document.querySelector('#tweets');
    list.appendChild(tweet_as_link);
}

//note: chen's code I (David) adapted.
var generate_overall_sentiment_result = function(position, overall_sentiment_results){

    //convert dictionary to format of datatable
    var convert_dict_to_data_table = function(overal_sentiment_results){
        let single_result = overall_sentiment_results
        let data = [['Emo Level','Counts']]
        for(let [category,value] of Object.entries(single_result)){
            data.push([category,value])
        }
        return data
    }
    function plot_barchart(position,overall_sentiment_results) {
        function drawChart(tag_name,data) {
            let histogram_data = google.visualization.arrayToDataTable(data);
    
            let options = {
                title: 'Overall Sentiment',
                legend: {
                    position: 'none'
                },
            };

            let chart = new google.visualization.BarChart(tag_name);
            chart.draw(histogram_data, options);
        }
        google.charts.load("current", {
            packages: ["corechart"]
        });
        google.charts.setOnLoadCallback(
            () =>{drawChart(position, convert_dict_to_data_table(overall_sentiment_results))
            });
    

    
    }
    plot_barchart(position,overall_sentiment_results)
}

var fetch_result = async function () {
    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    const response = await fetch('/twitter/fetch_result', {
        method: 'POST',
        body: JSON.stringify({
            id: ids,
            category: categories
        }),
        headers: {
            'Accept': 'application/json, text/plain, */*',
            'Content-Type': 'application/json',
            "X-CSRFToken": csrftoken
        }
    });

    const add_tweet = (tweet_id) => {
        tweet = json_response.stream[tweet_id];
        console.log(tweet);
        if (tweet && tweet.text && tweet.sentiment) {
            add_tweet_to_ui(tweet);
            summary[tweet.sentiment.toLowerCase()]++;
        }
    };

    let json_response = await response.json();
    // console.log(json_response.stream);
    let new_tweet_ids = Object.keys(json_response.stream);

    new_tweet_ids.forEach(add_tweet);

    generate_overall_sentiment_result(document.querySelector("#insert-chart"), summary)

    // console.log(json_response);
}
