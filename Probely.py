import subprocess
import json

auth = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0ZW5hbnQiOiJwcm9iZWx5IiwidXNlcm5hbWUiOiJZVWt3WjhHZFhpUmkiLCJqdGkiOiJRRDdoWUFvdjdTYnIifQ.O53R154sjyE0I5iv_ykFkboz7i5qeQwRRk-Kve9hjIs'

def my_post(target):
    result = subprocess.Popen(f'curl https://api.probely.com/targets/{target}/scan_now/ -X POST -H "Authorization: JWT {auth}' , shell=True, stdout=subprocess.PIPE)
    result.wait()
    data, err = result.communicate()
    result = json.loads(str(data.decode('utf-8')))
    my_id=result.get('id')
    if my_id:
        return  result['id']
    raise Exception("not found")


def my_get(target ,my_id):
    result = subprocess.Popen(f'curl https://api.probely.com/targets/{target}/scans/{my_id}/ -X GET -H "Authorization: JWT {auth}', shell=True, stdout=subprocess.PIPE)
    result.wait()
    data, err = result.communicate()
    result = json.loads(str(data.decode('utf-8')))
    print(my_id, ',Low: ',result['lows'], ', Medium: ' , result['mediums'], ', High: ',result['highs'], ',total: ', (int(result['lows'])*1)+ (int(result['mediums'])*10)+ (int(result['highs'])*40))
    return{"ID": my_id, "Low":result['lows'], "Medium": result['mediums'], "High":result['highs'], "total": (int(result['lows'])*1)+ (int(result['mediums'])*10)+ (int(result['highs'])*40)}


def my_compare(result1, result2):
    severity=["low", "medium", "high"]
    z=0
    find = []
    find.append(int(result1["Low"])-int(result2["Low"]))
    find.append(int(result1["Medium"])-int(result2["Medium"]))
    find.append(int(result1["High"])-int(result2["High"]))
    
    for x in find:
        if x>0:
            print(f'{result1["ID"]} have {abs(x)} more {severity[z]} that {result2["ID"]}')
        elif x==0:
            print(f'{result1["ID"]} have the same number of {result2["ID"]}')
        else:
            print(f'{result2["ID"]} have {abs(x)} more {severity[z]} that {result1["ID"]}')
        z=z+1


if __name__ == '__main__':
    target='RzXFSNHH3qUY'

    my_id=my_post(target)
    my_get(target, my_id)

    result1 = my_get(target, '3hbQvcGEmLbW')    
    result2 = my_get(target, '2RnxpEEm2qd5')
    my_compare(result1, result2)