from storitell.cust_comments.models import CommentWithRank
from storitell.cust_comments.forms import CommentFormNew

def get_model():
    return CommentWithRank
def get_form():
    return CommentFormNew
