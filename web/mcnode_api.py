import requests
import ssl

mcnode_url = "https://dev.medcrypt.com:3000/"

def post_login_message(user_email):
    r = requests.get(mcnode_url + "log_user_authentication?format=json&user_email=" + user_email,verify=False)
    return r

def permissions_check(user_email,mcaction_id):
    r = requests.get(mcnode_url + "permissions_check?format=json&user_email=" + user_email + "&mcaction_id=" + mcaction_id,verify=False)
    print "Permissions Check | User email: " + user_email + " , Mcaction_id: " + mcaction_id + " , result: " + r.content
    if r.content == "true": #should change case of true here to True
        return True
    else:
        return False

def create_signature(user_email,mcaction_id):
    r = requests.get(mcnode_url + "create_signature?format=json&user_email=" + user_email + "&mcaction_id=" + mcaction_id,verify=False)
