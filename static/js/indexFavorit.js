async function makeRequest(url, method = 'GET') {
    let response = await fetch(url, {method});

    if (response.ok) {
        return await response.json();
    } else {
        let error = new Error(response.statusText);
        error.response = response;
        throw error;
    }
}
async function buttonOnClick(event) {
    event.preventDefault();
    let target = event.target
    let url = target.dataset.new
    let response = await makeRequest(url)
    if (response.user === true) {
        target.innerText = "Удалить из избранного"
    } else {
        target.innerText = "Добавить в избранные"
    }
}


function getButtons() {
    let buttons = document.getElementsByClassName('news')
    for (button of buttons) {
        button.addEventListener('click', buttonOnClick)
    }
}

window.addEventListener('load', getButtons)