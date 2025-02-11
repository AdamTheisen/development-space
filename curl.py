import requests

url = 'https://adc.arm.gov/elastic/metadata/_search'
headers = {
  "Content-Type": "application/json",
}
payload = {
  "aggs": {
    "distinct_site_code": {
      "terms": {
        "field": "site_code.keyword",
        "order": {
          "_key": "asc"
        },
        "size": 7000
      },
      "aggs": {
        "hits": {
          "top_hits": {
            "_source": [
              "site_type",
              "location",
              "site_code",
              "facility_code",
              "start_date",
              "end_date",
              "ffac",
              "site_name",
              "facility_name"
            ],
            "size": 1
          }
        }
      }
    }
  },
  "size": 0,
  "query": {
    "query_string": {
      "query": "site_type:* AND ffac:* AND location:*"
    }
  }
}

response = requests.request("POST", url, headers=headers, data=payload)
print(response.text)
