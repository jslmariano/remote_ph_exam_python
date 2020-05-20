from __future__ import annotations
import aenum
from http import HTTPStatus
import pprint


from sqlalchemy import func, distinct
from sqlalchemy.dialects import postgresql
from sqlalchemy.orm import load_only
from sqlalchemy.orm import lazyload
from sqlalchemy.orm.query import Query

class AbstractService(object):
    """docstring for AbstractService"""

    def createSession(self):
        return self.session

    def createQuery(self, _table_model):
        _session             = self.createSession()
        _query               = _session.query(_table_model)
        self.current_session = _session
        self.current_query   = _query
        return _query

    def setCurrentQuery(self, _query):
        self.current_query = _query
        return self

    def getCurrentQuery(self):
        return self.current_query

    def getInstrumentByColumn(self, _columns, _column_name_target = ''):
        _column_instrument = None
        for _column in _columns:
            if hasattr(_column, 'key'):
                if str(_column.key) == _column_name_target:
                    _column_instrument = _column
                    return _column_instrument
        return _column_instrument


    def getCurrentCount(self, _table_obj_pk):
        """
        Gets the current count.

        Modifed count to get the count fast
        Thanks to the community here.
        https://gist.github.com/hest/8798884

        :type       _table_obj_pk:  { type_description }
        :param      _table_obj_pk:  The table object pk

        :returns:   The current count.
        :rtype:     { return_type_description }
        """
        _query     = self.getCurrentQuery()
        if _query is None:
            return 0
        _query = _query.limit(None)
        _query = _query.offset(None)
        _query = _query.order_by(None)
        _query = _query.with_entities(
            func.count().over(None).label('total_count')
        )
        return _query.session.execute(_query).scalar()

    def getCurrentIDS(self, _table_obj_pk):
        _query     = self.getCurrentQuery()
        if _query is None:
            return []
        _query     = _query.with_entities(_table_obj_pk)
        return _query.all()


    def result2list(self, result, page = 0, pageSize = 0):
        indexctr = ((page) * pageSize)
        d = []
        for row in result:
            _row          = dict(zip(row.keys(), row))
            _row['index'] = indexctr
            d.append(_row)
            indexctr += 1
        return d

    def result2dict(self, result, _column = 'id'):
        d = {}
        indexctr = 0
        for row in result:
            _row          = dict(zip(row.keys(), row))
            _row['index'] = indexctr
            d[_row.get(_column, indexctr)] = _row
            indexctr += 1
        return d

    def allToDict(self, _query_instance):
        if not isinstance(_query_instance, Query):
            return ['Oops! Not a query instance!']
        _result_dict = [_u.__dict__ for _u in _query_instance]
        return _result_dict

    def showQuery(self, _query_object, return_query = False):
        DEBUG = True
        if not DEBUG:
            print("____________DEBUG SHOW QUERY is OFF ____________________________:")
            return "";
            pass
        print("____________DEBUG SHOW QUERY ____________________________:")

        if isinstance(_query_object, Query):
            _query_statement = _query_object.statement
        else:
            _query_statement = _query_object

        string_query = str(_query_statement.compile(
            dialect=postgresql.dialect(),
            compile_kwargs={"literal_binds": True}))
        if return_query:
            print("____________DEBUG RETURNED QUERY ____________________________:")
            return string_query
            pass
        else:
            print(string_query)
            pass
        print("____________DEBUG SHOW QUERY ____________________________:")
        pass