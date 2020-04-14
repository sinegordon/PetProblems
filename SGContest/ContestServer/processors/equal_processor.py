from pymongo import MongoClient
import sys
import json
import time
import os
from datetime import datetime
from processors import BaseProcessor
import resource
from subprocess import PIPE, Popen, STDOUT, TimeoutExpired


class Processor(BaseProcessor):
    def __init__(self, name, config):
        super().__init__(name, config)
        client = MongoClient(config['mongo_host'], config['mongo_port'])
        self.db = client[config['mongo_db']]

    def process(self, message, config=None):

        if isinstance(config, dict):
            config = {**self.config, **config}
        else:
            config = self.config

        try:
            need_keys = ('id', 'mqtt_key', 'user', 'language', 'course', 'problem', 'variant', 'code')
            if not all(k in message for k in need_keys):
                return None
            # Определяем настройки тестов
            with open(f'./languages.json', 'r') as read_file:
                languages_config = json.load(read_file)
            with open(f'./{message["course"]}.json', 'r') as read_file:
                course_config = json.load(read_file)
            pr = message['problem']
            var = message['variant']
            code = message['code']
            fname = f'{message["user"]}'
            with open(fname, 'w') as write_file:
                write_file.write(message['code'])
            # Проверка тестов
            problem_type = course_config[pr]['type']
            tests = course_config[pr]['variants'][var]
            results = {}
            success_count = 0
            res_score = 0
            for test_key in tests:
                result = {'score': 0, 'test_out': ''}
                test = tests[test_key]
                test_in = test['in']
                test_out = test['out']
                test_score = test['score']
                p = Popen([languages_config[message['language']], fname], stdout=PIPE, stdin=PIPE, stderr=STDOUT)    
                try:
                    outs, errs = p.communicate(input=str.encode(test_in), timeout=30)
                    outs = outs.decode("utf-8").rstrip()
                    print(f'Test input - {test_in}')
                    print(f'Program output - {outs}')
                    print(f'Reference output - {test_out}')
                    self.log(f'Test input - {test_in}')
                    self.log(f'Program output - {outs}')
                    self.log(f'Reference output - {test_out}')
                    result['test_out'] = outs
                    if test_out == outs:
                        result['score'] = test_score
                        res_score += test_score
                        success_count += 1
                except Exception as e:
                    result['test_out'] = str(e)
                    p.kill()
                    outs, errs = p.communicate()
                results[test_key] = result
                
            collection_date = datetime.today().strftime('%Y-%m-%d')
            # Select tnx collection
            collection = self.db[f'all-({collection_date})']
            results['success_count'] = success_count
            results['res_score'] = res_score
            json_data = {'message': message, 'result': results}
            self.log(f'Save to MongoDB: {json_data}.')
            transaction_id = collection.insert_one(json_data).inserted_id
            self.log(f'MongoDB response: {transaction_id}.')
            del json_data['_id']
            return json_data
        except Exception as err:
            str_log = self.log_fmt(f'Process error: {str(err)}')
            self.log(f'Process error: {str(err)}')
            return None
