from django.utils.decorators import method_decorator
from django.core.exceptions import ObjectDoesNotExist
from djcelery import models as celery_models
from rest_framework.viewsets import GenericViewSet
from djcelery import models
from rest_framework.response import Response
from FasterRunner import pagination
from fastrunner import serializers
from fastrunner.utils import response
from fastrunner.utils.decorator import request_log
from fastrunner.utils.task import Task


class ScheduleView(GenericViewSet):
    """
    定时任务增删改查
    """
    queryset = models.PeriodicTask.objects
    serializer_class = serializers.PeriodicTaskSerializer
    pagination_class = pagination.MyPageNumberPagination

    @method_decorator(request_log(level='DEBUG'))
    def list(self, request):
        """
        查询项目信息
        """
        project = request.query_params.get("project")
        search = request.query_params.get("search")
        queryset = self.get_queryset().filter(description=project).order_by('-date_changed')

        if search != '':
            queryset = queryset.filter(name__contains=search)

        page_schedule = self.paginate_queryset(queryset)
        serializer = self.get_serializer(page_schedule, many=True)
        return self.get_paginated_response(serializer.data)

    @method_decorator(request_log(level='INFO'))
    def add(self, request):
        """新增定时任务{
            name: str
            crontab: str
            switch: bool
            data: [int,int]  CASE ID ORDER BY STEP
            suite_id: int
            strategy: str
            receiver: str
            copy: str
            project: int
        }
        """
        task = Task('add', **request.data)
        resp = task.add_task()
        return Response(resp)

    @method_decorator(request_log(level='INFO'))
    def update(self, request, **kwargs):
        """
        更新任务
        """
        request.data["task_id"] = kwargs['id']
        task = Task('update', **request.data)
        resp = task.update_task()
        return Response(resp)

    @method_decorator(request_log(level='INFO'))
    def delete(self, request, **kwargs):
        """删除任务
        """
        task = models.PeriodicTask.objects.get(id=kwargs["id"])
        task.enabled = False
        task.delete()
        return Response(response.TASK_DEL_SUCCESS)

    @method_decorator(request_log(level='INFO'))
    def single(self, request, **kwargs):
        """
        查询单个任务信息
        """
        try:
            task = models.PeriodicTask.objects.get(id=kwargs['id'])
        except ObjectDoesNotExist:
            return Response(response.TASK_NOT_EXISTS)

        resp = {
            'data': {
                'id': task.id,
                'name': task.name,
                'enable': task.enabled,
                'case_ids': task.args,
                'kwargs': task.kwargs,
                'crontab_id': task.crontab_id
            },
            'success': True
        }

        return Response(resp)
