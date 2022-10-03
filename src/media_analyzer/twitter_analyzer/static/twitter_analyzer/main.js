console.log("loaded")
// Send a button's value to the API when clicked
$("button").click(async function() {
    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    
    //raw button value from its html 'value' property
    let button_value = $(this).val();

    //split the buttton value by its spacing (such as "stream 1" to [stream, 1])
    button_value_as_arr = value.split(" ");

    //the first element of the value property- its name
    button_value_name = button_value_as_arr[0];

    //the second element of the value property- the value
    button_value_integer = parseInt(button_value_as_arr[1]);

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
    });
});