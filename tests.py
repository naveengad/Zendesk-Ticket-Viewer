import unittest
import main
import APIrequest

class Tests(unittest.TestCase):    
    # test for get_tickets
    def test_get_tickets(self):
        api = APIrequest.APIrequest()
        resp = api.get_tickets()
        self.assertTrue(resp[0])

    # test for get_ticket_id(5)
    def test_get_ticket_id(self):
        api = APIrequest.APIrequest()
        resp = api.get_ticket_id(5)
        self.assertTrue(resp[0])

    # test for get_json_objects using url with ticket ID
    def test_get_json_objects(self):
        url = "https://naveengaddam.zendesk.com/api/v2/tickets/5.json"
        api = APIrequest.APIrequest()
        resp = api.get_json_objects(url)
        self.assertTrue(resp[0])

    # test for get_json_objects using url for all tickets
    def test_get_json_objects(self):
        url = "https://naveengaddam.zendesk.com/api/v2/tickets.json"
        api = APIrequest.APIrequest()
        resp = api.get_json_objects(url)
        self.assertTrue(resp[0])

    # test for handle_error
    def test_handle_error(self):
        api = APIrequest.APIrequest()
        resp = api.handle_error(401)
        self.assertTrue(not resp[0] and resp[1] == "Validation of username and password failed. Please try again with correct credentials.")

    # test for format_datetime
    def test_format_datetime(self):
        resp = main.format_datetime("2018-02-11T09:10:06Z")
        self.assertTrue(resp[0] == "11/02/2018" and resp[1] ==  "09:10")

if __name__ == "__main__":
    unittest.main()
