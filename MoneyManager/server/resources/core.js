log = {
    debug: (msg) => {
        console.log(`DEBUG|${(new Date()).toLocaleTimeString()}|${msg}`);
    }
}

async function send_get_request(route, params) {
    try {
        route_with_params = route;
        if (params) {
            let addres_params = '?'
            for (const key in params) {
                if (params.hasOwnProperty(key)) {
                    addres_params += `${key}=${params[key]}`;
                }
            }

            route_with_params += addres_params
        }

        log.debug(`Sending GET request to localhost:4433/api/${route_with_params}`);
        const response = await fetch(`http://localhost:4433/api/${route_with_params}`, {
            method: 'GET',
            // mode: 'cors',
            headers: {'Accept': 'application/json', 'Content-Type': 'application/json'}
        });
        json_response = await response.json()
        if (json_response.error) {
            throw json_response.error;
        }
        return json_response.response;
    } catch(err) {
        alert(`Error during request to server: ${err}`);
        throw err;
    }
}

async function send_post_request(route, params) {
    try {
        let data = {};
        for (const key in params) {
            if (params.hasOwnProperty(key)) {
                data[key] = params[key];
            }
        }

        const request_body = JSON.stringify(data);

        log.debug(`Sending POST request to localhost:4433/api/${route} with data ${request_body}`);
        const response = await fetch(`http://localhost:4433/api/${route}`, {
            method: 'POST',
            // mode: 'cors',
            headers: {'Accept': 'application/json', 'Content-Type': 'application/json'},
            body: request_body
        });
        json_response = await response.json()
        if (json_response.error) {
            throw json_response.error;
        }
        return json_response.response;
    } catch(err) {
        alert(`Error during request to server: ${err}`);
        throw err;
    }
}
