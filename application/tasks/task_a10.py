from .check_path import ensure_local_path
import sqlite3

def calculate_ticket_sales(db_file: str, ticket_type: str, output_file: str):

    db_file_path = ensure_local_path(db_file)
    output_file_path = ensure_local_path(output_file)
    # Connect to the SQLite database
    conn = sqlite3.connect(db_file_path)
    cursor = conn.cursor()

    
    # Query to calculate total sales for the specified ticket type
    query = """
    SELECT SUM(units * price) AS total_sales
    FROM tickets
    WHERE type = ?;
    """
    
    # Execute the query
    cursor.execute(query, (ticket_type,))
    result = cursor.fetchone()
    
    # Get the total sales value
    total_sales = result[0] if result[0] is not None else 0
    
    # Write the result to the output file
    with open(output_file_path, "w") as file:
        file.write(str(total_sales))
    
    # Close the database connection
    conn.close()