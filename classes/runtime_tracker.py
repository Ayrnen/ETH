import datetime as dt

class RuntimeTracker:
    start_time = None

    @staticmethod
    def start():
        RuntimeTracker.start_time = dt.datetime.now()
        print(f'Start time: {RuntimeTracker.start_time}')

    @staticmethod
    def stop():
        if RuntimeTracker.start_time is None:
            raise ValueError('Tracker was not started. Call start() before stop().')
        end_time = dt.datetime.now()
        runtime = end_time - RuntimeTracker.start_time
        print(f'End time: {end_time}')
        print(f'Runtime: {runtime}')