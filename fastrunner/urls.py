"""FasterRunner URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import path
from fastrunner.views import project, config, schedule, run, case, suite, report, leveltag
from fastrunner.utils import filehandle

urlpatterns = [
    # 项目相关接口地址
    path('project/', project.ProjectView.as_view({
        "get": "list",
        "post": "add",
        "patch": "update",
        "delete": "delete"
    })),
    path('project/<int:pk>/', project.ProjectView.as_view({"get": "single"})),

    # 定时任务相关接口
    path('schedule/', schedule.ScheduleView.as_view({
        "get": "list",
        "post": "add",
        "delete": "batch_delete"
    })),

    path('schedule/<int:id>/', schedule.ScheduleView.as_view({
        "get": "single",
        "patch": "update",
        "delete": "delete"
    })),

    # debugtalk.py 相关接口地址
    path('debugtalk/<int:pk>/', project.DebugTalkView.as_view({"get": "debugtalk"})),
    path('debugtalk/', project.DebugTalkView.as_view({
        "patch": "update",
        "post": "run"
    })),

    # file 接口地址
    path('file/', filehandle.FileView.as_view({
        "put": "upload"
    })),

    # case 接口模板地址
    path('case/', case.CaseTemplateView.as_view({
        "post": "add",
        "get": "list"
    })),

    path('case/<int:pk>/', case.CaseTemplateView.as_view({
        "delete": "delete",
        "get": "single",
        "patch": "update",
        "post": "copy"
    })),

    path('case/import/', case.CaseTemplateView.as_view({
        "post": "case_import",
    })),

    # suite 接口地址
    path('suite/', suite.SuiteView.as_view({
        "get": "list",
        "post": "add"
    })),

    path('suite/<int:id>/', suite.SuiteView.as_view({
        "get": "single",
        "patch": "update",
        "delete": "delete",
        "post": "copy"
    })),

    # config 接口地址
    path('config/', config.ConfigView.as_view({
        "post": "add",
        "get": "list",
        "delete": "delete"
    })),

    path('config/<int:pk>/', config.ConfigView.as_view({
        "post": "copy",
        "delete": "delete",
        "patch": "update",
        "get": "all"
    })),

    # variables 接口地址
    path('variables/', config.VariablesView.as_view({
        "post": "add",
        "get": "list",
        "delete": "delete"
    })),

    path('variables/<int:pk>/', config.VariablesView.as_view({
        "delete": "delete",
        "patch": "update"
    })),

    # leveltag 接口地址
    path('leveltag/', leveltag.LevelTagView.as_view({
        "post": "add",
        "get": "list",
        "delete": "delete"
    })),

    path('leveltag/<int:pk>/', leveltag.LevelTagView.as_view({
        "get": "single",
        "delete": "delete",
        "patch": "update"
    })),

    path('leveltag/parentinfo/', leveltag.LevelTagView.as_view({
        "get": "list_parentID"
    })),

    # run case
    path('run_case_by_body/', run.run_case_by_body),
    path('run_case_by_id/<int:id>/', run.run_case_by_id),

    # run suite
    path('run_suite_by_id/<int:id>', run.run_suite_by_id),
    path('run_testsuite/', run.run_testsuite),
    path('run_test/', run.run_test),
    path('run_testsuite_pk/<int:pk>/', run.run_testsuite_pk),
    path('run_suite_tree/', run.run_suite_tree),
    path('automation_test/', run.automation_test),

    # 报告地址
    path('reports/', report.ReportView.as_view({
        "get": "list"
    })),

    path('reports/<int:pk>/', report.ReportView.as_view({
        "delete": "delete",
        "get": "look"
    })),

    path('host_ip/', config.HostIPView.as_view({
        "post": "add",
        "get": "list"
    })),

    path('host_ip/<int:pk>/', config.HostIPView.as_view({
        "delete": "delete",
        "patch": "update",
        "get": "all"
    })),
]
