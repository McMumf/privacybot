from postmarker.core import PostmarkClient

def create_postmark_client(api_token: str):
    return PostmarkClient(server_token = api_token)

