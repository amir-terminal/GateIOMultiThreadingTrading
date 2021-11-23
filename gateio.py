# from gevent import monkey as curious_george
import requests
# curious_george.patch_all(thread=False, select=False)
from concurrent.futures import ThreadPoolExecutor
import time
import hashlib
import hmac
# import grequests
# from concurrent.futures import ThreadPoolExecutor

def gen_sign(method, url, query_string=None, payload_string=None):
    key = '6a44db421dd2e49e85174eb528010cd0'        # api_key
    secret = 'dbb4354841ec6c77d2cc5b1076df1f8574346210499966d34c32b89298fed829'     # api_secret

    t = time.time()
    m = hashlib.sha512()
    m.update((payload_string or "").encode('utf-8'))
    hashed_payload = m.hexdigest()
    s = '%s\n%s\n%s\n%s\n%s' % (
        method, url, query_string or "", hashed_payload, t)
    sign = hmac.new(secret.encode('utf-8'), s.encode('utf-8'),
                    hashlib.sha512).hexdigest()
    return {'KEY': key, 'Timestamp': str(t), 'SIGN': sign}



start_time = time.time()
body = ['{"text":"t-123456","currency_pair":"CWAR_USDT","type":"limit","account":"spot","side":"buy","iceberg":"0","amount":"100","price":"0.4","time_in_force":"gtc","auto_borrow":false}',
        '{"text":"t-123456","currency_pair":"CWAR_USDT","type":"limit","account":"spot","side":"buy","iceberg":"0","amount":"114","price":"0.35","time_in_force":"gtc","auto_borrow":false}', 
        '{"text":"t-123456","currency_pair":"CWAR_USDT","type":"limit","account":"spot","side":"buy","iceberg":"0","amount":"117","price":"0.34","time_in_force":"gtc","auto_borrow":false}', 
        '{"text":"t-123456","currency_pair":"CWAR_USDT","type":"limit","account":"spot","side":"buy","iceberg":"0","amount":"121","price":"0.33","time_in_force":"gtc","auto_borrow":false}', 
        '{"text":"t-123456","currency_pair":"CWAR_USDT","type":"limit","account":"spot","side":"buy","iceberg":"0","amount":"133","price":"0.31","time_in_force":"gtc","auto_borrow":false}', 
        '{"text":"t-123456","currency_pair":"CWAR_USDT","type":"limit","account":"spot","side":"buy","iceberg":"0","amount":"180","price":"0.2219","time_in_force":"gtc","auto_borrow":false}',
        '{"text":"t-123456","currency_pair":"CWAR_USDT","type":"limit","account":"spot","side":"buy","iceberg":"0","amount":"180","price":"0.2218","time_in_force":"gtc","auto_borrow":false}', 
        '{"text":"t-123456","currency_pair":"CWAR_USDT","type":"limit","account":"spot","side":"buy","iceberg":"0","amount":"180","price":"0.2217","time_in_force":"gtc","auto_borrow":false}',
        '{"text":"t-123456","currency_pair":"CWAR_USDT","type":"limit","account":"spot","side":"buy","iceberg":"0","amount":"180","price":"0.2216","time_in_force":"gtc","auto_borrow":false}', 
        '{"text":"t-123456","currency_pair":"CWAR_USDT","type":"limit","account":"spot","side":"buy","iceberg":"0","amount":"180","price":"0.2215","time_in_force":"gtc","auto_borrow":false}',
        '{"text":"t-123456","currency_pair":"CWAR_USDT","type":"limit","account":"spot","side":"buy","iceberg":"0","amount":"180","price":"0.2214","time_in_force":"gtc","auto_borrow":false}', 
        '{"text":"t-123456","currency_pair":"CWAR_USDT","type":"limit","account":"spot","side":"buy","iceberg":"0","amount":"180","price":"0.2213","time_in_force":"gtc","auto_borrow":false}', 
        '{"text":"t-123456","currency_pair":"CWAR_USDT","type":"limit","account":"spot","side":"buy","iceberg":"0","amount":"180","price":"0.2212","time_in_force":"gtc","auto_borrow":false}',
        '{"text":"t-123456","currency_pair":"CWAR_USDT","type":"limit","account":"spot","side":"buy","iceberg":"0","amount":"180","price":"0.2211","time_in_force":"gtc","auto_borrow":false}', 
        '{"text":"t-123456","currency_pair":"CWAR_USDT","type":"limit","account":"spot","side":"buy","iceberg":"0","amount":"180","price":"0.2199","time_in_force":"gtc","auto_borrow":false}',
        ]*5

def get_url(b):
    host = "https://api.gateio.ws"
    prefix = "/api/v4"
    headers = {'Accept': 'application/json', 'Content-Type': 'application/json'}
    url = '/spot/orders'
    query_param = ''
    # for `gen_sign` implementation, refer to section `Authentication` above
    sign_headers = gen_sign('POST', prefix + url, query_param, b)
    headers.update(sign_headers)
    return requests.request('POST', host + prefix + url, headers=headers, data=b)

# r = (grequests.request('POST',host + prefix + u,
#                      headers=headers, data=body) for u in urls)
# r = requests.post( host + prefix + url, headers=headers, data=body)
# print(r.json())
# grequests.map(r)
i = 0
while True:
    with ThreadPoolExecutor(max_workers=90) as pool:
        print(list(pool.map(get_url,body)))
    i+=1
    print(i)

        