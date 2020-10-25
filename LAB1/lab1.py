import requests 

NUME = "Minea Alexandra"
GRUPA = "342C3"

PROOF_FILE = 'proof.txt'

def get_proof(response):
    return response.json()['proof']

def task1():
    URL = "https://sprc.dfilip.xyz/lab1/task1/check"

    params = f"nume={NUME}&grupa={GRUPA}"
    data = {"secret": "SPRCisNice",}
    header = {"secret2": "SPRCisBest",}

    r = requests.post(URL, data=data, params=params, headers=header) 
    
    #print(r.text)
    print("proof TASK1")
    proof = get_proof(r)
    print(proof)

    f = open(PROOF_FILE, "w")
    f.write(f"proof TASK1\n{proof}\n")
    f.close()

def task2():
    URL = "https://sprc.dfilip.xyz/lab1/task2"

    json = {"username": "sprc", 'password': 'admin', 'nume' : NUME}
    r = requests.post(URL, json=json)
    
    print("proof TASK2")
    proof = get_proof(r)
    print(proof)

    f = open(PROOF_FILE, "a")
    f.write(f"proof TASK2\n{proof}\n")
    f.close()

def task3():
    URL_POST = "https://sprc.dfilip.xyz/lab1/task3/login"
    s = requests.Session()
    json = {"username": "sprc", 'password': 'admin', 'nume' : NUME}
    r = s.post(URL_POST, json=json)
    print(r.text)

    URL_GET = "https://sprc.dfilip.xyz/lab1/task3/check"
    r = s.get(URL_GET)
    print("proof TASK3")
    proof = get_proof(r)
    print(proof)

    f = open(PROOF_FILE, "a")
    f.write(f"proof TASK3\n{proof}\n")
    f.close()


task1()
task2()
task3()