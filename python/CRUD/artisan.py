from python.database_init import sqlite_connection


# CREATE

def add_artisan(name, location, speciality, connection):
    cursor = connection.cursor()
    try:
        cursor.execute("INSERT INTO Artisans (Name, Location, Speciality) VALUES (?, ?, ?)",
                       (name, location, speciality))
        connection.commit()
    except Exception as e:
        print(f"Error adding artisan: {e}")
        connection.rollback()  # Important: Rollback on error
    finally:
        connection.close()


# READ

def get_artisans(connection):
    cursor = connection.cursor()
    try:
        cursor.execute("SELECT * FROM Artisans")
        artisans = cursor.fetchall()
    except Exception as e:
        print(f"Error getting artisans: {e}")
        artisans = []
    finally:
        connection.close()
    return artisans


# UPDATE

def update_artisan(artisan_id, name, location, specialty, connection):
    cursor = connection.cursor()
    try:
        cursor.execute("UPDATE Artisans SET Name=?, Location=?, Speciality=? WHERE ArtisanID=?",
                       (name, location, specialty, artisan_id))
        connection.commit()
    except Exception as e:
        print(f"Error updating artisan: {e}")
        connection.rollback()
    finally:
        connection.close()


# DELETE

def delete_artisan(artisan_id, connection):
    cursor = connection.cursor()
    try:
        cursor.execute("DELETE FROM Artisans WHERE ArtisanID=?",
                       (artisan_id))
        connection.commit()
    except Exception as e:
        print(f"Error deleting artisan: {e}")
        connection.rollback()
    finally:
        connection.close()

