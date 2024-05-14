import http from 'k6/http';
import { check } from 'k6';
import { randomIntBetween } from 'https://jslib.k6.io/k6-utils/1.1.0/index.js';

export let options = {
    scenarios: {
        ramping_test: {
            executor: 'ramping-arrival-rate',
            startRate: 10, // start at 10 RPS
            timeUnit: '1s',
            preAllocatedVUs: 100, // number of VUs to pre-allocate
            maxVUs: 100, // maximum number of VUs that can be allocated during the test
            stages: [
                { target: 30, duration: '30s' }, // ramp to 100 RPS over 2 minutes
            ],
        },
    },
};

export default function () {
    let url = 'https://mainserver-fdhzgisj6a-de.a.run.app/api/v1/restaurants';

    const res = http.get(url);
    
    check(res, {
        'is status 200': (r) => r.status === 200,
    });
}