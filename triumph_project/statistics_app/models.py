from django.db import models
from triumph_app.models import Challenge

# Create your models here.



class Session(models.Model):
    student = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    session_start_at = models.DateTimeField()
    session_end_at = models.DateTimeField()

    def __str__(self):
        return str(self.student.username + '; '
                   + self.session_start_at.day.__str__() + '.'
                   + self.session_start_at.month.__str__() + '.'
                   + self.session_start_at.year.__str__() + 'at:  '
                   + self.session_start_at.hour.__str__() + '.'
                   + self.session_start_at.minute.__str__() + ';  '
                   + self.session_end_at.day.__str__() + '.'
                   + self.session_end_at.month.__str__() + '.'
                   + self.session_end_at.year.__str__() + 'at:  '
                   + self.session_end_at.hour.__str__() + '.'
                   + self.session_end_at.minute.__str__() + '.')


class StudentAnswer(models.Model):
    session = models.ForeignKey(Session, on_delete=models.CASCADE)
    challenge = models.ForeignKey(Challenge, on_delete=models.CASCADE)
    is_Right_Answer = models.BooleanField()

    def __str__(self):
        return str(self.session.__str__() + '; ' + self.challenge.__str__() + '; ' + self.is_Right_Answer.__str__())
