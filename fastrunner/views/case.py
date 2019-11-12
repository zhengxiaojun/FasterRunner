from django.core.exceptions import ObjectDoesNotExist
from django.utils.decorators import method_decorator
from rest_framework.viewsets import GenericViewSet
from fastrunner import models, serializers
from rest_framework.response import Response
from fastrunner.utils import response
from fastrunner.utils import prepare
from fastrunner.utils.decorator import request_log
from fastrunner.utils.parser import Format, Parse
from fastrunner.utils.filehandle import FileParse
from django.db import DataError
from datetime import datetime


class CaseTemplateView(GenericViewSet):
    """
    Case 操作视图
    """
    serializer_class = serializers.CaseSerializer
    queryset = models.Case.objects

    @method_decorator(request_log(level='DEBUG'))
    def list(self, request):
        """
         用例列表 {
            project: int,
            node: int
        }
        """
        project = request.query_params["project"]
        search = request.query_params["search"]
        need_page = request.query_params["need_page"]

        queryset = self.get_queryset().filter(project__id=project).order_by('-update_time')

        if search != '':
            queryset = queryset.filter(name__contains=search)

        if need_page == 'true':
            pagination_queryset = self.paginate_queryset(queryset)
            serializer = self.get_serializer(pagination_queryset, many=True)
            return self.get_paginated_response(serializer.data)
        else:
            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data)

    @method_decorator(request_log(level='INFO'))
    def add(self, request):
        """
        新增一个用例
        """

        case = Format(request.data)
        case.parse()

        case_body = {
            'name': case.name,
            'body': case.testcase,
            'url': case.url,
            'method': case.method,
            'project': models.Project.objects.get(id=case.project),
            'leveltag_name': case.leveltag_name
        }

        try:
            models.Case.objects.create(**case_body)
        except DataError:
            return Response(response.DATA_TO_LONG)

        return Response(response.CASE_ADD_SUCCESS)

    @method_decorator(request_log(level='INFO'))
    def update(self, request, **kwargs):
        """
        更新用例
        """
        pk = kwargs['pk']
        case = Format(request.data)
        case.parse()

        case_body = {
            'name': case.name,
            'body': case.testcase,
            'url': case.url,
            'method': case.method,
            'leveltag_name': case.leveltag_name,
            'update_time': datetime.now()
        }

        try:
            models.Case.objects.filter(id=pk).update(**case_body)
        except ObjectDoesNotExist:
            return Response(response.CASE_NOT_EXISTS)

        return Response(response.CASE_UPDATE_SUCCESS)

    @method_decorator(request_log(level='INFO'))
    def copy(self, request, **kwargs):
        """
        复制用例
        pk int: test id
        {
            name: case name
        }
        """
        pk = kwargs['pk']
        name = request.data['name']
        case = models.Case.objects.get(id=pk)
        body = eval(case.body)
        body["name"] = name
        case.body = body
        case.id = None
        case.name = name
        case.save()
        return Response(response.CASE_ADD_SUCCESS)

    @method_decorator(request_log(level='INFO'))
    def delete(self, request, **kwargs):
        """
        删除一个用例 pk
        删除多个
        [{
            id:int
        }]
        """

        try:
            pk = kwargs.get('pk')
            if pk:  # 单个删除
                if prepare.caseInSuite(pk):
                    return Response(response.CASE_IN_SUITE)
                models.Case.objects.get(id=pk).delete()
                return Response(response.CASE_DELETE_SUCCESS)
            else:
                exist = False
                for content in request.data:
                    if prepare.caseInSuite(content["id"]):
                        exist = True
                        break
                    models.Case.objects.get(id=content['id']).delete()
                if exist:
                    return Response(response.CASE_IN_SUITE)
                else:
                    return Response(response.CASE_DELETE_SUCCESS)

        except ObjectDoesNotExist:
            return Response(response.CASE_NOT_EXISTS)

    @method_decorator(request_log(level='INFO'))
    def single(self, request, **kwargs):
        """
        查询单个用例，返回body信息
        """
        try:
            case = models.Case.objects.get(id=kwargs['pk'])
        except ObjectDoesNotExist:
            return Response(response.CASE_NOT_EXISTS)

        parse = Parse(eval(case.body))
        parse.parse_http()

        resp = {
            'id': case.id,
            'body': parse.testcase,
            'success': True,
        }

        return Response(resp)

    @method_decorator(request_log(level='INFO'))
    def case_import(self, request):
        """
        用例导入
        {
            filetype: 1 - json , 2 -excel
            leveltagName
            filename
        }
        """
        filetype = request.data['filetype']
        filename = request.data['filename']
        project = request.data['project']
        leveltagName = request.data['leveltagName']
        parse = FileParse(filetype, filename, leveltagName)
        test_cases = parse.parsePostmanJson()

        for test_case in test_cases:
            case = models.Case.objects.filter(name=test_case["name"])
            if case:
                test_case["name"] = test_case["name"] + leveltagName

            case_body = {
                'name': test_case["name"],
                'body': test_case["body"],
                'url': test_case["url"],
                'method': test_case["method"],
                'project': models.Project.objects.get(id=project),
                'leveltag_name': leveltagName
            }

            try:
                models.Case.objects.create(**case_body)
            except DataError:
                return Response(response.DATA_TO_LONG)

        if test_cases:
            return Response(response.CASE_UPLOAD_SUCCESS)

        return Response(response.CASE_UPLOAD_FAIL)
