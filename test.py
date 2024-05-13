from main import *
import os

def Clear():
    if os.path.isfile('Fail.count') == True:
        os.remove('Fail.count')

def FailCounter():
    if os.path.isfile('Fail.count') == False:
        open('Fail.count', 'w').writelines(str(0))
    count = int(open('Fail.count', 'r').readline())
    count = count + 1
    open('Fail.count', 'w').writelines(str(count))
    return count

def Fail(reason):
    print(f'{FailCounter()} - FAIL: {reason}')


def Pass():
    print('PASS')


Clear()

try:
    rsp = Request_index.generate_id()
    if type(rsp) == str:
        if len(rsp) == 9:
            Pass()
        else:
            Fail('INCORRECT LEN')
    else:
        Fail('INCORRECT TYPE')
except Exception as e:
    Fail(e)

try:
    rsp = Request_index.new('TEST')
    if rsp == True:
        Pass()
    else:
        Fail('INCORRECT TYPE')
except Exception as e:
    Fail(e)

try:
    rsp = Request_index.get_id('TEST')
    if type(rsp) == str:
        if len(rsp) == 9:
            Pass()
        else:
            Fail('INCORRECT LEN')
    else:
        Fail('INCORRECT TYPE')
except Exception as e:
    Fail(e)

try:
    rsp = Request_index.get_last()
    if type(rsp) == str:
        if len(rsp) == 9:
            Pass()
        else:
            Fail('INCORRECT LEN')
    else:
        Fail('INCORRECT TYPE')
except Exception as e:
    Fail(e)

try:
    id = Request_index.get_id('TEST')
    rsp = Request_index.update('TEST1', id)
    if rsp == True:
        Pass()
    else:
        Fail('INCORRECT TYPE')
except Exception as e:
    Fail(e)

try:
    id = Request_index.get_id('TEST')
    rsp = Save.new('TEST', 'http://test.com/', 'GET', 'TEST=TEST', {"test": "test"})
    if rsp == True:
        Pass()
    else:
        Fail('INCORRECT TYPE')
except Exception as e:
    Fail(e)

try:
    rsp = Save.clear()
    if rsp == True:
        Pass()
    else:
        Fail('INCORRECT TYPE')
except Exception as e:
    Fail(e)

Clear()