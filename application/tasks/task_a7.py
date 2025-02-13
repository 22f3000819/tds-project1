from .check_path import ensure_local_path

def extract_email_address(email_content: str, output_file: str):
    """
    Extract the sender's email address from the email content and write it to the output file.
    Always give file path with local directory in mind for calling EG: ./data/...
    """
    # Use an LLM to extract the email address
    """
    MAKE OPENAI  API CALL TO EXTRACT INFO Or multimodal
    """ 
    # Write the extracted email address to the output file
    email_content_path = ensure_local_path(email_content)
    print(f'trying to get email content from {email_content_path}')
    with open(email_content_path, "r") as file:
        email_info = file.read() #readlines gives list, this gives string

    print('email_content_file_found')
    output_file_path = ensure_local_path(output_file)
    return email_info, output_file_path