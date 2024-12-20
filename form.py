from bs4 import BeautifulSoup

def extract(config):
    with (open(config, "r") as configData) :
        file = configData.read()
        soup = BeautifulSoup(file, 'html.parser')
        username = soup.find('input', {'type': 'text'})['name']
        password = soup.find('input', {'type': 'password'})['name']
        submit = soup.find('input', {'type': 'submit'})['name']
        data = {
            username:"",
            password : '',
            submit:''
        }

        return data

print(extract("config.txt"))

