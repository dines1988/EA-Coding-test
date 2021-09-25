import json
import arrow
import requests
from jsonschema import validate
from jsonschema import Draft6Validator
from header_validator import HeadersValidator

endpoint = "https://eacp.energyaustralia.com.au/codingtest/api/v1/festivals"

with open('schema.json') as f:
          schema = json.load(f)

class TestIntegration(HeadersValidator):
     def test_get_band_details_response_200(self):
          response = requests.get(endpoint)
          assert response.status_code == 200 or response.status_code == 429
          print(response)

     def test_get_band_details_response_header(self):
          response = requests.get(endpoint)
          assert response.status_code == 200 or response.status_code == 429

          if(response.status_code == 200 and len(str(response.text))>10 ):
               assert response.headers["Content-Type"] == "application/json; charset=utf-8"
               assert len(str(response.headers["vary"])) >= 1
               super().check_header(response)

          else:
               if(response.status_code == 429):
                    assert response.text == "Too many requests, throttling"
                    assert response.headers["Content-Type"] == "text/html; charset=utf-8"
                    super().check_header(response)
               assert response.headers["Content-Type"] == "application/json; charset=utf-8"
               super().check_header(response)
          print(response.headers)

     def test_get_band_details_schema(self):
          response = requests.get(endpoint)   

          # Validate schema structure
          assert response.status_code == 200 
          resp_body = response.json()

          # Validate will raise exception if given json is not what is described in schema.
          validate(instance=resp_body, schema=schema)
          print(resp_body)
     
     def test_get_band_details_data(self):
          response = requests.get(endpoint)   

          # Validate missing data
          assert response.status_code == 200 
          resp_body = response.json()
          print(len(resp_body))

          if(len(resp_body) > 1):
               print(json.dumps(resp_body[0]))
               total_num_records = len(resp_body)
               for i in range(total_num_records):
                    band_data = json.dumps(resp_body[i])
                    band_data = json.loads(band_data) 
                    assert len(str(band_data.get("name")))>1
                    print("++++++++++++++++++++++++++++++")
                    num_of_records = len(band_data['bands'])
                    band_data = band_data['bands']

                    for i in range(num_of_records):
                         current_record = json.dumps(band_data[i])
                         current_record = json.loads(current_record)

                         try:
                              if(len(current_record.get('name'))>1 and len(current_record.get('recordLabel'))>1):
                                   assert True
                              else:
                                   print("The following record name or lable is blank...")
                                   print("===============================================")
                                   print("Record name:" + current_record.get('name'))
                                   print("Record label:" + current_record.get('recordLabel'))
                                   assert False
                         except TypeError:
                                   print("One of the attribute record name or label is missing...")
          else:
               print("No data in the response body...")
               assert False
               

          

               

