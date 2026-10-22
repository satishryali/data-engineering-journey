"""SQLite-only disposable fixtures. No access to any learner database or filesystem."""
import sqlite3
import time


def run_sql(query, kind='count'):
    if len(query) > 12000 or not query.strip():
        return {'passed': False, 'error': 'Enter a SELECT query of at most 12,000 characters.', 'fixtures': []}
    fixtures = [([(1, 'Asha'), (2, 'Asha'), (3, 'Devi')], [(101, 1, 7), (102, 1, None), (103, 3, 0)]),
                ([(7, 'Ravi'), (9, 'Mira'), (10, 'Ravi')], [(501, 9, None), (502, 9, None)]),
                ([(4, 'Zero')], [])]
    results = []
    allowed_functions = {'count', 'sum', 'coalesce', 'ifnull', 'total', 'min', 'max', 'avg'}
    for customers, orders in fixtures:
        db = sqlite3.connect(':memory:')
        try:
            db.enable_load_extension(False)
            db.setlimit(sqlite3.SQLITE_LIMIT_LENGTH, 100000)
            db.setlimit(sqlite3.SQLITE_LIMIT_SQL_LENGTH, 12000)
            db.setlimit(sqlite3.SQLITE_LIMIT_COLUMN, 40)
            db.setlimit(sqlite3.SQLITE_LIMIT_EXPR_DEPTH, 40)
            db.setlimit(sqlite3.SQLITE_LIMIT_COMPOUND_SELECT, 5)
            db.executescript('CREATE TABLE customers(customer_id INTEGER PRIMARY KEY,name TEXT); CREATE TABLE orders(order_id INTEGER PRIMARY KEY,customer_id INTEGER,amount INTEGER);')
            db.executemany('INSERT INTO customers VALUES(?,?)', customers)
            db.executemany('INSERT INTO orders VALUES(?,?,?)', orders)
            def authorize(action, arg1, arg2, database, trigger):
                if action == sqlite3.SQLITE_READ:
                    # SQLite can report database=None for an implicit rowid read.
                    return sqlite3.SQLITE_OK if arg1 in ('customers', 'orders') and database in ('main', None) else sqlite3.SQLITE_DENY
                if action == sqlite3.SQLITE_FUNCTION:
                    return sqlite3.SQLITE_OK if (arg2 or '').lower() in allowed_functions else sqlite3.SQLITE_DENY
                return sqlite3.SQLITE_OK if action == sqlite3.SQLITE_SELECT else sqlite3.SQLITE_DENY
            db.set_authorizer(authorize)
            deadline = time.monotonic() + .4
            steps = 0
            def limit():
                nonlocal steps
                steps += 1
                return steps > 1500 or time.monotonic() > deadline
            db.set_progress_handler(limit, 100)
            actual = db.execute(query).fetchmany(101)
            if len(actual) > 100:
                raise ValueError('Result exceeds 100-row limit')
            expected = []
            for ident, name in customers:
                matches = [o for o in orders if o[1] == ident]
                if kind == 'join':
                    expected.extend((ident, o[0]) for o in matches) if matches else expected.append((ident, None))
                elif kind == 'sum':
                    amounts = [o[2] for o in matches if o[2] is not None]
                    expected.append((ident, name, sum(amounts) if amounts else None))
                else:
                    expected.append((ident, name, len(matches)))
            results.append({'passed': actual == expected, 'actual': actual, 'expected': expected})
        except (sqlite3.Error, ValueError) as error:
            return {'passed': False, 'error': str(error), 'fixtures': results}
        finally:
            db.close()
    return {'passed': all(f['passed'] for f in results), 'fixtures': results, 'error': None}
