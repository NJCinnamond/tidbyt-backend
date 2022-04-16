import http.client
import json


class TidbytAPIClient:
    def __init__(self, host):
        self.host = host
        self.conn = http.client.HTTPSConnection(host, port=None)

    def get(self, path, headers):
        self.conn.request("GET", path, headers=headers)
        return self.conn.getresponse()

    def post(self, path, data, headers):
        print("PATH: ", path)
        self.conn.request("POST", path, data, headers=headers)
        return self.conn.getresponse()

    def put(self, path, data):
        self.conn.request("PUT", path, data)
        return self.conn.getresponse()

    def delete(self, path, headers):
        self.conn.request("DELETE", path, headers=headers)
        return self.conn.getresponse()

    def get_headers(self, authorization_token):
        headers = {
            "Authorization": "Bearer {}".format(str(authorization_token)),
            "Content-Type": "application/json",
        }
        return headers

    def install_to_device(self, device_id, authorization_token, installation_id, image):
        headers = self.get_headers(authorization_token)
        print("IMAGE: ", image)
        data = json.dumps(
            {
                "image": image,
                "installationID": installation_id,
                "background": False,  # TODO: Should we make this a field in TidbytInstallation?
            }
        )

        path = "/v0/devices/{}/push".format(device_id)
        return self.post(path, data, headers)

    def uninstall_from_device(self, device_id, authorization_token, installation_id):
        headers = self.get_headers(authorization_token)
        path = "/v0/devices/{}/installations/{}".format(device_id, installation_id)
        print("PATH: ", path)
        return self.delete(path, headers)

    def list_installations(self, device_id, authorization_token):
        headers = self.get_headers(authorization_token)
        path = "/v0/devices/{}/installations".format(device_id)
        return self.get(path, headers)

    def get_installation(self, device_id, authorization_token, installation_id):
        headers = self.get_headers(authorization_token)
        path = "/v0/devices/{}/installations/{}/preview".format(
            device_id, installation_id
        )
        return self.get(path, headers)

    def get_device(self, device_id, authorization_token):
        headers = self.get_headers(authorization_token)
        path = "/v0/devices/{}".format(device_id)
        return self.get(path, headers)
