import random
import requests
from .config_file import SettingConfig


def GET(api_url):
    Read = SettingConfig().ReadSetting()
    """封装get方法"""
    headers = {'User_Agent': random.choice(
        Read.get('USER_AGENT_LIST'))}
    try:
        result = requests.get(api_url, headers=headers)
        return result.json()
    except Exception as e:
        print("get请求错误: %s" % e)

def get_dict_value(date, keys, default=None):
    keys_list = keys.split('.')
    if isinstance(date, dict):
        dictionary = dict(date)
        for i in keys_list:
            try:
                if dictionary.get(i) != None:
                    dict_values = dictionary.get(i)
                elif dictionary.get(i) == None:
                    dict_values = dictionary.get(int(i))
            except:
                return default
            dictionary = dict_values
        return dictionary
    else:
        try:
            dictionary = dict(eval(date))
            if isinstance(dictionary, dict):
                for i in keys_list:
                    try:
                        if dictionary.get(i) != None:
                            dict_values = dictionary.get(i)
                        elif dictionary.get(i) == None:
                            dict_values = dictionary.get(int(i))
                    except:
                        return default
                    dictionary = dict_values
                return dictionary
        except:
            return default
