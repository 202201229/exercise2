import sqlite3

# Read the file
file_path = 'stephen_king_adaptations.txt'
with open(file_path, 'r') as file:
    content = file.readlines()

# Copy content to a list
stephen_king_adaptations_list = []
for line in content:
    movie_id, movie_name, movie_year, imdb_rating = line.strip().split(',')
    stephen_king_adaptations_list.append([movie_id, movie_name, int(movie_year), float(imdb_rating)])  # Use a list instead of a tuple

# Establish connection with SQLite database
conn = sqlite3.connect('stephen_king_adaptations.db')
c = conn.cursor()

# Create a table
c.execute('''CREATE TABLE IF NOT EXISTS stephen_king_adaptations_table
             (movieID TEXT, movieName TEXT, movieYear INTEGER, imdbRating REAL)''')

# Insert data into the table
c.executemany("INSERT INTO stephen_king_adaptations_table VALUES (?, ?, ?, ?)",
              stephen_king_adaptations_list)

# Commit the changes
conn.commit()

# Rest of the code unchanged...

# User interaction loop
while True:
    print("Please select an option:")
    print("1. Search by movie name")
    print("2. Search by movie year")
    print("3. Search by movie rating")
    print("4. STOP")
    option = input("Enter your choice: ")

    if option == '1':
        movie_name = input("Enter the name of the movie to search: ")
        c.execute("SELECT * FROM stephen_king_adaptations_table WHERE movieName=?", (movie_name,))
        result = c.fetchall()
        if result:
            print("Movie details:")
            for movie in result:
                print("ID:", movie[0])
                print("Name:", movie[1])
                print("Year:", movie[2])
                print("Rating:", movie[3])
        else:
            print("No such movie exists in our database.")

    elif option == '2':
        movie_year = input("Enter the year of the movie to search: ")
        c.execute("SELECT * FROM stephen_king_adaptations_table WHERE movieYear=?", (movie_year,))
        result = c.fetchall()
        if result:
            print("Movies released in", movie_year)
            for movie in result:
                print("ID:", movie[0])
                print("Name:", movie[1])
                print("Year:", movie[2])
                print("Rating:", movie[3])
        else:
            print("No movies were found for that year in our database.")

    elif option == '3':
        rating = float(input("Enter the minimum rating to search: "))
        c.execute("SELECT * FROM stephen_king_adaptations_table WHERE imdbRating >= ?", (rating,))
        result = c.fetchall()
        if result:
            print("Movies with a rating of", rating, "and above:")
            for movie in result:
                print("ID:", movie[0])
                print("Name:", movie[1])
                print("Year:", movie[2])
                print("Rating:", movie[3])
        else:
            print("No movies at or above that rating were found in the database.")

    elif option == '4':
        break

# Close the connection
conn.close()