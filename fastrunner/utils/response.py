PROJECT_ADD_SUCCESS = {
    "code": "0001",
    "success": True,
    "msg": "项目添加成功"
}

PROJECT_EXISTS = {
    "code": "0101",
    "success": False,
    "msg": "项目已存在"
}

PROJECT_NOT_EXISTS = {
    "code": "0102",
    "success": False,
    "msg": "项目不存在"
}

DEBUGTALK_NOT_EXISTS = {
    "code": "0102",
    "success": False,
    "msg": "debugtalk不存在"
}

DEBUGTALK_UPDATE_SUCCESS = {
    "code": "0002",
    "success": True,
    "msg": "debugtalk更新成功"
}

PROJECT_UPDATE_SUCCESS = {
    "code": "0002",
    "success": True,
    "msg": "项目更新成功"
}

PROJECT_DELETE_SUCCESS = {
    "code": "0003",
    "success": True,
    "msg": "项目删除成功"
}

SYSTEM_ERROR = {
    "code": "9999",
    "success": False,
    "msg": "系统错误"
}

TREE_ADD_SUCCESS = {
    "code": "0001",
    "success": True,
    "msg": "树形结构添加成功"
}

TREE_UPDATE_SUCCESS = {
    "code": "0002",
    "success": True,
    "msg": "树形结构更新成功"
}

KEY_MISS = {
    "code": "0100",
    "success": False,
    "msg": "请求数据非法"
}

FILE_UPLOAD_SUCCESS = {
    'code': '0001',
    'success': True,
    'msg': '文件上传成功'
}

FILE_EXISTS = {
    'code': '0101',
    'success': False,
    'msg': '文件已存在,默认使用已有文件'
}

# CASE

DATA_TO_LONG = {
    'code': '0100',
    'success': False,
    'msg': '数据信息过长！'
}

CASE_ADD_SUCCESS = {
    'code': '0001',
    'success': True,
    'msg': '用例添加成功'
}

CASE_EXISTS = {
    "code": "0101",
    "success": False,
    "msg": "已存在该用例,请重新命名"
}

CASE_NOT_EXISTS = {
    "code": "0102",
    "success": False,
    "msg": "该用例不存在"
}

CASE_UPLOAD_SUCCESS = {
    'code': '0103',
    'success': True,
    'msg': '用例导入成功'
}

CASE_UPLOAD_FAIL = {
    'code': '0104',
    'success': False,
    'msg': '无可用用例导入'
}

CASE_DELETE_SUCCESS = {
    "code": "0003",
    "success": True,
    "msg": "该用例删除成功"
}

CASE_IN_SUITE = {
    "code": "0303",
    "success": False,
    "msg": "该用例在套件内,请先在套件内删除该用例后,再执行删除"
}

CASE_UPDATE_SUCCESS = {
    'code': '0002',
    'success': True,
    'msg': '该用例更新成功'
}

# SUITE

SUITE_ADD_SUCCESS = {
    'code': '0001',
    'success': True,
    'msg': '套件添加成功'
}

SUITE_EXISTS = {
    "code": "0101",
    "success": False,
    "msg": "该套件名称已存在,请重新命名"
}

SUITE_NOT_EXISTS = {
    "code": "0102",
    "success": False,
    "msg": "该套件名称不存在"
}

SUITE_UPDATE_SUCCESS = {
    'code': '0002',
    'success': True,
    'msg': '该套件名称更新成功'
}

SUITE_DEL_SUCCESS = {
    'code': '0003',
    'success': True,
    'msg': '套件删除成功'
}

CONFIG_EXISTS = {
    "code": "0101",
    "success": False,
    "msg": "此配置已存在，请重新命名"
}

VARIABLES_EXISTS = {
    "code": "0101",
    "success": False,
    "msg": "此变量已存在，请重新命名"
}

CONFIG_ADD_SUCCESS = {
    'code': '0001',
    'success': True,
    'msg': '环境添加成功'
}

VARIABLES_ADD_SUCCESS = {
    'code': '0001',
    'success': True,
    'msg': '变量添加成功'
}

CONFIG_NOT_EXISTS = {
    "code": "0102",
    "success": False,
    "msg": "指定的环境不存在"
}

REPORT_NOT_EXISTS = {
    "code": "0102",
    "success": False,
    "msg": "指定的报告不存在"
}

REPORT_DEL_SUCCESS = {
    'code': '0003',
    'success': True,
    'msg': '报告删除成功'
}

VARIABLES_NOT_EXISTS = {
    "code": "0102",
    "success": False,
    "msg": "指定的全局变量不存在"
}

CONFIG_UPDATE_SUCCESS = {
    "code": "0002",
    "success": True,
    "msg": "环境更新成功"
}

VARIABLES_UPDATE_SUCCESS = {
    "code": "0002",
    "success": True,
    "msg": "全局变量更新成功"
}

TASK_ADD_SUCCESS = {
    "code": "0001",
    "success": True,
    "msg": "定时任务新增成功"
}

TASK_TIME_ILLEGAL = {
    "code": "0101",
    "success": False,
    "msg": "时间表达式非法"
}

TASK_HAS_EXISTS = {
    "code": "0102",
    "success": False,
    "msg": "定时任务已存在"
}

TASK_EMAIL_ILLEGAL = {
    "code": "0102",
    "success": False,
    "msg": "请指定邮件接收人列表"
}

TASK_DEL_SUCCESS = {
    "code": "0003",
    "success": True,
    "msg": "任务删除成功"
}

PLAN_DEL_SUCCESS = {
    "code": "0003",
    "success": True,
    "msg": "集成计划删除成功"
}

PLAN_ADD_SUCCESS = {
    "code": "0001",
    "success": True,
    "msg": "计划添加成功"
}

PLAN_KEY_EXIST = {
    "code": "0101",
    "success": False,
    "msg": "该KEY值已存在，请修改KEY值"
}

PLAN_ILLEGAL = {
    "code": "0101",
    "success": False,
    "msg": "提取字段格式错误，请检查"
}

PLAN_UPDATE_SUCCESS = {
    "code": "0002",
    "success": True,
    "msg": "计划更新成功"
}

HOSTIP_EXISTS = {
    "code": "0101",
    "success": False,
    "msg": "此域名已存在，请重新命名"
}

HOSTIP_ADD_SUCCESS = {
    'code': '0001',
    'success': True,
    'msg': '域名添加成功'
}

HOSTIP_NOT_EXISTS = {
    "code": "0102",
    "success": False,
    "msg": "指定的域名不存在"
}

HOSTIP_UPDATE_SUCCESS = {
    "code": "0002",
    "success": True,
    "msg": "域名更新成功"
}

HOST_DEL_SUCCESS = {
    'code': '0003',
    'success': True,
    'msg': '域名删除成功'
}

# LEVELTAG

LEVELTAG_EXISTS = {
    "code": "0001",
    "success": False,
    "msg": "该层级标签已存在，请重新命名"
}

LEVELTAG_NOT_EXISTS = {
    "code": "0002",
    "success": False,
    "msg": "该层级标签不存在"
}

LEVELTAG_ADD_SUCCESS = {
    'code': '0003',
    'success': True,
    'msg': '层级标签添加成功'
}

LEVELTAG_UPDATE_SUCCESS = {
    "code": "0004",
    "success": True,
    "msg": "层级标签更新成功"
}

LEVELTAG_DEL_SUCCESS = {
    'code': '0003',
    'success': True,
    'msg': '层级标签删除成功'
}
