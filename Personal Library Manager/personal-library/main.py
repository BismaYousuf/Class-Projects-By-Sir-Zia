import streamlit as st
import sqlite3
import os
import pandas as pd

# Database file
DB_FILE = os.path.join(os.path.dirname(__file__), "library.db")

# Initialize database
def initialize_database():
    """Create the database and tables if they don't exist."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    # Create books table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS books (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        author TEXT NOT NULL,
        year INTEGER NOT NULL,
        genre TEXT NOT NULL,
        read BOOLEAN NOT NULL
    )
    ''')
    
    conn.commit()
    conn.close()

# Database operations
def execute_query(query, parameters=(), fetchall=False):
    """Execute a database query with error handling."""
    try:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute(query, parameters)
        
        result = None
        if fetchall:
            result = cursor.fetchall()
        else:
            conn.commit()
            result = cursor.lastrowid
            
        cursor.close()
        conn.close()
        return result
    except sqlite3.Error as e:
        st.error(f"Database error: {e}")
        return None

def add_book_to_db(title, author, year, genre, read_status):
    """Add a book to the database."""
    query = '''
    INSERT INTO books (title, author, year, genre, read)
    VALUES (?, ?, ?, ?, ?)
    '''
    parameters = (title, author, year, genre, read_status)
    
    book_id = execute_query(query, parameters)
    return book_id is not None

def get_all_books():
    """Get all books from the database."""
    query = "SELECT id, title, author, year, genre, read FROM books ORDER BY title"
    books_data = execute_query(query, fetchall=True)
    
    if not books_data:
        return []
    
    # Convert to list of dictionaries
    books = []
    for book in books_data:
        books.append({
            "id": book[0],
            "title": book[1],
            "author": book[2],
            "year": book[3],
            "genre": book[4],
            "read": bool(book[5])
        })
    
    return books

def search_books(search_type, search_query):
    """Search for books in the database."""
    if search_type == "Title":
        query = "SELECT id, title, author, year, genre, read FROM books WHERE LOWER(title) LIKE ? ORDER BY title"
    else:  # Author
        query = "SELECT id, title, author, year, genre, read FROM books WHERE LOWER(author) LIKE ? ORDER BY author"
    
    parameters = (f"%{search_query.lower()}%",)
    books_data = execute_query(query, parameters, fetchall=True)
    
    if not books_data:
        return []
    
    # Convert to list of dictionaries
    books = []
    for book in books_data:
        books.append({
            "id": book[0],
            "title": book[1],
            "author": book[2],
            "year": book[3],
            "genre": book[4],
            "read": bool(book[5])
        })
    
    return books

def delete_book(book_id):
    """Delete a book from the database."""
    query = "DELETE FROM books WHERE id = ?"
    parameters = (book_id,)
    
    result = execute_query(query, parameters)
    return result is not None

def get_statistics():
    """Get library statistics from the database."""
    # Total books
    total_query = "SELECT COUNT(*) FROM books"
    total_result = execute_query(total_query, fetchall=True)
    total_books = total_result[0][0] if total_result else 0
    
    # Read books
    read_query = "SELECT COUNT(*) FROM books WHERE read = 1"
    read_result = execute_query(read_query, fetchall=True)
    read_books = read_result[0][0] if read_result else 0
    
    # Calculate percentage
    if total_books > 0:
        read_percentage = (read_books / total_books) * 100
    else:
        read_percentage = 0
    
    # Top genres
    genre_query = """
    SELECT genre, COUNT(*) as count 
    FROM books 
    GROUP BY genre 
    ORDER BY count DESC 
    LIMIT 5
    """
    genres_data = execute_query(genre_query, fetchall=True)
    genres = {genre: count for genre, count in genres_data} if genres_data else {}
    
    # Top authors
    author_query = """
    SELECT author, COUNT(*) as count 
    FROM books 
    GROUP BY author 
    ORDER BY count DESC 
    LIMIT 5
    """
    authors_data = execute_query(author_query, fetchall=True)
    authors = {author: count for author, count in authors_data} if authors_data else {}
    
    # Books by decade
    decade_query = """
    SELECT (year / 10) * 10 as decade, COUNT(*) as count 
    FROM books 
    GROUP BY decade 
    ORDER BY decade
    """
    decades_data = execute_query(decade_query, fetchall=True)
    decades = {f"{decade}s": count for decade, count in decades_data} if decades_data else {}
    
    return {
        "total_books": total_books,
        "read_books": read_books,
        "read_percentage": read_percentage,
        "genres": genres,
        "authors": authors,
        "decades": decades
    }

# Initialize database
initialize_database()

# Streamlit UI
st.set_page_config(page_title="Personal Library Manager", page_icon="📚", layout="wide")

st.title("📚 Personal Library Manager")

# Sidebar Menu
menu = st.sidebar.radio("📌 Menu", ["📖 Add Book", "🔍 Search Books", "📚 View Library", "📊 Statistics"])

# Add a Book
if menu == "📖 Add Book":
    st.header("📖 Add a New Book")

    with st.form("add_book_form"):
        title = st.text_input("📚 Book Title", placeholder="Enter the book title")
        author = st.text_input("✍️ Author", placeholder="Enter the author's name")
        year = st.number_input("📅 Publication Year", min_value=2000, max_value=2100, step=1)
        genre = st.text_input("🎭 Genre", placeholder="Enter book genre")
        read_status = st.radio("📖 Have you read this book?", ["Yes", "No"])

        submitted = st.form_submit_button("➕ Add Book")

        if submitted:
            if title and author and genre:
                # Add to database
                success = add_book_to_db(
                    title.strip(),
                    author.strip(),
                    int(year),
                    genre.strip(),
                    read_status == "Yes"
                )
                
                if success:
                    st.success("✅ Book added successfully to database!")
                else:
                    st.error("❌ Failed to add book to database.")
            else:
                st.error("⚠️ Please fill in all fields!")

# Search Books
elif menu == "🔍 Search Books":
    st.header("🔍 Search for a Book")

    search_type = st.radio("Search by:", ["Title", "Author"])
    search_query = st.text_input("🔎 Enter your search term", placeholder="Type here...")

    if search_query:
        results = search_books(search_type, search_query)

        if results:
            st.write(f"✅ Found {len(results)} matching books:")
            
            # Convert to DataFrame for better display
            df = pd.DataFrame(results)
            
            # Add delete button for each book
            for i, book in enumerate(results):
                col1, col2 = st.columns([5, 1])
                with col1:
                    st.write(f"**{book['title']}** by {book['author']} ({book['year']}) - {book['genre']} - {'Read' if book['read'] else 'Unread'}")
                with col2:
                    if st.button(f"🗑️ Delete", key=f"delete_{book['id']}"):
                        if delete_book(book['id']):
                            st.success(f"✅ Deleted '{book['title']}'")
                            st.rerun()
                        else:
                            st.error("❌ Failed to delete book.")
                st.divider()
        else:
            st.warning("❌ No books found with that search term.")

# View All Books
elif menu == "📚 View Library":
    st.header("📚 Your Library")

    # Get all books from database
    library = get_all_books()

    if library:
        # Create tabs for different views
        tab1, tab2 = st.tabs(["Table View", "Card View"])
        
        with tab1:
            # Convert to DataFrame for table display
            df = pd.DataFrame(library)
            # Rename columns for display
            df = df.rename(columns={
                "id": "ID",
                "title": "Title",
                "author": "Author",
                "year": "Year",
                "genre": "Genre",
                "read": "Read"
            })
            # Replace boolean with Yes/No
            df["Read"] = df["Read"].map({True: "Yes", False: "No"})
            # Display as table
            st.dataframe(df.drop(columns=["ID"]), use_container_width=True)
        
        with tab2:
            # Display as cards with delete buttons
            cols = st.columns(3)
            for i, book in enumerate(library):
                with cols[i % 3]:
                    with st.container(border=True):
                        st.subheader(book["title"])
                        st.write(f"**Author:** {book['author']}")
                        st.write(f"**Year:** {book['year']}")
                        st.write(f"**Genre:** {book['genre']}")
                        st.write(f"**Status:** {'Read ✅' if book['read'] else 'Unread ❌'}")
                        
                        if st.button(f"🗑️ Delete", key=f"delete_card_{book['id']}"):
                            if delete_book(book['id']):
                                st.success(f"✅ Deleted '{book['title']}'")
                                st.rerun()
                            else:
                                st.error("❌ Failed to delete book.")
    else:
        st.warning("⚠️ Your library is empty. Add books first!")

# Display Statistics
elif menu == "📊 Statistics":
    st.header("📊 Library Statistics")

    # Get statistics from database
    stats = get_statistics()
    
    # Display basic stats
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("📚 Total Books", stats["total_books"])
    with col2:
        st.metric("📖 Books Read", stats["read_books"])
    with col3:
        st.metric("📊 Read Percentage", f"{stats['read_percentage']:.1f}%")
    
    # Display charts if there are books
    if stats["total_books"] > 0:
        # Create tabs for different charts
        tab1, tab2, tab3 = st.tabs(["Genres", "Authors", "Decades"])
        
        with tab1:
            st.subheader("📊 Books by Genre")
            if stats["genres"]:
                # Create bar chart for genres
                genre_df = pd.DataFrame({
                    "Genre": list(stats["genres"].keys()),
                    "Count": list(stats["genres"].values())
                })
                st.bar_chart(genre_df.set_index("Genre"))
            else:
                st.info("No genre data available.")
        
        with tab2:
            st.subheader("✍️ Books by Author")
            if stats["authors"]:
                # Create bar chart for authors
                author_df = pd.DataFrame({
                    "Author": list(stats["authors"].keys()),
                    "Count": list(stats["authors"].values())
                })
                st.bar_chart(author_df.set_index("Author"))
            else:
                st.info("No author data available.")
        
        with tab3:
            st.subheader("📅 Books by Decade")
            if stats["decades"]:
                # Create bar chart for decades
                decade_df = pd.DataFrame({
                    "Decade": list(stats["decades"].keys()),
                    "Count": list(stats["decades"].values())
                })
                st.bar_chart(decade_df.set_index("Decade"))
            else:
                st.info("No decade data available.")
    
# Footer
st.sidebar.write("---")
st.sidebar.write("📌 **Developed with ❤️ Bisma Yousuf**")

# Add database backup option in sidebar
st.sidebar.write("---")
st.sidebar.subheader("Database Management")

if st.sidebar.button("📦 Backup Database"):
    import shutil
    from datetime import datetime
    
    backup_dir = "backups"
    if not os.path.exists(backup_dir):
        os.makedirs(backup_dir)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_file = f"{backup_dir}/library_backup_{timestamp}.db"
    
    try:
        shutil.copy2(DB_FILE, backup_file)
        st.sidebar.success(f"✅ Database backed up to {backup_file}")
    except Exception as e:
        st.sidebar.error(f"❌ Backup failed: {e}")

# Add import/export options
if st.sidebar.button("📤 Export to JSON"):
    import json
    
    library = get_all_books()
    
    # Remove ID field for export
    for book in library:
        book.pop("id", None)
    
    try:
        export_file = "library_export.json"
        with open(export_file, "w") as f:
            json.dump(library, f, indent=4)
        st.sidebar.success(f"✅ Exported {len(library)} books to {export_file}")
    except Exception as e:
        st.sidebar.error(f"❌ Export failed: {e}")