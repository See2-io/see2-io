# Django modules
from django.db import models
from django.contrib.auth.models import User

# See2-io modules


# See2-io Core models.
class AbstractActor(models.Model):
    '''
    Simple Abstract model for Actors in See2.
    For now, it uses an enumeration pattern to designate actor type as one-of person, organisation or bot.
    '''
    name = models.CharField(max_length=32,)
    ORG = 'ORG'
    PER = 'PER'
    BOT = 'BOT'
    ACTOR_TYPES = (
        (ORG, 'Organisation'),
        (PER, 'Person'),
        (BOT, 'Robot'),
    )
    type = models.CharField(
        max_length=3,
        choices=ACTOR_TYPES,
        default=PER,
    )
    email = models.EmailField('Email Address', null=True, blank=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True,)

    def is_user(self):
        return not self.user == None

    def actor_type(self):
        return self.type

    class Meta:
        abstract = True


class Actor(AbstractActor):
    '''
    TODO: Dummy parent class because I don't seem to understand how to usefully use Django abstract classes.
    '''
    def __init__(self, *args, **kwargs):
        super(Actor, self).__init__(*args, **kwargs)


class Person(Actor):
    '''
    A human actor.
    '''
    first_name = models.CharField('First Name', max_length=64, null=True, blank=True)
    last_name = models.CharField('Last Name', max_length=64,)

    def __init__(self, *args, **kwargs):
        super(Person, self).__init__(*args, **kwargs)
        self.type = AbstractActor.PER


class Organisation(Actor):
    '''
    A business, charity, government or other organisation.
    '''
    def __init__(self, *args, **kwargs):
        super(Organisation, self).__init__(*args, **kwargs)
        self.type = AbstractActor.ORG


class Bot(Actor):
    '''

    '''
    def __init__(self, *args, **kwargs):
        super(Bot, self).__init__(*args, **kwargs)
        self.type = AbstractActor.BOT

