#pip install requests
#https://haveibeenpwned.com/
#this api uses 'k-anonymity' so we only pass in first 5 digits of our password
#See https://en.wikipedia.org/wiki/K-anonymity

#https://docs.python.org/3/library/hashlib.html


# str2hash = "12345"
# result = hashlib.md5(str2hash.encode())
# print(result.hexdigest())

import requests, hashlib,sys

def send_request(query):    #send first 5 chars to the API and return response
    res = requests.get('https://api.pwnedpasswords.com/range/' + query)
    if res.status_code != 200:
        RuntimeError('Erro occured..please try again')
    return res.text

#Get all hashes matches,loop thrugh them and compare each with our tail
def get_password_leaks(hashes, hash_to_check):   #get number of password leaks
    hashes = (line.split(':') for line in hashes.splitlines())
    for h,count in hashes:
        if h == hash_to_check:
            return count
    return 0


def hash_password(query):
    password = hashlib.sha1(query.encode()).hexdigest().upper()
    first5_chars,tail = password[:5], password[5:]
    response = send_request(first5_chars)
    return get_password_leaks(response, tail)

# hash_password('password')
def main(args):
    # if isinstance(args, list):
    for password in args:
        count= hash_password(password)
        if count:
            print(password + ' was found '+ count + ' times')
        else:
            print('No matches found for: ' + password)
    return 'Done!!'

array_of_passwords = ['Father','hello','wserfwew','password','Oops']

if __name__ == '__main__':
    main(array_of_passwords)