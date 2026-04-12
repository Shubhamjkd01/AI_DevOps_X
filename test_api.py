import requests
base = 'http://localhost:7860'
try:
    r1 = requests.post(base + '/reset')
    print('RESET:', r1.json())
    r2 = requests.get(base + '/tasks')
    print('TASKS:', r2.json())
    r3 = requests.post(base + '/step', json={'action_type': 'analyze', 'file_path': 'main.py', 'patch_content': ''})
    print('STEP:', r3.json())
    r4 = requests.get(base + '/state')
    print('STATE:', r4.json())
except Exception as e:
    print('ERROR:', str(e))
