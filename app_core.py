import re, os, sys
import time
import random


from database import load_db, save_db

# Note : add uniqe email checker in registiration
# Note : check valid date 

users = load_db('users.json')
projects = load_db('projects.json')

def id_gen():
    current_time = int(time.time())
    random_number = random.randint(0, 9999)
    
    return f"{current_time}{random_number}"


def registration_temp():
    user_data = {"email":'',"fname":'', "lname":'', "password":'',"confirm_pass":'', "mobile":''}
    user_data['fname'] = input('\tFirst Name : ').lower().strip()
    user_data['lname'] = input('\tLast Name : ').lower().strip()

    user_data['email'] = input('\tEmail : ')

    user_data['password'] = input('\tPassword : ').strip()
    user_data['confirm_pass'] = input('\tConfirm-Password : ').strip()
    user_data['mobile'] = input('\tMobile : (+20) ').strip()

    return user_data


def project_temp():
    user_fund = {"title":"", "details":"", "target":"", "start":"", "end":""}

    user_fund['title'] = input('\tTitle : ').title().strip()
    user_fund['details'] = input('\tDetails : ').lower().strip()
    user_fund['target'] = input('\tTotal Target : ').lower().strip()
    user_fund['start'] = input('\tStart Date dd-mm-yyyy : ').lower().strip()
    user_fund['end'] = input('\tEnd Date dd-mm-yyyy : ').lower().strip()

    return user_fund

    
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

    elif check == 'username' :
        if not input_from_user.isalpha() :
            return False
        return True

    elif check == 'string' :
        return all(i.isalpha() or i.isspace() for i in input_from_user)


    matched = re.search(pattern,input_from_user)
    if matched :
        return True
    return False


def check_password(pass_from_db, pass_from_user):

    if pass_from_db != pass_from_user:
        return False
    return True


def check_project_info(check_project) :

    if  not check_valid(check_project['title'], 'string') :
        return 'Title must be alphabets only.'
    
    if not check_project['target'].isdigit():
        return 'Total target must be digits only.'
    
    if  not check_valid(check_project['start'], 'date') or \
        not check_valid(check_project['end'], 'date') :
        return 'Incorrect date formula.'


@safe_exit
def registration(user_data, conf_pass):

    global users, projects

    if  not check_valid(user_data['fname'], 'username') or \
        not check_valid(user_data['lname'], 'username'):
        print("Invalid Name.")

    elif not check_valid(user_data['email'], 'email'):
        print("Invalid Email.")

    elif user_data['password'] != conf_pass:
        print("Passwords do not match.")

    elif not check_valid(user_data['mobile'], 'mobile') :
        print("Invalid mobile phone number.")

    else:
        print("\nRegistration successful!")
        user_data.pop('confirm_pass')
        users.update({user_data['email']:user_data})
        projects.update({user_data['email']:{}})
        save_db(users, 'users.json')


#need test ( not working in view_db() )
def check_projects_db(user_email):
    global projects
    if not user_email in projects :
        projects.update({user_email:{}})


def create_fund(user_email, project_info):
    global projects

    check_projects_db(user_email)

    user_fund = project_info
    check_project_info(user_fund)

    user_project = projects[user_email]
    user_project[id_gen()] = user_fund
    save_db(projects, 'projects.json')


def edit_delete(user_email, func, project_id):
    
    global projects

    check_projects_db(user_email)

    user_projects = projects[user_email]

    if project_id in user_projects :

        if func == 'delete' :
            user_projects.pop(project_id)
            save_db(projects, 'projects.json')
            return
       
        elif func == 'edit' :
            fund_update = project_temp()

            for key, value in fund_update.items() :
                if not value :
                    fund_update[key] = user_projects[project_id][key]

            edit_check = check_project_info(fund_update)
            if edit_check :
                return f'\n(EDIT) {edit_check}'

            user_projects[project_id].update(fund_update)
            save_db(projects, 'projects.json')

    else :
        return "Permission Denied"
    
    
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
        

def login(debug=False):
    if debug :
        debugger = ('user@debug.com', 'debug')
        return debugger

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

