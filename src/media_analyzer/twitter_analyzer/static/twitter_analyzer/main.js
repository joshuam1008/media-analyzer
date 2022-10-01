console.log("loaded")
// listen to button click and send value to api
$("button").click(async function() {
    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    let value = $(this).val();
    value = value.split(" ")
    value[1] = parseInt(value[1])
    const response = await fetch('/twitter/toggle_modules', {
        method: 'POST',
        body: JSON.stringify({
            name: value[0],
            state: value[1]
        }),
        headers: {
            'Accept': 'application/json, text/plain, */*',
            'Content-Type': 'application/json',
            "X-CSRFToken": csrftoken
        }
    })
    // alert(`module is ${value[0]} value is ${value[1]}.`);
});