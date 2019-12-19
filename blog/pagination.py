# -*- encoding: utf-8 -*-
"""
@File:      pagination.py.py
@Time:      2019/12/15 3:40 下午
@Author:    Colin
@Email:     bsply@126.com
@Software:  PyCharm
"""
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
# from rest_framework.pagination import LimitOffsetPagination
from rest_framework.pagination import CursorPagination


class StandardResultsSetPagination(PageNumberPagination):
    # 获取URL参数中传入的页码key
    page_query_param = 'page'

    # 默认每页显示的数据条数
    page_size = 10
    # URL传入的每页显示条数的参数
    page_size_query_param = 'page_size'
    # 每页显示数据最大条数
    max_page_size = 10
    # 根据ID从大到小排列
    ordering = "-createTime"

    def get_paginated_response(self, data):
        from collections import OrderedDict
        return Response(OrderedDict([
            ('count', self.page.paginator.count),
            ('page_size', self.page_size),
            ('current_page', int(self.request.query_params.get(self.page_query_param, 1))),
            ('next', self.get_next_link()),
            ('previous', self.get_previous_link()),
            ('results', data)
        ]))


# class StandardResultsSetPagination(CursorPagination):
#     # URL传入的游标参数
#     cursor_query_param = 'cursor'
#     # 默认每页显示的数据条数
#     page_size = 2
#     # URL传入的每页显示条数的参数
#     page_size_query_param = 'page_size'
#     # 每页显示数据最大条数
#     max_page_size = 1000
#
#     # 根据ID从大到小排列
#     ordering = "-createTime"