# -*- coding: utf-8 -*
__author__ = 'admin'
import requests
import hashlib
import time

class PlayvisionAPI(object):

    __API_URL__ = "http://api.playvision.ru/v1/"

    def __init__(self, project_id, api_secret):
        self._project_id = project_id
        self._api_secret = api_secret

    def _send_request_(self, method, **parameters):
        sig = hashlib.md5()
        for key in sorted(parameters.keys()):
            sig.update("%s=%s" % (key, parameters[key]))
        sig.update("%s=%s" % ("token", self._api_secret))
        parameters["sig"] = sig.hexdigest()
        result = requests.get(self.__API_URL__ + method, params=parameters)
        if result.status_code == requests.codes.ok:
            return result.json()["response"]
        else:
            # TODO: обработать ошибку
            print "ERROR"
            return None

    def users_get(self, user_ids):
        # user_ids - проверить, что это список целых чисел
        assert sum(map(lambda x: not isinstance(x, (int, long)), user_ids)) == 0
        # переделать в строку
        user_ids = ",".join([str(i) for i in user_ids])
        # сформировать запрос и отправить его
        return self._send_request_("users.get", user_ids=user_ids)

    def friends_get(self, user_id):
        # проверка того, что дали айдишку
        assert isinstance(user_id, (int, long))
        # сформировать запрос и отправить его
        return self._send_request_("friends.get", user_id=user_id)

    def friends_get_app_users(self, user_id):
        # проверка того, что дали айдишки
        assert isinstance(user_id, (int, long))
        # сформировать запрос и отправить его
        return self._send_request_("friends.getAppUsers", user_id=user_id, project_id=self._project_id)

    def wall_get(self, user_id):
        # проверка того, что дали айдишку
        assert isinstance(user_id, (int, long))
        # сформировать запрос и отправить его
        return self._send_request_("wall.get", user_id=user_id)

    def wall_post(self, user_id, token, message, psid):
        # проверка того, что дали то, чео надо было
        assert isinstance(user_id, (int, long))
        assert isinstance(message, str)
        assert isinstance(psid, (int, long))
        assert isinstance(token, str)
        return self._send_request_("wall.post", user_id=user_id, project_id=self._project_id,token=token,message=message,psid=psid)

    def secure_set_user_level(self, user_id, level, psid):
        # проверка того, что дали то, чео надо было
        assert isinstance(user_id, (int, long))
        assert isinstance(level, (int, long))
        assert isinstance(psid, (int, long))
        current_time = time.time()
        return self._send_request_("secure.setUserLevel", user_id=user_id, project_id=self._project_id,level=level,
                                   time=current_time, psid=psid)

    # работа с магазином
    # платежный API