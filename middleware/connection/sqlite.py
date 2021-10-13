from sqlalchemy.sql import expression
from sqlalchemy.ext import compiler


class group_concat_sqlite(expression.FunctionElement):
    name = "group_concat"


@compiler.compiles(group_concat_sqlite, 'sqlite')
def _group_concat_sqlite(element, compiler, **kw):
    if len(element.clauses) == 2:
        separator = element.clauses.clauses[1].value
    else:
        separator = ','

    return "GROUP_CONCAT({} , '{}')".format(
        compiler.process(element.clauses.clauses[0]),
        separator,
    )
