hotel_booking_client.py 
import Pyro4 
 
def main(): 
    try: 
        hotel_booking = Pyro4.Proxy("PYRONAME:hotel.booking.server") 
        print("Connected to the Hotel Booking Server.\n") 
    except Pyro4.errors.PyroError: 
        print("Error: Could not connect to the Hotel Booking Server.") 
        return 
 
    while True: 
        operation = input("Enter operation (BOOK/CANCEL/EXIT): ").strip().upper() 
 
        if operation == "EXIT": 
            print("Exiting... Thank you!") 
            break 
 
        elif operation == "BOOK": 
            guest = input("Enter guest name: ").strip() 
            room = input("Enter room number: ").strip() 
 
            if not room.isdigit(): 
                print("Invalid room number. Please enter a numeric value.") 
                continue 
 
            response = hotel_booking.book_room(guest, room) 
            print(response) 
 
        elif operation == "CANCEL": 
            guest = input("Enter guest name: ").strip() 
            response = hotel_booking.cancel_booking(guest) 
            print(response) 
 
        else: 
            print("Invalid operation. Please enter BOOK, CANCEL, or EXIT.") 
 
if __name__ == "__main__": 
    main()




part 2 of code 
hotel_booking_server.py 

import Pyro4 
 
@Pyro4.expose 
class HotelBookingServer: 
    def __init__(self): 
        self.rooms = {} 
 
    def book_room(self, guest, room): 
        if room in self.rooms: 
            return f"Room {room} is already booked." 
        else: 
            self.rooms[room] = guest 
            return f"Room {room} booked for {guest}." 
 
    def cancel_booking(self, guest): 
        for room, booked_guest in list(self.rooms.items()): 
            if booked_guest == guest: 
                del self.rooms[room] 
                return f"Booking for {guest} cancelled." 
        return f"No booking found for {guest}." 
 
if __name__ == "__main__": 
    daemon = Pyro4.Daemon() 
    ns = Pyro4.locateNS() 
    server = HotelBookingServer() 
    uri = daemon.register(server) 
    ns.register("hotel.booking.server", uri) 
    print("Hotel Booking Server is ready.") 
    daemon.requestLoop()
