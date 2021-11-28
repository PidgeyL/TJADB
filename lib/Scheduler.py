import time
import threading

from datetime import datetime, timedelta


class Job():
    def __init__(self, function, *args, **kwargs):
        self.function  = function
        self.args      = args
        self.kwargs    = kwargs
        self._last_run = None

    def run(self):
        self._last_run = datetime.now()
        self.function(*self.args, **self.kwargs)


class Scheduler():
    def __init__(self):
        # Queues
        self._daily    = []
        self._hourly   = []
        self._minute   = []
        self._timed    = []
        # Set last-run to every trigger - 1
        self._last_run = datetime.now() - timedelta(days=1, hours=1, minutes=1)
        # Thread for timer loop
        self._running = False
        self._timeout = 5.0

    def add_daily(self, function, *args, **kwargs):
        self._daily.append( Job(function, *args, **kwargs) )

    def add_hourly(self, function, *args, **kwargs):
        self._hourly.append( Job(function, *args, **kwargs) )

    def add_minute(self, function, *args, **kwargs):
        self._minute.append( Job(function, *args, **kwargs) )

    def add_timed(self, timeout, repeat, function,*args, **kwargs):
        self._timed.append( {'repeat': repeat, 'timeout': timeout,
                             'last-run': datetime.now().timestamp(),
                             'job': Job(function, *args, **kwargs) } )

    def start(self):
        self._running = True
        self._tick()

    def stop(self):
        self._running = False

    def _tick(self):
        now = datetime.now()
        # Cron style schedules
        if now.day    != self._last_run.day:    #Day changed
            [j.run() for j in self._daily]
        if now.hour   != self._last_run.hour:   # Every hour
            [j.run() for j in self._hourly]
        if now.minute != self._last_run.minute: # Every minute
            [j.run() for j in self._minute]
        # Timeout events
        ended = []
        for event in self._timed:
            if (now.timestamp() - event['last-run']) >= event['timeout']:
                event['job'].run()
                if event['repeat'] == True:
                    event['last-run'] = now.timestamp()
                else:
                    ended.append(event)
        self._timed = [x for x in self._timed if x not in ended]
        # Continue ?
        self._last_run = now
        if self._running:
            t = threading.Timer(self._timeout, self._tick)
            t.start()
