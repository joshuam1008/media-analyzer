
$( document ).ready(function() {
    alert("loaded")
    const csrftoken = Cookies.get('csrftoken')
  });
// listen to button click and send value to api
$("button").click(async function() {
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
            "X-CSRFToken": document.querySelector('[name=csrfmiddlewaretoken]').value
        }
    })
    // alert(`module is ${value[0]} value is ${value[1]}.`);
});