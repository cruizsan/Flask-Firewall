import json
import re

class flask_firewall:
    def __init__(self, request, user_groups, abort_func, config='security/firewall/flask_firewall.json'):
        with open(config) as json_data:
            self.config = json.load(json_data)
        self.routes = self._get_routes(r_type='include')
        self.exclude = self._get_routes(r_type='exclude')
        self.request = request
        self.user_groups = user_groups
        self.abort_func = abort_func
        if self._is_include():
            if not self._check_routing():
                self.abort_func(403)

    def get_group(self, route):
        for r in self.routes:
            route_regex = r['route']
            if re.search(route_regex, route):
                return r['groups']
        return None

    def get_user_groups(self):
        return self.user_groups

    def _check_routing(self):
        route = self._get_request_path()
        route_groups_valid = self.get_group(route)
        user_groups_valid = self.user_groups
        if not route_groups_valid:
            return True
        if not isinstance(route_groups_valid, list):
            route_groups_valid = [route_groups_valid]
        if not isinstance(user_groups_valid, list):
            user_groups_valid = [user_groups_valid]

        for user_g in user_groups_valid:
            if user_g in route_groups_valid:
                return True
        return False

    def _is_include(self):
        route = self._get_request_path()
        for exclude in self.exclude:
            route_regex = exclude
            if re.search(route_regex, route):
                return False
        return True

    def _get_request_path(self):
        return self.request.path

    def _get_routes(self, r_type='include'):
        routes = []
        try:
            routes_config = self.config['flask_firewall']['routing'][r_type]
            if not isinstance(routes_config, list):
                routes_config = [routes_config]
        except Exception, e:
            print("ERROR flask_firewall._get_routes >>>>")
            print(e)
            print("<<<< ERROR flask_firewall._get_routes")
            routes_config = []
        for r in routes_config:
            routes.append(r)
        return routes
