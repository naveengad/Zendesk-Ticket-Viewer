import json
import requests


class APIrequest:
    def __init__(self):
        self.URL = "https://naveengaddam.zendesk.com/api/v2/tickets.json"
        self.username = "naveengaddam28@gmail.com"
        self.password = "28@May91"
        self.url_prefix = "https://naveengaddam.zendesk.com/api/v2/tickets/"
        self.url_suffix = ".json"
        self.tickets_cache = []

    # get_ticket_id: gets the specific ticket
    # returns ticket with id equal to tkt_id
    def get_ticket_id(self, tkt_id):
        # if tickets are already fetched, return the ticket from the cache
        if self.tickets_cache: 
            count = len(self.tickets_cache)
            # check whether ticket id is in the range
            if 0 < tkt_id <= count:
                return (True, self.tickets_cache[tkt_id - 1])
            else:
                return (False, "Ticket with ID " + str(tkt_id) + " is not present.")
        # build the url with provided ticket id
        url = self.url_prefix + str(tkt_id) + self.url_suffix
        try:
            resp = self.get_json_objects(url)
        except:
            return (False, "Failed to estabilsh a new connection with the server. Please check your INTERNET connection and try again.")
        # check for status error
        if not resp[0]:
            if resp[1] == 404:
                return (False, "Ticket with ID " + str(tkt_id) + " is not present.")
            return resp
        # return the ticket
        json_obj = resp[1]        
        ticket = json_obj["ticket"]
        return (True, ticket)

    # getTickets: gets all the tickets from the Zendesk account
    # returns: a list of dictionaries, each dictionary corresponding to a ticket's contents
    def get_tickets(self):
        url = self.URL
        tickets = []
        while url:            
            # call the Zendesk API and get tickets
            try:
                resp = self.get_json_objects(url)
            except:
                error_msg = "Failed to estabilsh a new connection with the server. "
                error_msg += "Please check your INTERNET connection and try again."
                return (False,  error_msg)
            # check for status error
            if not resp[0]:
                return resp
            json_obj = resp[1]
            # extend tickets with recieved json ticket objects
            tickets += json_obj["tickets"]
            # get next page URL                    
            url = json_obj["next_page"] 
        self.tickets_cache = tickets       
        return (True, tickets)

    # get_json_objects: gets the json object of ticket(s) 
    # return json in case of success, else return error message
    def get_json_objects(self, url):
        response = requests.get(url, auth=(self.username, self.password))
        # check for any status error
        if response.status_code != 200:
            error = self.handle_error(response.status_code)
            return error            
        return (True, response.json())

    # based on status code, handle the error and build error message
    # return the error message along with False flag
    def handle_error(self, status):
        # bad request error
        if status == 400:
            error_msg = "Server cannot or will not process the request due to an apparent client error"
            error_msg += " (e.g., malformed request syntax, size too large, invalid request message framing)."
        # unauthorised error
        elif status == 401:
            error_msg = "Validation of username and password failed. Please try again with correct credentials."
        # record not found
        elif status == 404:
            # will build the error message with ticket ID in get_ticket_id method
            error_msg = 404
         # request time out
        elif status == 408:
            error_msg = "The server timed out waiting for the request. Please try again."   
        # Server errors or any other errors 
        else:
            error_msg = "Cannot process the request at this moment. Please wait for few minutes and try again."       
        return (False, error_msg)
