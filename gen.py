import requests
import json
import time
import asyncio
import uuid
import shortuuid


headers = {
    'Accept': '*/*',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'en-US,en;q=0.5',
    'Alt-Used': 'spicy.porn',
    'Connection': 'keep-alive',
    'Content-type': 'application/x-www-form-urlencoded',
    'Host': 'spicy.porn',
    'Origin': 'https://spicy.porn',
    'Referer': 'https://spicy.porn/login',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:121.0) Gecko/20100101 Firefox/121.0',
}

def urlencode_dict(data):
    """
    Convert a dictionary to x-www-form-urlencoded format.
    """
    encoded_data = "&".join([f"{key}={value}" for key, value in data.items()])
    return encoded_data



def save_cookies(cookies):
    cookies = requests.utils.dict_from_cookiejar(cookies)
    with open('cookies.json','r') as infile:
        cookies_dict = json.load(infile)
    l = len(cookies_dict["cookies"])
    l=l+1
    arr = [cookies,1,0]
    cookies_dict["cookies"][f'{l}']=arr
    with open('cookies.json','w') as outfile:
        json.dump(cookies_dict,outfile)
    return f'{l}'

def load_cookies():
    flag = 0
    with open('cookies.json','r') as infile:
        cookies_dict = json.load(infile)
    
    for i in cookies_dict["cookies"]:
        print(i,cookies_dict["cookies"][i][1]==0,cookies_dict["cookies"][i][2]<=7)
        if(cookies_dict["cookies"][i][1]==0 and cookies_dict["cookies"][i][2]<=7):
            print(cookies_dict["cookies"][i][1]==0,cookies_dict["cookies"][i][2]<=7)
            flag=1
            cookies = cookies_dict["cookies"][i][0]
            cookies_dict["cookies"][i][1]=1
            with open('cookies.json','w') as outfile:
                json.dump(cookies_dict,outfile)
            id = i;
            break
    if(flag==0):
        cookies=None
        id=None
    return [cookies,id]




def signup(session):
    url = "https://spicy.porn/signup"
    uid = shortuuid.uuid()
    data = f"email={uid}@olen.com&password=l242444"
    request = session.post(url,headers=headers,data=data)
    cookies = session.cookies
    print(cookies)
    id=save_cookies(cookies)
    return [cookies['user_id'],f'{id}']

def login(session,cookies):
    session.cookies.update(cookies)
    return cookies['user_id']



def submit(user_id,session,id,data):
    url = 'https://spicy.porn/submit'
    data = data
    request = session.post(url, headers=headers, data=data)


    url3 = f"https://spicy.porn/user/{user_id}?last_t=0&last_pid=pid"
    c = -1
    url = None
    for i in range(0,100):
        request = session.get(url3)
        json_data = json.loads(request.content.decode('utf-8'))
        p = len(json_data["new_images"])
        if(c==-1):
            c=p
        else:
            if(p>c):
                first_key = list(json_data["new_images"].keys())[0]
                url = json_data["new_images"][first_key]['i']
                print(url)
                break
        time.sleep(3)
    with open('cookies.json','r') as infile:
        cookies_dict = json.load(infile)
    cookies_dict["cookies"][id][1]=0
    cookies_dict["cookies"][id][2]=cookies_dict["cookies"][id][2]+1
    with open('cookies.json','w') as outfile:
        json.dump(cookies_dict,outfile)
    print(url)
    if(url!=None):
       return "https://spicy.porn/imgthumb/"+url
    else:
        return None


# Create a session
    

async def main(data):
    loop = asyncio.get_event_loop()
    session = requests.Session()
    cookiesArr = await loop.run_in_executor(None,load_cookies) 
    if(cookiesArr[0]==None):
        sgn=await loop.run_in_executor(None,signup,session)
        user=sgn[0]
        cookieId = sgn[1]
    else:
        cookies = cookiesArr[0]
        cookieId = cookiesArr[1]
        user=await loop.run_in_executor(None,login,session,cookies)
    url = await loop.run_in_executor(None,submit,user,session,cookieId,data)
    return url

