import json
from pathlib import Path

from functions import get_response_GPT, get_prompts_GPT
from config import PROMPTS_DIR, SEO_CITY_DESCRIPTIONS_DIR, SEO_CITY_ATTRACTIONS_DIR


def recursive_replace(d, old_str, new_str):
    for k, v in d.items():
        if isinstance(v, dict):
            recursive_replace(v, old_str, new_str)
        if isinstance(v, str):
            d[k] = v.replace(old_str, new_str)
    return d


def get_seo_text(city: str, attractions: list[str]) -> None:
    
    prompt = recursive_replace(get_prompts_GPT(PROMPTS_DIR/'city_attractions_pmt.json'), '[city]', city)
    
    data = dict()
    for attraction in attractions:
        prompt_i = prompt['attraction']
        prompt_i = prompt_i.replace('[attraction]', attraction)
        response = get_response_GPT(prompt_i)
        response = response.strip(' ').strip('\"')
        response = response.replace('Title: ', '').replace('\n\n', '\n')
        data[attraction] = response

    # write result in json
    SEO_CITY_ATTRACTIONS_DIR.mkdir(parents=True, exist_ok=True)  
    with open(f'{SEO_CITY_ATTRACTIONS_DIR}/{city}.json', 'w') as file:
        json.dump(data, file, indent=4)
    
    
def get_seo():
    files = Path(SEO_CITY_DESCRIPTIONS_DIR).glob('*.json')
    for i, file in enumerate(files, start=1):
        city = file.name.partition('.')[0]
        with open(file, 'r') as json_file:
            attractions = json.load(json_file)['lists']['attractions']
        print(f'\nProcessing: {i}. {city}')
        get_seo_text(city, attractions) 
        print('...successfully!')
        
    
if __name__ == '__main__':
    get_seo()