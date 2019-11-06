# -*- coding:utf-8 -*-
# @Author : jack-zheng
# @Time : 19/10/31 上午11:11
from django.core.exceptions import ObjectDoesNotExist
from django.utils.decorators import method_decorator
from rest_framework.viewsets import GenericViewSet
from fastrunner import models, serializers
from rest_framework.response import Response
from fastrunner.utils import response
from fastrunner.utils.decorator import request_log
from datetime import datetime


class LevelTagView(GenericViewSet):
    """
    层级关系操作视图
    """
    serializer_class = serializers.LevelTagSerializer
    queryset = models.LevelTag.objects

    @method_decorator(request_log(level='DEBUG'))
    def list(self, request):
        """
            {
                project: int,
                search: str
            }
        """
        project = request.query_params['project']
        search = request.query_params["search"]
        ltype = request.query_params["ltype"]

        queryset = self.get_queryset().filter(project__id=project).order_by('-update_time')

        if search != '':
            queryset = queryset.filter(name__contains=search)

        if ltype != '':
            queryset = queryset.filter(ltype=ltype)

        pagination_queryset = self.paginate_queryset(queryset)
        serializer = self.get_serializer(pagination_queryset, many=True)

        return self.get_paginated_response(serializer.data)

    @method_decorator(request_log(level='DEBUG'))
    def list_parentID(self, request):
        """
            {
                project: int,
                level: int,
                search: str
            }
        """
        project = request.query_params['project']
        level = '1' if request.query_params['level'] == '2' else '2'

        queryset = self.get_queryset().filter(project__id=project, level=level)
        serializer = self.get_serializer(queryset, many=True)

        return Response(serializer.data)

    @method_decorator(request_log(level='INFO'))
    def add(self, request):
        """
            {
                project: int
                name: str
                level: int
                parentID: int
                ltype: int
            }
        """
        try:
            project = models.Project.objects.get(id=request.data["project"])
        except ObjectDoesNotExist:
            return Response(response.PROJECT_NOT_EXISTS)

        if models.LevelTag.objects.filter(name=request.data["name"], project=project).first():
            return Response(response.LEVELTAG_EXISTS)

        request.data["project"] = project

        models.LevelTag.objects.create(**request.data)
        return Response(response.LEVELTAG_ADD_SUCCESS)

    @method_decorator(request_log(level='INFO'))
    def update(self, request, **kwargs):
        """
            {
                project: int
                name: str
                level: int
                parentName: str
                ltype: int
            }
        """
        pk = kwargs['pk']

        try:
            leveltag = models.LevelTag.objects.get(id=pk)

        except ObjectDoesNotExist:
            return Response(response.LEVELTAG_NOT_EXISTS)

        if models.LevelTag.objects.exclude(id=pk).filter(name=request.data['name']).first():
            return Response(response.LEVELTAG_EXISTS)

        leveltag.name = request.data["name"]
        leveltag.level = request.data["level"]
        leveltag.parentName = request.data["parentName"]
        leveltag.ltype = request.data["ltype"]
        leveltag.update_time = datetime.now()
        leveltag.save()

        return Response(response.LEVELTAG_UPDATE_SUCCESS)

    @method_decorator(request_log(level='INFO'))
    def delete(self, request, **kwargs):
        """
            删除一个接口 pk
            删除多个 [{ id:int }]
        """
        try:
            if kwargs.get('pk'):  # 单个删除
                models.LevelTag.objects.get(id=kwargs['pk']).delete()
            else:
                for content in request.data:
                    models.LevelTag.objects.get(id=content['id']).delete()

        except ObjectDoesNotExist:
            return Response(response.LEVELTAG_NOT_EXISTS)

        return Response(response.LEVELTAG_DEL_SUCCESS)

    @method_decorator(request_log(level='INFO'))
    def single(self, request, **kwargs):
        """
        查询一条记录
        """
        try:
            leveltag = models.LevelTag.objects.get(id=kwargs['pk'])
        except ObjectDoesNotExist:
            return Response(response.LEVELTAG_NOT_EXISTS)

        resp = {
            'data': {
                'id': leveltag.id,
                'name': leveltag.name,
                'level': str(leveltag.level),
                'parentName': leveltag.parentName,
                'ltype': str(leveltag.ltype),

            },
            'success': True
        }

        return Response(resp)
