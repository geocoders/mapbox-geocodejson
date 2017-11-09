# encoding: utf-8

from flask import Flask
from flask_restful import Resource, Api, reqparse
import requests
from params import mapbox_API_key as TOKEN
from params import mapbox_base_url as BASE

app = Flask(__name__)
api = Api(app)

mapbox_API_key = TOKEN
mapbox_base_url = BASE

class CarmenAutocomplete(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('q', type=str, help='the q you are you looking for', required=True)
        parser.add_argument('limit', type=int) #not available in the api ?
        args = parser.parse_args()
        query = args['q']

        autocomplete_url = "{}/{}.json".format(mapbox_base_url, query)
        get_results = requests.get(autocomplete_url, params = {'access_token' : mapbox_API_key})

        if not "features" in get_results.json() :
            return {"type": "FeatureCollection", "features":[], "error":"no results"}

        carmen_results = get_results.json()['features']
        geocodejson_results = []

        for a_feature in carmen_results :
            a_feature['properties']['type'] = a_feature['place_type'][0]
            a_feature['properties']['id'] = a_feature['id']
            a_feature['properties']['score'] = a_feature['relevance']
            a_feature['properties']["name"] = a_feature['text']
            a_feature['properties']["label"] = a_feature['place_name']
            if "context" in a_feature and len(a_feature["context"]) > 2:
                a_feature['properties']["city"] = a_feature['context'][1]['text']
                a_feature['properties']["postcode"] = a_feature['context'][0]['text']
                a_feature['properties']["country"] = a_feature['context'][2]['text']

            if "address" in a_feature:
                a_feature['properties']["housenumber"] = a_feature['address']
                a_feature['properties']["street"] = a_feature['text']
                a_feature['properties']['type'] = "housenumber"
                a_feature['properties']["name"] = "{} {}".format(a_feature['properties']["housenumber"], a_feature["text"])

            geocodejson_results.append(a_feature)

        geocoder_json = {
            "type" : "FeatureCollection",
            "query" : get_results.json()['query'],
            "features" : geocodejson_results,
        }

        return geocoder_json

api.add_resource(CarmenAutocomplete, '/')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
