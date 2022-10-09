var summary = {}
var selected_words = []
var selected_langs = []
//Language name from ISO 639-1 code
var languageNames = new Intl.DisplayNames(['en'], { type: 'language' });
var lang_tag_list = []
//modified upon button click
var categories = {
    'stream': false,
    'sentiment': false,
    'lang': false
}
//missing data by category
var missing_categories = {
    'stream': 0,
    'sentiment': 0,
    'lang': 0
}
//stream rate
var stream_rate = 0
//which overal reuslt to generate
var summary_category = null
//twitter with none filed
var ids = []
var total_tweet = 0
//all tweet recieved
all_tweets = {}
id = 0

langs = {
    "af": "Afrikaans",
    "ar": "Arabic",
    "bg": "Bulgarian",
    "bn": "Bengali",
    "ca": "Catalan",
    "cs": "Czech",
    "cy": "Welsh",
    "da": "Danish",
    "de": "German",
    "el": "Greek",
    "en": "English",
    "es": "Spanish",
    "et": "Estonian",
    "fa": "Persian",
    "fi": "Finnish",
    "fr": "French",
    "gu": "Gujarati",
    "he": "Hebrew",
    "hi": "Hindi",
    "hr": "Croatian",
    "hu": "Hungarian",
    "id": "Indonesian",
    "it": "Italian",
    "ja": "Japanese",
    "kn": "Kannada",
    "ko": "Korean",
    "lt": "Lithuanian",
    "lv": "Latvian",
    "mk": "Macedonian",
    "ml": "Malayalam",
    "mr": "Marathi",
    "ne": "Nepali",
    "nl": "Dutch",
    "no": "Norwegian",
    "pa": "Punjabi",
    "pl": "Polish",
    "pt": "Portuguese",
    "ro": "Romanian",
    "ru": "Russian",
    "sk": "Slovak",
    "sl": "Slovenian",
    "so": "Somali",
    "sq": "Albanian",
    "sv": "Swedish",
    "sw": "Swahili",
    "ta": "Tamil",
    "te": "Telugu",
    "th": "Thai",
    "tl": "Tagalog",
    "tr": "Turkish",
    "uk": "Ukrainian",
    "ur": "Urdu",
    "vi": "Vietnamese",
    "zh-cn": "Chinese (China)",
    "zh-tw ": "Chinese (Taiwan)"
}

//toggle result
$(".nav-link").click(function () {
    let text = $(this).text()
    let value = $(this).attr("value")
    //change text for buttom
    text = text.split(" ");
    if (text[0] == "Start") {
        text[0] = "Stop"
    } else if (text[0] == "Stop") {
        text[0] = "Start"
    }
    //toggle module
    if (value in categories) {
        categories[value] = !categories[value]
        $(this).html(text.join(" "))
    }
    console.log(categories)
})
//save the tweet locally and static
var save_tweets = function (json_response) {
    let stream = json_response.stream
    stream_rate = Object.keys(stream).length / 2
    let inds = json_response.inds
    for (data of [stream, inds]) {
        for (id of Object.keys(data)) {
            if (!(id in all_tweets)) {
                all_tweets[id] = {}
            }
            for (category of Object.keys(data[id]))
                if (category == 'lang') {
                    all_tweets[id][category] = langs[data[id][category]]
                }
                else {
                    all_tweets[id][category] = data[id][category]
                }
            //if result is none put twitter id into ids
            if (data[id][category] == null) {
                //do nothing for now
            }
        }
    }

}
//generate static of the stream
var get_static = function () {
    //update ui
    $("#rate").html(`Rate: ${stream_rate}/min`)
    $("#sentiment_count").html(`sentiment: ${missing_categories['sentiment']}`)
    $("#twitter_count").html(`Total: ${total_tweet}`)
}
//add tweet to ui
var add_tweet_to_ui = (tweet_id, tweet, position) => {
    const tweet_as_link = document.createElement("a");
    tweet_as_link.id = tweet_id
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

    position.appendChild(tweet_as_link);
    const list_2 = document.querySelector('#tweet_filtered');
    let tweet_passes_filter = false;

    // if no selected words but selected languages, only show tweets in selected languages
    if (selected_words.length == 0 && selected_langs.length > 0) {
        if (selected_langs.includes(langs[tweet.lang])) {
            tweet_passes_filter = true;
        }
    } else if (selected_words.length > 0 && selected_langs.length == 0) {
        // if no selected languages but selected words, only show tweets with selected words
        if (tweet.text.split(" ").some(word => selected_words.includes(word))) {
            tweet_passes_filter = true;
        }
    } else if (selected_words.length > 0 && selected_langs.length > 0) {
        // if both selected words and selected languages, only show tweets with selected words and selected languages
        if (tweet.text.split(" ").some(word => selected_words.includes(word))) {
            if (selected_langs.includes(langs[tweet.lang])) {
                tweet_passes_filter = true;
            }
        }
    }

    if (tweet_passes_filter) {
        list_2.appendChild(tweet_as_link);
    }

}

$("#clear-tweets").click(() => {
    var ids = [];
    var total_tweet = 0;
    all_tweets = {};
    id = 0;
    $('#tweet_stream').empty();
});

