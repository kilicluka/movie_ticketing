# Movie Ticketing
Simple app simulating a movie ticket purchasing cycle.


# Note
There's a `fixtures.json` file with some initial movies, halls, showtimes and seats.

# About the app
To be able to make reservations, users have to be logged in. JWT authentication is used for that purpose.

The idea for the usage is:
- once the user logs in, they select the showtime they want to purchase the tickets for
- if the user already has an `OPEN` reservation for that showtime, that one has to be used
- when the user doesn't have any reservations, they get created by the user selecting a single seating for the showtime
- this triggers a `POST` request and creates the reservation
- every subsequent seating pick triggers a `PUT` request, sending all of the user's currently selected seats
- only available seats + the seats already selected by the user are allowed for `PUT` requests
- reservations (and their updates) can be made only up to a certain point before the movie (30 minutes by default)
- once created, the reservation stays active for 15 minutes. Seat updates don't increase this time
- in a production environment, a cron job would be running every N minutes, deleting all of the expired reservations
- to complete a reservation (no payment methods are implemented) a `PATCH` request is sent to `reservations/uuid/complete`
