import urllib.request, urllib.parse, urllib.error
import urllib.request, urllib.error, urllib.parse

class StatHat:

        def http_post(self, path, data):
                pdata = bytes(urllib.parse.urlencode(data).encode())
                req = urllib.request.Request('http://api.stathat.com' + path, pdata)
                resp = urllib.request.urlopen(req)
                return resp.read()

        def post_value(self, user_key, stat_key, value, timestamp=None):
                args = {'key': stat_key, 'ukey': user_key, 'value': value}
                if timestamp is not None:
                        args['t'] = timestamp
                return self.http_post('/v', args)

        def post_count(self, user_key, stat_key, count, timestamp=None):
                args = {'key': stat_key, 'ukey': user_key, 'count': count}
                if timestamp is not None:
                        args['t'] = timestamp
                return self.http_post('/c', args)

        def ez_post_value(self, ezkey, stat_name, value, timestamp=None):
                args = {'ezkey': ezkey, 'stat': stat_name, 'value': value}
                if timestamp is not None:
                        args['t'] = timestamp
                return self.http_post('/ez', args)

        def ez_post_count(self, ezkey, stat_name, count, timestamp=None):
                args = {'ezkey': ezkey, 'stat': stat_name, 'count': count}
                if timestamp is not None:
                        args['t'] = timestamp
                print(args)
                return self.http_post('/ez', args)

