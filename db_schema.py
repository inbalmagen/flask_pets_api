import psycopg2

# Database connection settings
DB_HOST = 'dpg-cr4vmr52ng1s73e8j78g-a.frankfurt-postgres.render.com'
DB_NAME = 'db_pets_k5jh'
DB_USER = 'db_pets_k5jh_user'
DB_PASS = 'EkjGLCXC10SpVN9WjQLx2iaV3NaFoucl'
DB_PORT = '5432'  # Default PostgreSQL port

def create_database_and_table():
    try:
        # Connect to the PostgreSQL server
        conn = psycopg2.connect(
            host=DB_HOST,
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASS,
            port=DB_PORT
        )
        conn.autocommit = True
        cur = conn.cursor()

        # Create the pets table
        cur.execute('''
            CREATE TABLE IF NOT EXISTS pets (
                id SERIAL PRIMARY KEY,
                name VARCHAR(100) NOT NULL,
                age INT NOT NULL,
                url TEXT NOT NULL
            );
        ''')

        # Insert initial data into the pets table
        cur.execute('''
            INSERT INTO pets (name, age, url) VALUES 
            ('Bella', 3, 'https://thumbor.forbes.com/thumbor/fit-in/900x510/https://www.forbes.com/advisor/wp-content/uploads/2023/07/top-20-small-dog-breeds.jpeg.jpg'),
            ('Charlie', 4, 'https://www.thesprucepets.com/thmb/hxWjs7evF2hP1Fb1c1HAvRi_Rw0=/2765x0/filters:no_upscale():strip_icc()/chinese-dog-breeds-4797219-hero-2a1e9c5ed2c54d00aef75b05c5db399c.jpg'),
            ('Max', 2, 'https://s3.amazonaws.com/cdn-origin-etr.akc.org/wp-content/uploads/2017/11/02151216/Afghan-Hound-standing-in-a-garden-400x267.jpg'),
            ('Luna', 5, 'https://media-cldnry.s-nbcnews.com/image/upload/t_nbcnews-fp-1200-630,f_auto,q_auto:best/rockcms/2022-08/220805-border-collie-play-mn-1100-82d2f1.jpg');
        ''')

        conn.commit()
        cur.close()
        conn.close()

        print("Table created successfully, and initial data inserted.")

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    create_database_and_table()
