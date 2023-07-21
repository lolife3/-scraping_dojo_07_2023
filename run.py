from bs4 import BeautifulSoup
import requests
import chompjs
import json


class Scrapper():
    def __init__(self, url):
        self.response = requests.get(url)
        self.soup = BeautifulSoup(self.response.text, "html.parser")
        self.data = self.soup.find_all("script")[1]
    
    
    def parse_data(self):
        parsed_data = self.data.get_text().split("var data = [")[1].split("];")[0].strip()
        self.data = list(chompjs.parse_js_objects(parsed_data))
        return self.data
    
    
    def save(self, entry):
        with open("output.jsonl", "a", encoding='utf8') as file:
            json.dump(entry, file, indent=2, ensure_ascii=False)
              
        
if __name__ == "__main__":
    try:
        list_of_entries = []
        for page in range(1,11):    
            scrapper_object = Scrapper(f"http://quotes.toscrape.com/js-delayed/page/{page}/")
            scrapper_object.parse_data()
            
            for entry in scrapper_object.data:
                list_of_entries.append({
                    "text": entry["text"],
                    "by": entry["author"]["name"],
                    "tags": entry["tags"]
                    })
        scrapper_object.save(list_of_entries)
    except:
        print("program terminated")