var categories = ['stream', 'sentiment']
var ids = []
// listen to button click and send value to api

stream_active = false;
fetch_every_second = null;

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

    tweet_as_link.innerHTML = tweet;

    const list = document.querySelector('#tweets');
    list.appendChild(tweet_as_link);
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
        tweet = json_response.stream[tweet_id]?.text;
        console.log("Tweet Id: " + tweet_id);
        console.log("Object: ");
        console.log("ID:");
        console.log(ids);
        console.log(json_response.stream);
        if (tweet != undefined) {
            add_tweet_to_ui(tweet);
        }
    };

    let json_response = await response.json();
    // console.log(json_response.stream);
    let new_tweet_ids = Object.keys(json_response.stream);

    new_tweet_ids.forEach(add_tweet);



    // console.log(json_response);
}