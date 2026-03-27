from typing import Callable
from email.message import EmailMessage


SendEmailFn = Callable[[EmailMessage], None]