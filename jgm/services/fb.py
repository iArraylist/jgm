import urllib
import json


class GraphAPI(object):
    def __init__(self, access_token=None):
        self.access_token = access_token

    def get_object(self, path, **args):
        """Fetches the given object from the graph."""
        return self.request(path, args)

    def request(self, path, args=None, post_args=None):
        """Fetches the given path in the Graph API.

        We translate args to a valid query string. If post_args is given,
        we send a POST request to the given path with the given arguments.
        """
        if not args:
            args = {}
        if self.access_token:
            if post_args is not None:
                post_args["access_token"] = self.access_token
            else:
                args["access_token"] = self.access_token
        post_data = None if post_args is None else urllib.urlencode(post_args)
        f = urllib.urlopen("https://graph.facebook.com/" + path + "?" + urllib.urlencode(args), post_data)
        try:
            data = f.read()
        finally:
            f.close()
        try:
            response = json.loads(data)
            if response.get("error"):
                raise GraphAPIError(response["error"].get("code", 1),
                                    response["error"]["message"])
        except ValueError:
            response = data

        return response


class GraphAPIError(Exception):
    def __init__(self, code, message):
        Exception.__init__(self, message)
        self.code = code