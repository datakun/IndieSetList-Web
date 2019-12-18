function start() {
    gapi.client.init({
        'apiKey': '',
        'discoveryDocs': ['https://people.googleapis.com/$discovery/rest'],
        'clientId': '',
        'scope': 'profile',
    }).then(function () {
        return gapi.client.people.people.get({
            'resourceName': 'people/me',
            'requestMask.includeField': 'person.names'
        });
    }).then(function (response) {
        console.log(response.result);
    }, function (reason) {
    });
};
gapi.load('client', start);