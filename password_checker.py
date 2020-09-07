import requests
import hashlib
import sys

#API url


def request_api_data(query_char):
	
	url = 'https://api.pwnedpasswords.com/range/' + query_char 
	response = requests.get(url)
	if response.status_code != 200:
		raise RuntimeError(f'Error fetching {response.status_code}, check the API and Try Agian')

	return response

def get_password_leaks_count(hashes, hashes_to_check):
    hashes = (line.split(':') for line in hashes.text.splitlines())
    for h, count in hashes:
        if h == hashes_to_check:
            return count
    return 0


def pawned_api_check(password):
    sha1password = hashlib.sha1(password.encode('utf-8')).hexdigest().upper() #hexdigest give double string of hexadecimal number
    firts5_char, tail = sha1password[:5], sha1password[5:]
    response = request_api_data(firts5_char)
    
    return get_password_leaks_count(response, tail) 




def main(args):

    with open(args, 'r+') as file:
        for password_in_line in file.readlines():
            password_in_line = password_in_line.strip()
            count = pawned_api_check(password_in_line)
            if count:
                print(f'This {password_in_line} Password Has ben Compromised {count} Times')
            else:
                print(f'{password_in_line} Password was not Compromised')
    
    return "Done!"

if __name__ == '__main__' :
    sys.exit(main(sys.argv[1]))