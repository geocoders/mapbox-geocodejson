# Mapbox geocoding results in geocodejson format

A very dumb proxy to run queries against mapbox geocoding API, and make Carmen geojson result compatible with [geocodejson](https://github.com/geocoders/geocodejson-spec).

## Intalling

Python3 is needed.
To install the requirements :

    pipenv install --three

Then duplicate the default_params folder and rename to params :

    cp -R default_params/ params/

Put your mapbox api key in the `params/__init__.py`

## Running

    python api.py

Then, you can geocode some stuff :

        curl 'http://localhost:5000/?q=rue%20de%20la%20procession'

Or use [geocoder-tester](https://github.com/geocoders/geocoder-tester) :

        py.test --api-url http://localhost:5000/ --max-run 10
