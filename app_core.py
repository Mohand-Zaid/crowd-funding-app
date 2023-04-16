import re, os, sys

from database import load_db, save_db

# Note : add uniqe email checker in registiration
# Note : check valid date 
# Note : check validation of new data (edit)

users = load_db('users.json')
projects = load_db('projects.json')


start_id = 100
def id_gen():
    global start_id
    start_id += 1
    return str(start_id)

    
def safe_exit(fun):
    def sub_try(arg1=None, arg2=None):
        try :
            fun(arg1, arg2)
        except KeyboardInterrupt :
            print()
        except EOFError :
            print()
    return sub_try


def check_valid(input_from_user, check):

    if not check :
        return 'Check label not detected.'
    elif check == 'email' :
        pattern = r'^[\w\d\._-]+@[\w\d\.-]+\.[\w]{2,}$'
    elif check == 'mobile' :
        pattern = r'^(10|11|12|15)\d{8}$'

    elif check == 'date' :
        pattern = r'\d{1,2}-\d{1,2}-\d{4}'
    
    elif check == 'string' :
        if not input_from_user.isalpha():
            return False
        return True

    matched = re.search(pattern,input_from_user)
    if matched :
        return True
    return False


def check_password(pass_from_db, pass_from_user):

    if pass_from_db != pass_from_user:
        return False
    return True


@safe_exit
def registration(arg1=None, arg2=None):

    global users, projects

    print('\nCrowd-Funding Registration\n')

    user_data = {"fname":'', "lname":'', "password":'', "mobile":''}
    user_data['fname'] = input('\tFirst Name : ').lower().strip()
    user_data['lname'] = input('\tLast Name : ').lower().strip()

    email = input('\tEmail : ')

    user_data['password'] = input('\tPassword : ').strip()
    confirm_pass = input('\tConfirm-Password : ').strip()
    user_data['mobile'] = input('\tMobile : (+20) ').strip()

    if  not check_valid(user_data['fname'], 'string') or \
        not check_valid(user_data['lname'], 'string'):
        print("Invalid Name.")

    if not check_valid(email, 'email'):
        print("Invalid Email.")

    if user_data['password'] != confirm_pass:
        print("Passwords do not match.")

    if not check_valid(user_data['mobile'], 'mobile') :
        print("Invalid mobile phone number.")

    else:
        print("\nRegistration successful!")
        users.update({email:user_data})
        projects.update({email:{}})
        save_db(users, 'users.json')


#need test ( not working in view_db() )
def check_projects_db(user_email):
    global projects
    if not user_email in projects :
        projects.update({user_email:{}})


def projects_ds():
    user_fund = {"title":"", "details":"", "target":"", "start":"", "end":""}

    user_fund['title'] = input('\tTitle : ').title().strip()
    user_fund['details'] = input('\tDetails : ').lower().strip()
    user_fund['target'] = input('\tTotal Target : ').lower().strip()
    user_fund['start'] = input('\tStart Date dd-mm-yyyy : ').lower().strip()
    user_fund['end'] = input('\tEnd Date dd-mm-yyyy : ').lower().strip()

    return user_fund


def create_fund(user_email):
    global projects

    check_projects_db(user_email)

    user_fund = projects_ds()

    if  not check_valid(user_fund['title'], 'string') or \
        not check_valid(user_fund['details'], 'string') :
        print('Title and Details must be alphabits only.')

    if not user_fund['target'].isdigit():
        print('Enter Total Target In Digits.')
    
    if  not check_valid(user_fund['start'], 'date') or \
        not check_valid(user_fund['end'], 'date') :
        print('Incorrect date formula.')

    else :
        user_project = projects[user_email]
        user_project[id_gen()] = user_fund
        save_db(projects, 'projects.json')


# Note : check validation of new data
def edit_delete(user_email, func):
    
    global projects

    check_projects_db(user_email)

    project_id = input(f"({func.upper()}) Project ID : ").strip().lower()
    user_project = projects[user_email]

    if project_id in user_project :

        if func == 'delete' :
            user_project.pop(project_id)
            save_db(projects, 'projects.json')
       
        elif func == 'edit' :
            fund_update = projects_ds()

            for key, value in fund_update.items() :
                if value :
                    user_project[project_id].update({key:value})
                    save_db(projects, 'projects.json')

    else :
        print('Permission Denied')
    
    
def format_project_details(project_details):
    print(f"Title: {project_details['title']}")
    print(f"Details: {project_details['details']}")
    print(f"Total target: {project_details['target']}")
    print(f"Start time: {project_details['start']}")
    print(f"End time: {project_details['end']}")


def view_db(email, db):
    check_projects_db(email) #need test

    if email in db :

        for user_email, details in db.items():
            print(f"\nEmail: {user_email}")
            print('-'*20)
            for project_id, project_details in details.items():
                print(f"\nProject ID: {project_id}")
                format_project_details(project_details)
    else :
        for project_id, project_details in db.items():
                print(f"\nProject ID: {project_id}")
                format_project_details(project_details)
        

def login():
    email = input("Enter your email: ").lower().strip()
    password = input("Enter your password: ").strip()

    if email in users :
        user = users[email]

        if password == user['password'] :
            print("\nLogin successful!\n")
            user = (email, user['fname'])
            return user
        else:
            print("Invalid password!")
            return False

    print("Email not registered!")
    return False


def search(srch_date) :

    found_projects = []

    for user, pro in projects.items():
        for project_id, details in pro.items():
            if srch_date == details['start']:
                found_projects.append((users[user]['fname'],users[user]['lname'], project_id))

    return found_projects


def restart():
    
    print("\nRestarting the application ...\n")
    app = sys.executable
    os.execl(app, app, *sys.argv)