$("#clear-filtered").click(() => {
    $('#tweet_filtered').empty();
});

//note: chen's code I (David) adapted.
var plot_histo = function (position, overall_sentiment_results, title) {

    //convert dictionary to format of datatable
    var convert_dict_to_data_table = function (overal_sentiment_results) {
        let single_result = overall_sentiment_results
        let data = [
            ['Emo Level', 'Counts']
        ]
        for (let [category, value] of Object.entries(single_result)) {
            data.push([category, value])
        }
        return data
    }

    function plot_barchart(position, overall_sentiment_results) {
        function drawChart(tag_name, data) {
            let histogram_data = google.visualization.arrayToDataTable(data);

            let options = {
                title: title,
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
            () => {
                drawChart(position, convert_dict_to_data_table(overall_sentiment_results))
            });



    }
    plot_barchart(position, overall_sentiment_results)
}

var fetch_result = async function () {
    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    const keys = Object.keys(categories);
    const request_categories = keys.filter(function (key) {
        return categories[key]
    });
    const response = await fetch('/twitter/fetch_result', {
        method: 'POST',
        body: JSON.stringify({
            id: ids,
            category: request_categories
        }),
        headers: {
            'Accept': 'application/json, text/plain, */*',
            'Content-Type': 'application/json',
            "X-CSRFToken": csrftoken
        }
    });

    const add_tweet = (tweet_id) => {
        tweet = json_response.stream[tweet_id];
        let position = document.querySelector('#tweet_stream');
        if (tweet && tweet.text) {
            let add = true;
            for (category of Object.keys(categories)) {
                if (category != "stream" && categories[category] == true && !(tweet[category])) {
                    add = false;
                }
            }
            if (add) {
                add_tweet_to_ui(tweet_id, tweet, position);
            }
            // summary[tweet.sentiment.toLowerCase()]++;
        }
    };

    let json_response = await response.json();

    //save result
    save_tweets(json_response)
    let new_tweet_ids = Object.keys(json_response.stream);
    total_tweet += new_tweet_ids.length
    new_tweet_ids.forEach(add_tweet);
}
//add keyword or language label
var add_keyword = function () {
    let keyword = $("#input_keyword").val()
    $("#input_keyword").val("")
    if (keyword != "") {
        selected_words.push(keyword)
        $("#keywords").append(`<button type="button" class="btn btn-info btn-sm keyword" onclick="delete_keyword_lang(this)">${keyword}</button>`)
    }
}
var add_lang = function () {
    let lang = $("#lang_filter").val()
    if (lang != "") {
        selected_langs.push(lang)
        $("#langs").append(`<button type="button" class="btn btn-info btn-sm lang" onclick="delete_keyword_lang(this)">${lang}</button>`)
    }
}
//remove keyword or language label
var delete_keyword_lang = function (node) {
    const type = node.classList.contains('lang') ? 'lang' : 'keyword'
    const parent = node.parentNode
    parent.removeChild(node)
    const selected_list = type == 'lang' ? selected_langs : selected_words
    const index = selected_list.indexOf(node.textContent);
    if (index !== -1) {
        selected_list.splice(index, 1);
    }


    console.log(selected_words)
    console.log(selected_langs)
}

// add keyword
$("#submit_lang").click(function () {
    add_lang()
})
$("#submit_keyword").click(function () {
    add_keyword()
})
//select which summary to generate
$(".summary").click(function () {
    summary_category = $(this).val()
})
//generate plot based on summary_category
var generate_plot = function () {
    if (summary_category) {
        if (Object.keys(summary).length != 0) {
            const position = document.querySelector("#insert_chart")
            let title = null
            if (summary_category == 'sentiment') {
                title = "Sentiment Count"
                //plot sentiment
                plot_histo(position, summary, title)
            } else if (summary_category == 'lang') {
                title = "Language Count"
                lang_tag_list = Object.keys(summary)
                // console.log(lang_tag_list)
                //plot lang
                plot_histo(position, summary, title)
            }
            summary = {}
        }
        else {
            $("#insert_chart").html('<h5 class="text-center" >Waiting on data</h5>')
        }
    }
    else {
        $("#insert_chart").html('<h5 class="text-center" >Select a category first</h5>')
    }




}
//generate summary based on summary_category
//add id to ids if the category is missing
var generate_summary = function () {
    if (summary_category) {
        let missing_count = 0;
        for (id of Object.keys(all_tweets)) {
            const key = all_tweets[id][summary_category]
            if (key) {
                let current_value = summary[key] ?? 0
                summary[key] = current_value + 1
            } else {
                missing_count++;
                //TODO add to ids, but have to remove it when recieve 
                // ids.push(parseInt(id));
            }
        }
        missing_categories[summary_category] = missing_count;
    }
}

for (const [key, value] of Object.entries(langs)) {
    $("#lang_filter").append(`<option value="${value}">${value}</option>`)
}


setInterval(
    function () {
        //fetch result
        fetch_result();
        //get static 
        get_static();
        //generate summary of result
        generate_summary()
        //generate plot
        generate_plot()
        //update auto complete
        //$('#input_lang').autocomplete("option", { source: lang_tag_list });
    }, 2000
);