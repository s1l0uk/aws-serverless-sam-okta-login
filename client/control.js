var accessToken = null;

var signIn = new OktaSignIn({
    baseUrl: 'http://{yourOktaDomain}',
    clientId: '{yourClientId}',
    redirectUri: window.location.origin,
    authParams: {
        issuer: 'https://{yourOktaDomain}/oauth2/default',
        responseType: ['token', 'id_token']
    }
});

signIn.renderEl({
    el: '#widget-container'
}, function success(res) {
    if (res.status === 'SUCCESS') {
        accessToken = res.tokens.accessToken.accessToken;
        signIn.hide();
    } else {
        alert('fail);')
    }
}, function(error) {
    alert('error ' + error);
});

function onmessage() {
    const url = "http://localhost:3000/api/messages";
    var headers = {}
    if (accessToken != null) {
        document.getElementById('token').value = accessToken;
    }
    fetch(url, {
        method : "POST",
        mode: 'cors',
        body: new URLSearchParams(new FormData(document.getElementById("messageForm"))),
    })
    .then((response) => {
        if (!response.ok) {
            throw new Error(response.error)
        }
        return response.text();
    })
    .then(data => {
        messages = JSON.parse(data)
        document.getElementById('messages').value = messages.join('\n');
    })
    .catch(function(error) {
        document.getElementById('messages').value = error;
    });
}
