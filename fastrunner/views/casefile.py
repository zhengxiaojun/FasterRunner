# -*- coding:utf-8 -*-
# @Author : jack-zheng
# @Time : 19/11/5 下午1:51

from django.utils.decorators import method_decorator
from rest_framework.viewsets import GenericViewSet
from rest_framework.response import Response
from fastrunner.utils.decorator import request_log
import os
import json

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")) + "/upload/"


class FileView(GenericViewSet):
    """
    文件操作视图
    """

    @method_decorator(request_log(level='DEBUG'))
    def upload(self, request):
        print(request.FILES)
        filename = request.data['filename']
        file = request.FILES['file']

        filepath = BASE_DIR + filename

        with open(filepath, 'wb+') as f:
            for chunk in file.chunks():
                f.write(chunk)

        return Response(status=204)

    @method_decorator(request_log(level='DEBUG'))
    def download(self, request, filename, format=None):
        file_obj = request.data['file']
        # ...
        # do some stuff with uploaded file
        # ...
        return Response(status=200)


class FileParse(object):
    def __init__(self, filetype, filename, leveltagName):
        self.filetype = filetype
        self.filename = filename
        self.leveltagName = leveltagName
        self.test_cases = []

    def read(self, filename):
        with open(filename, 'r') as file:
            data = file.read()
        return data

    def parseUrl(self, raw):
        return raw.split('?')[0]

    def parseParams(self, case):
        """
        :param case:
        :return: dict
        """
        params = {}
        desc_params = {}
        print(case["request"]["url"])

        if 'query' in case["request"]["url"]:
            for param in case["request"]["url"]["query"]:
                params[param["key"]] = param["value"]
                if 'description' in param:
                    desc_params[param["key"]] = param["description"]
                else:
                    desc_params[param["key"]] = ''

        return params, desc_params

    def parseBody(self, case, leveltagName):
        params, desc_params = self.parseParams(case)

        body = {
            'name': case["name"],
            'times': 1,
            'leveltag_name': leveltagName,
            'request': {
                'url': self.parseUrl(case["request"]["url"]["raw"]),
                'method': case["request"]["method"],
                'verify': False,
                'params': params
            },
            'desc': {
                'header': {},
                'data': {},
                'files': {},
                'params': desc_params,
                'variables': {},
                'extract': {}
            },
            'validate': []
        }
        return body

    def add_test_case(self, cases):
        for case in cases:
            test_case = {}

            test_case["name"] = case["name"]
            test_case["url"] = self.parseUrl(case["request"]["url"]["raw"])
            test_case["method"] = case["request"]["method"]
            test_case["body"] = self.parseBody(case, self.leveltagName)

            self.test_cases.append(test_case)

    def parsePostmanJson(self, folder_level):
        """
        :param filetype: 1: json 2: excel
        :param filename:
        :return:
            'name': data.name,
            'body': data.testcase,
            'url': data.url,
            'method': data.method,
        """
        file = BASE_DIR + self.filename
        data = self.read(file)
        if self.filetype == '1':
            data = json.loads(data)

            if folder_level == '1':
                cases = data["item"]  # 一级目录
                self.add_test_case(cases)

            if folder_level == '2':
                for item1 in data["item"]:
                    self.add_test_case(item1["item"])  # 二级目录

        return self.test_cases
