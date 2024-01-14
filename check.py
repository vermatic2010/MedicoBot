import requests

url = "https://nutrition-by-api-ninjas.p.rapidapi.com/v1/nutrition"

querystring = {"query":"tomato"}

headers = {
	"X-RapidAPI-Key": "9f18e8c471mshc6126d1eefc68dcp1a5af0jsnbb9f33043ee4",
	"X-RapidAPI-Host": "nutrition-by-api-ninjas.p.rapidapi.com"
}

response = requests.get(url, headers=headers, params=querystring)

print(response.json())