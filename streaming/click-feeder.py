#!/usr/bin/env python3
import sys
import time, datetime
import random
import math

random.seed(314159)
class Event:
    def __init__(self, sender, msg, at):
        self.sender = sender
        self.msg = msg
        self.at = at
    def __lt__(self, other):
        return ((self.at) < (other.at))
    def __eq__(self, other):
        return ((self.at) == (other.at))
    def __str__(self):
        return (str(self.at) + ': ' + str(self.sender) + ': ' + self.msg)

class Sender:
    msgs = []
    delay = tuple()
    def __init__(self, name, msgs, delay_mu, delay_sigma):
        self.name = name
        self.msgs  = msgs
        self.delay = (delay_mu, delay_sigma,)
    def __str__(self):
        return '%s: %s (%.3f, %.3f)' % (self.name, self.msgs, self.delay[0], self.delay[1])
    def __repr__(self):
        return '%s: %s (%.3f, %.3f)' % (self.name, self.msgs, self.delay[0], self.delay[1])
    def new_event(self):
        utcnow = datetime.datetime.utcnow()
        delta_t = random.normalvariate(self.delay[0], self.delay[1])
        next_event_time = utcnow + datetime.timedelta(seconds = delta_t)
        next_event = Event(self, random.choice(self.msgs), next_event_time)
        print('new_event', next_event)
        return next_event
    def next_delay(self):
        return random.normalvariate(self.delay[0], self.delay[1])
    def next_msg(self):
        return (random.choice(self.msgs))

alice = Sender('Alice', ('url1', 'url2', 'url3',), 16.0, 1.0)
bobby = Sender('Bobby', ('url1', 'url2', 'url3',),  8.0, 1.0)
cindy = Sender('Cindy', ('url1', 'url2', 'url3',),  4.0, 1.0)
print (alice.next_delay(), alice.next_msg(), str(alice.new_event()),)
print (bobby.next_delay(), bobby.next_msg(), str(bobby.new_event()),)
print (cindy.next_delay(), cindy.next_msg(), str(cindy.new_event()),)

class Dispatcher:
    senders = []
    out_evs = []
    def __str__(self):
        senders = 'senders = \n' + '\n'.join([str(elem) for elem in list(self.senders)])
        out_evs = 'out_evs = \n' + '\n'.join([str(elem) for elem in list(self.out_evs)])
        return '\n'.join((senders, out_evs,))
    def add_sender(self, sender):
        self.senders.append(sender)
        first_event = sender.new_event()
        print(first_event)
        self.out_evs.append(first_event)
        self.out_evs = sorted(self.out_evs)
    def repl_event(self, event_old):
        sender = event_old.sender
        new_event = sender.new_event()
        out_evs = self.out_evs[1:]
        out_evs.append(new_event)
        self.out_evs = sorted(out_evs)
        print ('replaced dispatcher event\n', event_old, '\nwith\n', new_event)
        return new_event
    def launch(self):
        times  = [str(self.out_evs[i].at) for i in range(len(self.out_evs))]
        utcnow = datetime.datetime.utcnow()
        times += [str(utcnow)]
        print('\n'.join(times))
        while True:
            utcnow = datetime.datetime.utcnow()
            if utcnow <= self.out_evs[0].at:
                # wait for the first event time
                print('first_time', [str(ev) for ev in self.out_evs])
                wait_time = self.out_evs[0].at - utcnow
                wait_secs = wait_time.total_seconds()
                print('waiting', wait_secs)
                time.sleep(math.ceil(wait_secs))
            else:
                print('resuming')
                next_event = self.repl_event(self.out_evs[0])
                print('next event', next_event)
                next_delay = next_event.sender.next_delay()
                time.sleep(math.ceil(next_delay))
                print ('yielding', next_event, flush=True)
                yield next_event


dispatcher = Dispatcher()
dispatcher.add_sender(alice)
dispatcher.add_sender(bobby)
dispatcher.add_sender(cindy)

num_events = 5
for ev in dispatcher.launch():
    num_events -= 1
    print(ev)
    if num_events <= 0:
        break

