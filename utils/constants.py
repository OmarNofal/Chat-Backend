# message syntax constants

# Header fields
HEADER_REQUEST = 'request'
HEADER_FILE_TYPE = 'file_type'
HEADER_TOKEN = 'token'
HEADER_CONTENT_LENGTH = 'content-length'

# Request field values
REQUEST_MESSAGE_SEND = 'send_message'               # client wants to send a message
REQUEST_MESSAGE_RECEIVE = 'receive_message'         # server sends a message to the client
REQUEST_MESSAGE_DELETE = 'delete_message'           # client wants to delete a message
REQUEST_MESSAGES_READ = 'messages_read'             # client read messages
REQUEST_UPLOAD_FILE = 'upload_file'                 # client is uploading a file
REQUEST_DOWNLOAD_FILE = 'download_file'             # client wants to download a file
REQUEST_POLL_MESSAGES = 'poll_messages'             # client asks for messages sent to him
REQUEST_PENDING_MESSAGES = 'pending_messages'       # server tells client that he has messages to be delieverd to him (client must ask for them using REQUEST_POLL_MESSAGES)
REQUEST_MESSAGES_RECEIVED = 'message_received'      # client receievd messages

# Body fields
BODY_TO_ID = 'to_id'
BODY_MESSAGE_ID = 'message_id'
BODY_MESSAGE_TEXT = 'message_text'
BODY_MEDIA_ID = 'media_id'
BODY_MESSAGES_IDS = 'messages_ids'