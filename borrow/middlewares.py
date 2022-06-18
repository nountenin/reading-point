from django.contrib.sessions.models import Session

from borrow.models import Borrow
from datetime import date

from borrow.views import expired_Borrow
from django.contrib.sessions.backends.db import SessionStore
new_borrows = []


class NotifBorrow:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        borrows = Borrow.objects.filter(status=1)
        for borrow in borrows:
            b = {
                'pk': borrow.pk,
                'expired_date_borrow': borrow.expired_date_borrow,
                'return_date_borrow': borrow.return_date_borrow,
                'reader': borrow.reader,
                'book': borrow.book,
                'stat': borrow.expired_date_borrow > date.today(),
                'days': (borrow.expired_date_borrow - date.today()).days
            }
            new_borrows.append(b)
        for expired in new_borrows:
            if not expired['stat']:
                if expired in expired_Borrow:
                    pass
                else:
                    expired_Borrow.append(expired)

        return response
