# message syntax constants

# Header fields
HEADER_REQUEST = 'request'
HEADER_FILE_TYPE = 'file_type'
HEADER_TOKEN = 'token'
HEADER_CONTENT_LENGTH = 'content-length'
HEADER_FILE_EXTENSION = 'file_extension'

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
REQUEST_FILE_UPLOADED = 'file_uploaded'             # server tells client that a file is uploaded
REQUEST_ERROR = 'error'                             # any error that happens on server side
REQUEST_MESSAGE_STORED = 'message_stored'           # server tells client that his message was stored but not yet sent

# Body fields
BODY_TO_ID = 'to_id'
BODY_MESSAGE_ID = 'message_id'
BODY_MESSAGE_TEXT = 'message_text'
BODY_MEDIA_ID = 'media_id'
BODY_MESSAGES_IDS = 'messages_ids'
BODY_ERROR_FIELD = 'error_message'
BODY_MESSAGES = 'messages'
BODY_USER_ID = 'user_id'
BODY_RECEIVED_MESSAGES = 'received_messages'
BODY_READ_MESSAGES = 'read_messages'



# Firebase fields
FB_MESSAGE_TYPE = 'type'
FB_TYPE_NEW_FRIEND_REQUEST = 'new_request'
FB_TYPE_ACCEPTED_FRIEND_REQUEST = 'request_accepted'
FB_TYPE_NEW_MESSAGES = 'new_messages'
FB_USER_NAME = 'user_name'