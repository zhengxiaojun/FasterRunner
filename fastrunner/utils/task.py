import json
import logging
from djcelery import models as celery_models

from fastrunner.utils import response
from fastrunner.utils.parser import format_json

logger = logging.getLogger('FasterRunner')


class Task(object):
    """
    定时任务操作
    """

    def __init__(self, opt, **kwargs):
        logger.info("before process task data:\n {kwargs}".format(kwargs=format_json(kwargs)))
        if opt == 'update':
            self.__crontab_id = kwargs["crontab_id"]
            self.__task_id = kwargs['task_id']
        self.__name = kwargs["name"]
        self.__data = kwargs["data"]
        self.__crontab = kwargs["crontab"]
        self.__switch = kwargs["switch"]
        self.__task = "fastrunner.tasks.schedule_debug_api"
        self.__project = kwargs["project"]
        self.__suite_id = kwargs["suite_id"]
        self.__email = {
            "name": kwargs["name"],
            "strategy": kwargs["strategy"],
            "copy": kwargs["copy"],
            "receiver": kwargs["receiver"],
            "crontab": self.__crontab,
            "project": self.__project,
            "suite_id": self.__suite_id
        }
        self.__crontab_time = None

    def format_crontab(self):
        """
        格式化时间
        """
        crontab = self.__crontab.split(' ')
        if len(crontab) > 5:
            return response.TASK_TIME_ILLEGAL
        try:
            self.__crontab_time = {
                'day_of_week': crontab[4],
                'month_of_year': crontab[3],
                'day_of_month': crontab[2],
                'hour': crontab[1],
                'minute': crontab[0]
            }
        except Exception:
            return response.TASK_TIME_ILLEGAL

        return response.CRONTAB_ADD_SUCCESS

    def add_task(self):
        """
        add task
        """
        if celery_models.PeriodicTask.objects.filter(name__exact=self.__name).count() > 0:
            logger.info("{name} tasks exist".format(name=self.__name))
            return response.TASK_HAS_EXISTS

        if self.__email["strategy"] == '始终发送' or self.__email["strategy"] == '仅失败发送':
            if self.__email["receiver"] == '':
                return response.TASK_EMAIL_ILLEGAL

        resp = self.format_crontab()
        if resp["success"]:
            task, created = celery_models.PeriodicTask.objects.get_or_create(name=self.__name, task=self.__task)
            crontab = celery_models.CrontabSchedule.objects.filter(**self.__crontab_time).first()
            if crontab is None:
                crontab = celery_models.CrontabSchedule.objects.create(**self.__crontab_time)
            task.crontab = crontab
            task.enabled = self.__switch
            task.args = json.dumps(self.__data, ensure_ascii=False)
            task.kwargs = json.dumps(self.__email, ensure_ascii=False)
            task.description = self.__project
            task.save()
            logger.info("{name} tasks save success".format(name=self.__name))
            return response.TASK_ADD_SUCCESS
        else:
            return resp

    def update_task(self):
        """
        update task
        """
        if celery_models.PeriodicTask.objects.filter(id=self.__task_id).count() == 0:
            logger.info("{name} tasks not exist".format(name=self.__name))
            return response.TASK_NOT_EXISTS

        if self.__email["strategy"] == '始终发送' or self.__email["strategy"] == '仅失败发送':
            if self.__email["receiver"] == '':
                return response.TASK_EMAIL_ILLEGAL

        resp = self.format_crontab()
        if resp["success"]:
            task = celery_models.PeriodicTask.objects.filter(id=self.__task_id)

            crontab = celery_models.CrontabSchedule.objects.filter(id=self.__crontab_id)
            crontab.update(**self.__crontab_time)

            data = {
                'name': self.__name,
                'task': self.__task,
                'crontab_id': self.__crontab_id,
                'enabled': self.__switch,
                'args': json.dumps(self.__data, ensure_ascii=False),
                'kwargs': json.dumps(self.__email, ensure_ascii=False),
                'description': self.__project
            }

            task.update(**data)
            logger.info("{name} tasks update success".format(name=self.__name))
            return response.TASK_UPDATE_SUCCESS
        else:
            return resp
