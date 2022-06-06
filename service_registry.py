import time
import threading
import redis
import json

# 连接数据库
try:
    with open('database.json', 'r', encoding='utf8') as fp:
        config = json.load(fp)
        fp.close()

    redis_pool = redis.ConnectionPool(host=config["host"], port=config["port"],
                                      password=config["password"], db=config["db"])
except:
    print("数据库连接失败")
    exit(-1)


class RegistryThread(threading.Thread):
    def __init__(self, service_name: str, ip: str, host: str, time_len: int):
        threading.Thread.__init__(self)
        self.service_name = service_name
        self.ip = ip
        self.host = host
        self.time_len = time_len
        self.rds = redis.Redis(connection_pool=redis_pool)

    def run(self):
        url = get_local_url(self.ip, self.host)
        while True:
            self.rds.sadd(self.service_name, url)
            self.rds.set(url, "ok")
            self.rds.expire(url, self.time_len + 1)
            time.sleep(self.time_len)


def registry(service_name: str, ip: str, host: str, time_len):
    thread = RegistryThread(service_name, ip, host, time_len)
    thread.start()


def get_local_url(ip: str, host: str) -> str:
    return ip + ':' + host
