# Add Django imports here
from django.core.management.base import BaseCommand, CommandError

# Add third party imports here
import simpy
import time

# Add local imports here
from sense._exceptions import NotFound
from sense.enron_emails.events import send_emails, process_users
# from sense.enron_emails.events import send_emails_by_freq


class Command(BaseCommand):
    help = 'Runs the specified simulation.'

    def add_arguments(self, parser):
        parser.add_argument('sim_file', nargs='+', type=str)

    def handle(self, *args, **options):
        for sim_file in options['sim_file']:
            try:
                env = simpy.Environment()
                # email_by_freq_gen = send_emails_by_freq(env, 'W')
                # process = simpy.events.Process(env, email_by_freq_gen)
                users_gen = process_users(env)
                p1 = simpy.events.Process(env, users_gen)
                emails_gen = send_emails(env)
                p2 = simpy.events.Process(env, emails_gen)
                # env.run()
                for i in range(99, 251299, 100):
                    env.run(until=i)
                    print('Sleeping Enron simulation.')
                    time.sleep(0.1)
            except NotFound:
                raise CommandError('Sim "%s" not found' % sim_file)

            self.stdout.write(self.style.SUCCESS('Successfully found "%s"' % sim_file))

    def config_env(self,env):
        '''
        Configure the simulation environment 'env'.
        :param env:
        :return:
        '''
        pass


# class Server(object):
#     '''
#     This class represents the propagation of emails through a server
#     '''
#     def __init__(self, env, delay):
#         self.env = env
#         self.delay = delay
#         self.store = simpy.Store(env)
#
#     def latency(self, value):
#         yield self.env.timeout(self.delay)
#         self.store.put(value)
#
#     def send(self, value):
#         self.env.process(self.latency(value))
#
#     def fetch(self):
#         return self.store.get()
