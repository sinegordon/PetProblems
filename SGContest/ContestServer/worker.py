import logging
import json
import time
import importlib.util

from pathlib import Path
from multiprocessing import Process, Queue, current_process, Manager
from typing import Dict, Any, Type, Optional

from dispatcher import Dispatcher
from processors import BaseProcessor

logging.basicConfig(level=logging.DEBUG)


def start_worker(**kwargs):
    worker = Worker(**kwargs)
    worker._run()


class WorkerHandle:
    '''It runs worker in another process and communicate with it using service and data queues'''

    def __init__(self, config: Dict[Any, Any], queue: Queue):
        self.queue = queue
        self.service_queue : Queue = Queue()
        self.process_handle : Optional[Process] = None
        self.results : Dict[str, Any] = Manager().dict()
        self._config = config  # config on-the-fly update is not supported, so it's private

    def start(self):
        if self.process_handle is not None:
            raise Exception('Worker is already running')
            return
        kwargs = {'config': self._config, 'queue': self.queue, 'service_queue': self.service_queue, 'results': self.results}
        self.process_handle = Process(target=start_worker, kwargs=kwargs)
        return self.process_handle.start()

    def terminate(self):
        if self.process_handle is not None:
            self.process_handle.terminate()
            self.process_handle = None

    def kill(self):
        if self.process_handle is not None:
            self.process_handle.kill()
            self.process_handle = None


Processor = Type[BaseProcessor]
Config = Dict[Any, Any]

class Worker(Dispatcher):
    def __init__(self, config: Dict[Any, Any], queue: Queue, service_queue: Queue, results: Dict[str, Any]):
        self.queue = queue
        self.service_queue = service_queue
        self.results = results
        self.config = config
        self.processors_root = Path(config['processors_root'])
        self.processors : Dict[str, Processor] = {}
        for name, cfg in config['processors'].items():
            self.add_processor(name, cfg)
    
    def is_dispatchable(self, method: str) -> bool:
        return not method.startswith('_')

    def _load_processor(self, name: str, config: Config) -> Optional[Processor]:
        try:
            location = self.processors_root / (config['type'] + '.py')
            module_spec = importlib.util.spec_from_file_location(f'processors.{name}', location)
            module = importlib.util.module_from_spec(module_spec)
            module_spec.loader.exec_module(module)
            processor = module.Processor(name, config)
            logging.debug(f'{name} successfully loaded with configuration: {config}')
            return processor
        except Exception as err:
            logging.debug(f'{name} is failed to load: {err}')
        return None

    def _run(self) -> None:
        while True:
            try:
                message = None
                for q in [self.service_queue, self.queue]:
                    if not q.empty():
                        message = json.loads(q.get())
                        break
                if message is None:
                    time.sleep(1)
                    continue

                self.dispatch(**message)

            except Exception as err:
                print(str(err))

    def process_transaction(self, transaction: Dict[str, Any]) -> None:
        timeout = 60
        pid = current_process().pid
        str_out = f'PID = {pid}. Got transaction - {transaction}'
        print(str_out)
        transaction['timestamp'] = int(time.time())
        for name, p in self.processors.items():
            try:
                res = p.process(transaction, self.config)
                if not res is None:
                    self.results[res['message']['id']] = res
            except Exception as err:
                print(p.name, err)


    def get_processors_list(self) -> None:
        pass

    def add_processor(self, name: str, cfg: Config) -> None:
        # str_out = 'PID = {pid}. Get from self.service_queue - {cmd_str}'.format(pid=pid, cmd_str=cmd_str)
        # print(str_out)
        cfg.setdefault('service', self.config.get('service'))
        p = self._load_processor(name, cfg)
        if p is not None:
            self.processors[name] = p
        # str_out = 'PID = {pid}. Module {f} was added.'.format(pid=pid, f=cmd_mas['name'])
        # print(str_out)

    def del_processor(self, name: str) -> None:
        # str_out = 'PID = {pid}. Get from self.service_queue - {cmd_str}'.format(pid=pid, cmd_str=cmd_str)
        # print(str_out)
        if name in self.processors:
            self.processors.pop(name)
        # str_out = 'PID = {pid}. Module {f} was removed.'.format(pid=pid, f=cmd_mas['name'])
        # print(str_out)
