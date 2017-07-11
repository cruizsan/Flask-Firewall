import json
import re
from flask import abort


class flask_firewall:
    def __init__(self, request, user_groups, config='security/firewall/flask_firewall.json'):
        with open(config) as json_data:
            self.config = json.load(json_data)
        self.routes = self._get_routes(r_type='include')
        self.exclude = self._get_routes(r_type='exclude')
        self.request = request
        self.user_groups = user_groups
        self.abort_func = abort

        if self.is_route_defined_in_firewall():
            if self._is_include():
                error = self._check_routing()
                if error['error']:
                    self.abort_func(error['error_code'])
        else:
            behavior = self.config['flask_firewall']['behavior']
            if behavior.lower() == 'unauthorized':
                self.abort_func(403)

    def get_group(self, route):
        for r in self.routes:
            route_regex = r['route']
            if re.search(route_regex, route):
                return {'groups': r['groups'], 'error': r['error_code']}
        return None

    def get_user_groups(self):
        return self.user_groups

    def is_route_defined_in_firewall(self):
        all_routes = self.routes
        routes = []
        for r in all_routes:
            routes.append(r['route'])

        all_routes = self.exclude
        for r2 in all_routes:
            routes.append(r2)

        route = self._get_request_path()
        for r in routes:
            if re.search(r, route):
                return True
        return False

    def _check_routing(self):
        route = self._get_request_path()
        route_groups_valid = self.get_group(route)
        user_groups_valid = self.user_groups
        if not route_groups_valid:
            return True
        error_code = route_groups_valid['error']
        route_groups_valid = route_groups_valid['groups']
        if not isinstance(route_groups_valid, list):
            route_groups_valid = [route_groups_valid]
        if not isinstance(user_groups_valid, list):
            user_groups_valid = [user_groups_valid]

        for user_g in user_groups_valid:
            if user_g in route_groups_valid:
                return {'error': False, 'error_code': None}
        return {'error': True, 'error_code': error_code}

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
