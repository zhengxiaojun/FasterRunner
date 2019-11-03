# -*- coding: utf-8 -*-
from django.db import models

# Create your models here.
from fastuser.models import BaseTable


class Project(BaseTable):
    """
    项目信息表
    """

    class Meta:
        verbose_name = "项目信息"
        db_table = "Project"

    name = models.CharField("项目名称", unique=True, null=False, max_length=100)
    desc = models.CharField("简要介绍", max_length=100, null=False)
    responsible = models.CharField("创建人", max_length=20, null=False)


class Debugtalk(models.Model):
    """
    驱动文件表
    """

    class Meta:
        verbose_name = "驱动库"
        db_table = "Debugtalk"

    code = models.TextField("python代码", default="# write you code", null=False)
    project = models.OneToOneField(to=Project, on_delete=models.CASCADE)


class Config(BaseTable):
    """
    环境信息表
    """

    class Meta:
        verbose_name = "环境信息"
        db_table = "Config"

    name = models.CharField("环境名称", null=False, max_length=100)
    body = models.TextField("主体信息", null=False)
    base_url = models.CharField("请求地址", null=False, max_length=100)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)


class Case(BaseTable):
    """
    用例信息表
    """

    class Meta:
        verbose_name = "用例信息"
        db_table = "Case"

    name = models.CharField("接口名称", null=False, max_length=100)
    body = models.TextField("主体信息", null=False)
    url = models.CharField("请求地址", null=False, max_length=200)
    method = models.CharField("请求方式", null=False, max_length=10)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    leveltag_name = models.CharField("层级名称", null=False, max_length=100)


class Suite(BaseTable):
    """
    套件信息表
    """

    class Meta:
        verbose_name = "套件信息"
        db_table = "Suite"

    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    name = models.CharField("套件名称", null=False, max_length=100)
    length = models.IntegerField("用例个数", null=False)
    leveltag_name = models.CharField("层级名称", null=False, max_length=100)


class CaseStepInSuite(BaseTable):
    """
    Test Case Step
    """

    class Meta:
        verbose_name = "套件内用例执行顺序"
        db_table = "CaseStepInSuite"

    case_id = models.IntegerField("用例ID", null=False)
    case_name = models.CharField("用例名称", null=False, max_length=100)
    step = models.IntegerField("执行顺序", null=False)
    suite = models.ForeignKey(Suite, on_delete=models.CASCADE)


class HostIP(BaseTable):
    """
    全局变量
    """

    class Meta:
        verbose_name = "HOST配置"
        db_table = "HostIP"

    name = models.CharField(null=False, max_length=100)
    value = models.TextField(null=False)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)


class Variables(BaseTable):
    """
    全局变量
    """

    class Meta:
        verbose_name = "全局变量"
        db_table = "Variables"

    key = models.CharField(null=False, max_length=100)
    value = models.CharField(null=False, max_length=1024)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)


class Report(BaseTable):
    """
    报告存储
    """
    report_type = (
        (1, "调试"),
        (2, "异步"),
        (3, "定时")
    )

    class Meta:
        verbose_name = "测试报告"
        db_table = "Report"

    name = models.CharField("报告名称", null=False, max_length=100)
    type = models.IntegerField("报告类型", choices=report_type)
    summary = models.TextField("主体信息", null=False)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)


class Relation(models.Model):
    """
    树形结构关系
    """

    class Meta:
        verbose_name = "树形结构关系"
        db_table = "Relation"

    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    tree = models.TextField("结构主题", null=False, default=[])
    type = models.IntegerField("树类型", default=1)


class LevelTag(models.Model):
    """
    层级标签关系
    """

    class Meta:
        verbose_name = "层级标签关系"
        db_table = "LevelTag"

    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    name = models.TextField("层级名称", null=False, default='')
    level = models.IntegerField("当前层级", default=1)
    parentName = models.TextField("父级名称", null=False, default='')
    ltype = models.IntegerField("主体类型", default=1)  # 1 case,  2 suite
