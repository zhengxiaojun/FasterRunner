# -*- coding:utf-8 -*-
# @Author : jack-zheng
# @Time : 19/11/3 下午2:04
from django.core.exceptions import ObjectDoesNotExist
from django.utils.decorators import method_decorator
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet
from fastrunner import models, serializers

from rest_framework.response import Response
from fastrunner.utils import response
from fastrunner.utils import prepare
from fastrunner.utils.decorator import request_log
from datetime import datetime


class SuiteView(GenericViewSet):
    queryset = models.Suite.objects
    serializer_class = serializers.SuiteSerializer

    @method_decorator(request_log(level='INFO'))
    def list(self, request):
        """
        查询指定Suite列表，不包含执行顺序
        {
            "project": int,
            "node": int
        }
        """
        project = request.query_params["project"]
        search = request.query_params["search"]
        queryset = self.get_queryset().filter(project__id=project).order_by('-update_time')

        if search != '':
            queryset = queryset.filter(name__contains=search)

        pagination_query = self.paginate_queryset(queryset)
        serializer = self.get_serializer(pagination_query, many=True)

        return self.get_paginated_response(serializer.data)

    @method_decorator(request_log(level='INFO'))
    def add(self, request):
        """
        新增测试用例集
        {
            project: int,
            name: str
            length: int,
            leveltag_name:str,
            case_list: [ {case_id , case_name, step ]
        }
        """
        case_list = request.data.pop('case_list')

        # 获取 project instance
        try:
            project_id = request.data['project']
            request.data['project'] = models.Project.objects.get(id=project_id)

        except KeyError:
            return Response(response.KEY_MISS)

        except ObjectDoesNotExist:
            return Response(response.PROJECT_NOT_EXISTS)

        if models.Suite.objects.filter(name=request.data["name"], project=project_id).first():
            return Response(response.SUITE_EXISTS)

        # add suite
        models.Suite.objects.create(**request.data)

        suite = models.Suite.objects.filter(**request.data).first()

        # add case step by suite
        for case in case_list:
            kwargs = {
                "case_id": case["case_id"],
                "case_name": case["case_name"],
                "step": case["step"],
                "suite": suite
            }

            models.CaseStepInSuite.objects.create(**kwargs)

        return Response(response.SUITE_ADD_SUCCESS)

    @method_decorator(request_log(level='INFO'))
    def copy(self, request, **kwargs):
        """
        suite_id int
        {
            name: new suite name
            suite_id: id
        }
        """
        suite_id = kwargs['id']
        name = request.data['name']
        suite = models.Suite.objects.get(id=suite_id)
        suite.id = None
        suite.name = name
        suite.save()

        case_step = models.CaseStepInSuite.objects.filter(suite_id=suite_id)

        for step in case_step:
            step.id = None
            step.suite = suite
            step.save()

        return Response(response.SUITE_ADD_SUCCESS)

    @method_decorator(request_log(level='INFO'))
    def update(self, request, **kwargs):
        """
        更新测试用例集
        {
            project: int
            name: str
            ﻿leveltag_name: int
            case_list: [new_case_list]
        }
        """

        suite_id = kwargs['id']
        case_list = request.data.pop("case_list")
        request.data['update_time'] = datetime.now()

        models.Suite.objects.filter(id=suite_id).update(**request.data)

        suite = models.Suite.objects.get(id=suite_id)

        # delete old case step by suite
        old_step_list_ids = list(models.CaseStepInSuite.objects.filter(suite=suite).values('id'))
        for content in old_step_list_ids:
            models.CaseStepInSuite.objects.filter(id=content['id']).delete()

        # add new case step by suite
        for case in case_list:
            kwargs = {
                "case_id": case["case_id"],
                "case_name": case["case_name"],
                "step": case["step"],
                "suite": suite
            }

            models.CaseStepInSuite.objects.create(**kwargs)

        return Response(response.SUITE_UPDATE_SUCCESS)

    @method_decorator(request_log(level='INFO'))
    def delete(self, request, **kwargs):
        """
        pk: test id delete single
        [{id:int}] delete batch
        """
        id = kwargs.get('id')

        try:
            if id:
                prepare.delete_suite_and_case_step(id)
            else:
                for content in request.data:
                    prepare.delete_suite_and_case_step(content['id'])

        except ObjectDoesNotExist:
            return Response(response.SYSTEM_ERROR)

        return Response(response.SUITE_DEL_SUCCESS)

    @method_decorator(request_log(level='INFO'))
    def single(self, request, **kwargs):
        """
        查询一条记录
        { id: id}
        """
        try:
            id = kwargs['id']
            suite = models.Suite.objects.get(id=id)
        except ObjectDoesNotExist:
            return Response(response.SUITE_NOT_EXISTS)

        case_list = []
        case_step = models.CaseStepInSuite.objects.filter(suite_id=id)
        for step in case_step:
            case_list.append({
                'case_id': step.case_id,
                'case_name': step.case_name,
                'step': step.step,
            })

        resp = {
            'data': {
                'id': suite.id,
                'name': suite.name,
                'leveltag_name': suite.leveltag_name,
                'case_list': case_list
            },
            'success': True
        }

        return Response(resp)
