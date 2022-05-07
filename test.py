from requests import get, delete, post

address = '127.0.0.1:8080'

# Get all
print(get(f'http://{address}/api/v2/jobs').json())

# Get one
print(get(f'http://{address}/api/v2/jobs/1').json())

# Get wrong one
print(get(f'http://{address}/api/v2/jobs/999').json())

# Delete first job
print(delete(f'http://{address}/api/v2/jobs/1').json())
# Get all
print(get(f'http://{address}/api/v2/jobs').json())

# Delete wrong job
print(delete(f'http://{address}/api/v2/jobs/999').json())
# Get all
print(get(f'http://{address}/api/v2/jobs').json())

# Add correct job
print(post(f'http://{address}/api/v2/jobs', json={
    'id': 5,
    'team_leader': 1,
    'job': 'Building',
    'work_size': 20,
    'collaborators': '1, 2, 3',
    'is_finished': False,
}).json())
# Get all
print(get(f'http://{address}/api/v2/jobs').json())

# Add wrong job
print(post(f'http://{address}/api/v2/jobs', json={
    'id': '999',
    'team_leader': '999'
}).json())
# Get all
print(get(f'http://{address}/api/v2/users').json())