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
        self.cases = []  # 待解析
        self.test_cases = []  # 已解析

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

        if 'query' in case["request"]["url"]:
            for param in case["request"]["url"]["query"]:
                params[param["key"]] = param["value"]
                if 'description' in param:
                    desc_params[param["key"]] = param["description"]
                else:
                    desc_params[param["key"]] = ''

        return params, desc_params

    def parseHeaders(self, case):
        """
        :param case:
        :return: dict
        """
        headers = {}
        desc_headers = {}

        if 'header' in case["request"]:
            for hd in case["request"]["header"]:
                headers[hd["key"]] = hd["value"]
                if 'description' in hd:
                    desc_headers[hd["key"]] = hd["description"]
                else:
                    desc_headers[hd["key"]] = ''

        return headers, desc_headers

    def parseFormData(self, case):
        """
        :param case:
        :return: dict
        """
        formdatas = {}
        desc_formdatas = {}

        if 'body' in case["request"] and case["request"]["body"]["mode"] == "formdata":
            for bd in case["request"]["body"]["formdata"]:
                formdatas[bd["key"]] = bd["value"]
                if 'description' in bd:
                    desc_formdatas[bd["key"]] = bd["description"]
                else:
                    desc_formdatas[bd["key"]] = ''

        return formdatas, desc_formdatas

    def parseRawJson(self, case):
        """
        :param case:
        :return: dict
        """
        rawjson = {}

        if 'body' in case["request"] and case["request"]["body"]["mode"] == "raw":
            try:
                rawjson = json.loads(case["request"]["body"]["raw"])
            except Exception as e:
                print(e)
                rawjson = {}
                # if 'options' in case["request"]["body"]:
                #     if case["request"]["body"]["options"]["raw"]["language"] == 'json':
                #         rawjson = json.loads(case["request"]["body"]["raw"])

        return rawjson

    def parseBody(self, case, leveltagName):
        params, desc_params = self.parseParams(case)
        headers, desc_headers = self.parseHeaders(case)
        formdatas, desc_formdatas = self.parseFormData(case)
        rawjson = self.parseRawJson(case)

        body = {
            'name': case["name"],
            'times': 1,
            'leveltag_name': leveltagName,
            'request': {
                'url': self.parseUrl(case["request"]["url"]["raw"]),
                'method': case["request"]["method"],
                'verify': False,
                'headers': headers,
                'params': params,
                'data': formdatas,
                'json': rawjson
            },
            'desc': {
                'header': desc_headers,
                'data': desc_formdatas,
                'files': {},
                'params': desc_params,
                'variables': {},
                'extract': {}
            },
            'validate': []
        }
        return body

    def add_test_case(self, case):
        try:
            test_case = {}

            test_case["name"] = case["name"]
            test_case["url"] = self.parseUrl(case["request"]["url"]["raw"])
            test_case["method"] = case["request"]["method"]
            test_case["body"] = self.parseBody(case, self.leveltagName)

            self.test_cases.append(test_case)

        except KeyError as e:
            print(e)

    def get_cases(self, data):
        if 'item' in data:
            for child_item in data['item']:
                self.get_cases(child_item)
        else:
            self.cases.append(data)

    def parsePostmanJson(self):
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
        if self.filetype == '1':  # json
            data = json.loads(data)

            self.get_cases(data)
            print('case length:' + str(len(self.cases)))
            for case in self.cases:
                self.add_test_case(case)

        return self.test_cases
