from typing import Callable
from email.message import EmailMessage


CreateVerificationEmailFn = Callable[[int, str], EmailMessage]
SendEmailFn = Callable[[EmailMessage], None]