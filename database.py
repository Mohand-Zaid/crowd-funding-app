import json


# Need test
def save_db(db_to_save, file_name):
    try:
        with open(f'db/{file_name}', 'w') as file:
            json.dump(db_to_save, file)
    except NameError :
        print(f'{file_name} : Can Not Save. Database Files Not Found')

def load_db(file_name):
    try:
        with open(f'db/{file_name}', 'r') as file:
            return json.load(file)
    except FileNotFoundError as e :
        print(f'load_db() : {e}\nrun "fixdb" command in main console')

