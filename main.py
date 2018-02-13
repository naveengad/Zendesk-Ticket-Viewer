import APIrequest
import re

# format the date and time
# return date in dd/mm/yyyy format and time in hh:mm format
def format_datetime(datetime):
    dt = datetime.split("T")
    raw_date = dt[0].split("-")
    raw_date = list(reversed(raw_date))
    date = "/".join(raw_date)
    time = dt[1][:-4]
    return (date, time)

# method to get and display all the tickets
def display_all_tickets(api):
    print("Fetching the tickets.")    
    tkts = api.get_tickets()
    # return if there is some error
    if not tkts[0]:
        print(tkts[1])
        return False
    tickets = tkts[1] 
    # get the count of tickets   
    count = len(tickets)
    # each page consists of 25 records
    start = 0
    end = 25
    while start < count:
        if end > count: end = count
        # loop through 25 records and display them
        for i in range(start, end):
            ticket = tickets[i]
            # format date and time to display
            date, time = format_datetime(ticket["created_at"])
            # build the ticket structure to display
            ticket_disp = "TICKET ID: " + str(ticket['id']) + " | STATUS: " + ticket['status'].lower()
            ticket_disp += " | SUBJECT: " + ticket['subject'].lower() + ". | OPENED BY: " + str(ticket['submitter_id'])
            ticket_disp += " | DATE(dd/mm/yyyy): " + date + " | Time(hh:mm): " + time
            # display the ticket
            print(ticket_disp)
        print("\nDisplaying tickets " + str(start+1) + "-" + str(end) + " of " + str(count))
        # reached last page
        if end == count:
            print("\nDisplayed all tickets")
        while True:
            # provide 4 possible action options to the user
            print("\n*********************************SUB MENU*********************************")
            print("\nChoose an option")
            print("1. Go to Previous page")
            print("2. Go to Next page")
            print("3. Display ticket by ID")
            print("4. Return to MAIN MENU")
            val = input("Please input 1 or 2 or 3 or 4 and press 'Enter':\n")
            # return to previous page, in case of first page, display first page
            if int(val) == 1:
                if start != 0:
                    end = start
                    start -= 25                    
                break
            # go to next page,in case we reached last page, display first page
            elif int(val) == 2:
                if end == count:
                    start = 0
                    end = 25
                else:
                    start = end
                    end += 25
                break
            # display a specific ticket
            elif int(val) == 3:
                id = input("Enter the ticket id and press 'Enter': \n")
                done = display_each_ticket(api, int(id)) 
            # return from the method to stop display of tickets
            elif int(val) == 4:
                return True
            # invalid input
            else:
                print("You entered an invalid input. Please try again with valid input.")    

# display a specific ticket provided its ID
def display_each_ticket(api, id):
    print("Fetching the ticket with ID: " + str(id))
    # get ticket with provided ID       
    tkts = api.get_ticket_id(id) 
    # return in case of error   
    if not tkts[0]:
        print("\n" + tkts[1])
        return
    ticket = tkts[1]
    # format the date and time to display
    date, time = format_datetime(ticket["created_at"])
    # print the details of the ticket with provided ID
    print("\nTICKET ID: " + str(ticket["id"]))
    print("STATUS: " + ticket['status'].lower())
    print("CREATED DATE(dd/mm/yyyy): " + date)
    print("CREATED TIME(hh:mm): " + time)
    print("SUBJECT: " + ticket["subject"])
    print("DESCRIPTION:\n" + ticket["description"])    

if __name__ == "__main__":
    # print welcome message
    print("Welcome to the Zendesk Ticket Viewer")
    # build the APIrequest object
    api = APIrequest.APIrequest()
    # loop through until the user select exit option
    while True:
        # provide 3 possible action options to the user
        print("\n*********************************MAIN MENU*********************************")
        print("\nChoose your option")
        print("1. Display all tickets")
        print("2. Display ticket by ID")
        print("3. Quit")
        cmd = input("Please input 1 or 2 or 3 and press 'Enter':\n")  
        # dislay all tickets      
        if cmd == str(1):
            display_all_tickets(api) 
        # display a specific ticket with provided ID        
        elif cmd == str(2):             
            id = input("Enter the ticket id and press 'Enter': \n")
            done = display_each_ticket(api, int(id))
        # exit from the application            
        elif cmd == str(3):
            print("Exiting the application")
            print("Thank You")
            exit()
        # invalid input
        else:
            print("You entered an invalid input. Please try again with valid input.")
