from python.database_init import create_connection


# CREATE

def add_artisan(name, location, speciality):
    conn = create_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO Artisans (Name, Location, Speciality) VALUES (?, ?, ?)",
                       (name, location, speciality))
        conn.commit()
    except Exception as e:
        print(f"Error adding artisan: {e}")
        conn.rollback()  # Important: Rollback on error
    finally:
        conn.close()


# READ

def get_artisans():
    conn = create_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM Artisans")
        artisans = cursor.fetchall()
    except Exception as e:
        print(f"Error getting artisans: {e}")
        artisans = []
    finally:
        conn.close()
    return artisans


# UPDATE

def update_artisan(artisan_id, name, location, specialty):
    conn = create_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("UPDATE Artisans SET Name=?, Location=?, Speciality=? WHERE ArtisanID=?",
                       (name, location, specialty, artisan_id))
        conn.commit()
    except Exception as e:
        print(f"Error updating artisan: {e}")
        conn.rollback()
    finally:
        conn.close()


# DELETE

def delete_artisan(artisan_id):
    conn = create_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM Artisans WHERE ArtisanID=?",
                       (artisan_id))
        conn.commit()
    except Exception as e:
        print(f"Error deleting artisan: {e}")
        conn.rollback()
    finally:
        conn.close()
