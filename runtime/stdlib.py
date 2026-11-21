MAX_COLLECTION = 100000


def type_of(value):
    if value is None:
        return "null"
    if isinstance(value, bool):
        return "boolean"
    if isinstance(value, int):
        return "integer"
    if isinstance(value, float):
        return "float"
    if isinstance(value, str):
        return "string"
    if isinstance(value, list):
        return "list"
    if isinstance(value, dict):
        return "dict"
    return "unknown"


def length(value):
    if not isinstance(value, (str, list, dict)):
        raise TypeError("দৈর্ঘ্য() শুধু String, List বা Dictionary গ্রহণ করে")
    return len(value)


def append(items, value):
    if not isinstance(items, list):
        raise TypeError("যোগ_করো() প্রথম মান List হতে হবে")
    if len(items) >= MAX_COLLECTION:
        raise RuntimeError("List অতিরিক্ত বড়")
    return items + [value]


def keys(mapping):
    if not isinstance(mapping, dict):
        raise TypeError("চাবি() শুধু Dictionary গ্রহণ করে")
    return list(mapping.keys())




def _number(value, name):
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise TypeError(f"{name}() সংখ্যাসূচক মান গ্রহণ করে")
    return value


def absolute(value):
    return abs(_number(value, "abs"))


def rounded(value):
    return round(_number(value, "round"))


def floor_number(value):
    import math
    return math.floor(_number(value, "floor"))


def ceil_number(value):
    import math
    return math.ceil(_number(value, "ceil"))


def square_root(value):
    import math
    value = _number(value, "sqrt")
    if value < 0:
        raise ValueError("sqrt() ঋণাত্মক সংখ্যা গ্রহণ করে না")
    return math.sqrt(value)


def _string(value, name):
    if not isinstance(value, str):
        raise TypeError(f"{name}() String গ্রহণ করে")
    return value


def string_upper(value):
    return _string(value, "upper").upper()


def string_lower(value):
    return _string(value, "lower").lower()


def string_strip(value):
    return _string(value, "strip").strip()


def contains(container, item):
    if not isinstance(container, (str, list, dict)):
        raise TypeError("contains() প্রথম মান String, List বা Dictionary হতে হবে")
    return item in container


def string_replace(value, old, new):
    value = _string(value, "replace")
    old = _string(old, "replace")
    new = _string(new, "replace")
    return value.replace(old, new)



def _list(value, name):
    if not isinstance(value, list):
        raise TypeError(f"{name}() List গ্রহণ করে")
    return value


def reverse_list(items):
    return list(reversed(_list(items, "reverse")))


def sort_list(items):
    items = _list(items, "sort")
    try:
        result = sorted(items)
    except TypeError:
        raise TypeError("sort() List-এর মানগুলো পরস্পর তুলনাযোগ্য হতে হবে") from None
    return result


def remove_item(items, value):
    result = list(_list(items, "remove"))
    try:
        result.remove(value)
    except ValueError:
        raise ValueError("remove() মানটি List-এ পাওয়া যায়নি") from None
    return result


def insert_item(items, index, value):
    items = _list(items, "insert")
    if isinstance(index, bool) or not isinstance(index, int):
        raise TypeError("insert() Index অবশ্যই Integer হতে হবে")
    if index < 0 or index > len(items):
        raise ValueError("insert() Index সীমার বাইরে")
    if len(items) >= MAX_COLLECTION:
        raise RuntimeError("List অতিরিক্ত বড়")
    result = list(items)
    result.insert(index, value)
    return result


def dict_values(mapping):
    if not isinstance(mapping, dict):
        raise TypeError("values() শুধু Dictionary গ্রহণ করে")
    return list(mapping.values())


def has_key(mapping, key):
    if not isinstance(mapping, dict):
        raise TypeError("has_key() শুধু Dictionary গ্রহণ করে")
    return key in mapping


def get_value(mapping, key):
    if not isinstance(mapping, dict):
        raise TypeError("get() শুধু Dictionary গ্রহণ করে")
    return mapping.get(key)

BUILTINS = {
    "ধরন": (1, type_of),
    "type_of": (1, type_of),
    "দৈর্ঘ্য": (1, length),
    "length": (1, length),
    "যোগ_করো": (2, append),
    "append": (2, append),
    "চাবি": (1, keys),
    "keys": (1, keys),

    "পরম": (1, absolute),
    "abs": (1, absolute),
    "পূর্ণ_রাউন্ড": (1, rounded),
    "round": (1, rounded),
    "নিচের_পূর্ণ": (1, floor_number),
    "floor": (1, floor_number),
    "উপরের_পূর্ণ": (1, ceil_number),
    "ceil": (1, ceil_number),
    "বর্গমূল": (1, square_root),
    "sqrt": (1, square_root),

    "বড়_হাতের": (1, string_upper),
    "upper": (1, string_upper),
    "ছোট_হাতের": (1, string_lower),
    "lower": (1, string_lower),
    "ছাঁটো": (1, string_strip),
    "strip": (1, string_strip),
    "আছে_কি": (2, contains),
    "contains": (2, contains),
    "প্রতিস্থাপন": (3, string_replace),
    "replace": (3, string_replace),
    "উল্টাও": (1, reverse_list),
    "reverse": (1, reverse_list),
    "সাজাও": (1, sort_list),
    "sort": (1, sort_list),
    "বাদ_দাও": (2, remove_item),
    "remove": (2, remove_item),
    "ঢোকাও": (3, insert_item),
    "insert": (3, insert_item),
    "মানসমূহ": (1, dict_values),
    "values": (1, dict_values),
    "চাবি_আছে_কি": (2, has_key),
    "has_key": (2, has_key),
    "নাও_মান": (2, get_value),
    "get": (2, get_value),

}

# BB_SYSTEM_LIBRARY_V1
# Platform adapter: filesystem and JSON builtins.
# All file paths are restricted to the current working directory.

import json as _bb_json
import os as _bb_os
import tempfile as _bb_tempfile
from pathlib import Path as _BBPath

MAX_FILE_BYTES = 1024 * 1024
MAX_DIRECTORY_ENTRIES = 1000


def _bb_safe_path(value):
    if not isinstance(value, str) or not value:
        raise TypeError("File path অবশ্যই non-empty String হতে হবে")
    if "\x00" in value or "\\" in value:
        raise ValueError("Invalid file path")

    relative = _BBPath(value)
    if relative.is_absolute() or any(
        part in ("..", ".") for part in relative.parts
    ):
        raise ValueError("শুধু Workspace-এর relative path অনুমোদিত")

    root = _BBPath.cwd().resolve(strict=True)
    candidate = root.joinpath(relative)

    current = root
    for part in relative.parts:
        current = current / part
        if current.is_symlink():
            raise ValueError("Symlink path অনুমোদিত নয়")

    resolved = candidate.resolve(strict=False)
    try:
        resolved.relative_to(root)
    except ValueError:
        raise ValueError("Workspace-এর বাইরে যাওয়া যাবে না") from None

    return candidate



def _bb_open_parent(path):
    _bb_safe_path(path)
    parts = _BBPath(path).parts
    if not parts:
        raise ValueError("File path-এ filename থাকতে হবে")

    flags = (
        _bb_os.O_RDONLY
        | _bb_os.O_DIRECTORY
        | _bb_os.O_NOFOLLOW
        | _bb_os.O_CLOEXEC
    )
    fd = _bb_os.open(".", flags)
    try:
        for part in parts[:-1]:
            next_fd = _bb_os.open(part, flags, dir_fd=fd)
            _bb_os.close(fd)
            fd = next_fd
        return fd, parts[-1]
    except Exception:
        _bb_os.close(fd)
        raise


def _bb_open_directory(path):
    _bb_safe_path(path)
    flags = (
        _bb_os.O_RDONLY
        | _bb_os.O_DIRECTORY
        | _bb_os.O_NOFOLLOW
        | _bb_os.O_CLOEXEC
    )
    fd = _bb_os.open(".", flags)
    try:
        for part in _BBPath(path).parts:
            next_fd = _bb_os.open(part, flags, dir_fd=fd)
            _bb_os.close(fd)
            fd = next_fd
        return fd
    except Exception:
        _bb_os.close(fd)
        raise


def file_read(path):
    try:
        parent_fd, name = _bb_open_parent(path)
    except FileNotFoundError:
        raise ValueError("File পাওয়া যায়নি বা এটি regular file নয়") from None
    fd = None
    try:
        flags = (
            _bb_os.O_RDONLY
            | _bb_os.O_NOFOLLOW
            | _bb_os.O_CLOEXEC
            | getattr(_bb_os, "O_NONBLOCK", 0)
        )
        try:
            fd = _bb_os.open(name, flags, dir_fd=parent_fd)
        except FileNotFoundError:
            raise ValueError("File পাওয়া যায়নি বা এটি regular file নয়") from None
        import stat as _bb_stat
        info = _bb_os.fstat(fd)
        if not _bb_stat.S_ISREG(info.st_mode):
            raise ValueError("শুধু regular file পড়া যাবে")
        if info.st_size > MAX_FILE_BYTES:
            raise ValueError("File size limit অতিক্রম করেছে")

        chunks = []
        total = 0
        while True:
            chunk = _bb_os.read(fd, min(65536, MAX_FILE_BYTES + 1 - total))
            if not chunk:
                break
            chunks.append(chunk)
            total += len(chunk)
            if total > MAX_FILE_BYTES:
                raise ValueError("File size limit অতিক্রম করেছে")
        return b"".join(chunks).decode("utf-8")
    finally:
        if fd is not None:
            _bb_os.close(fd)
        _bb_os.close(parent_fd)


def file_write(path, content):
    if not isinstance(content, str):
        raise TypeError("File content অবশ্যই String হতে হবে")
    data = content.encode("utf-8")
    if len(data) > MAX_FILE_BYTES:
        raise ValueError("File size limit অতিক্রম করেছে")

    try:
        parent_fd, name = _bb_open_parent(path)
    except FileNotFoundError:
        raise ValueError("Parent directory আগে থেকে থাকতে হবে") from None
    temp_name = None
    fd = None
    try:
        try:
            existing = _bb_os.stat(
                name, dir_fd=parent_fd, follow_symlinks=False
            )
        except FileNotFoundError:
            existing = None

        if existing is not None:
            import stat as _bb_stat
            if _bb_stat.S_ISLNK(existing.st_mode):
                raise ValueError("Symlink target অনুমোদিত নয়")
            if not _bb_stat.S_ISREG(existing.st_mode):
                raise ValueError("Target regular file হতে হবে")

        import secrets as _bb_secrets
        flags = (
            _bb_os.O_WRONLY
            | _bb_os.O_CREAT
            | _bb_os.O_EXCL
            | _bb_os.O_NOFOLLOW
            | _bb_os.O_CLOEXEC
        )
        for _ in range(10):
            candidate = ".bb-write-" + _bb_secrets.token_hex(12)
            try:
                fd = _bb_os.open(
                    candidate, flags, 0o600, dir_fd=parent_fd
                )
                temp_name = candidate
                break
            except FileExistsError:
                continue
        if fd is None:
            raise OSError("Temporary file তৈরি করা যায়নি")

        view = memoryview(data)
        while view:
            written = _bb_os.write(fd, view)
            if written <= 0:
                raise OSError("File write অসম্পূর্ণ")
            view = view[written:]
        _bb_os.fsync(fd)
        _bb_os.close(fd)
        fd = None

        _bb_os.replace(
            temp_name,
            name,
            src_dir_fd=parent_fd,
            dst_dir_fd=parent_fd,
        )
        temp_name = None
        return True
    finally:
        if fd is not None:
            _bb_os.close(fd)
        if temp_name is not None:
            try:
                _bb_os.unlink(temp_name, dir_fd=parent_fd)
            except OSError:
                pass
        _bb_os.close(parent_fd)


def file_exists(path):
    try:
        parent_fd, name = _bb_open_parent(path)
    except FileNotFoundError:
        return False
    fd = None
    try:
        flags = (
            _bb_os.O_RDONLY
            | _bb_os.O_NOFOLLOW
            | _bb_os.O_CLOEXEC
            | getattr(_bb_os, "O_NONBLOCK", 0)
        )
        try:
            fd = _bb_os.open(name, flags, dir_fd=parent_fd)
        except FileNotFoundError:
            return False
        import stat as _bb_stat
        return _bb_stat.S_ISREG(_bb_os.fstat(fd).st_mode)
    finally:
        if fd is not None:
            _bb_os.close(fd)
        _bb_os.close(parent_fd)


def directory_list(path):
    try:
        fd = _bb_open_directory(path)
    except (FileNotFoundError, NotADirectoryError):
        raise ValueError("Directory পাওয়া যায়নি বা path directory নয়") from None
    try:
        entries = []
        import stat as _bb_stat
        for name in _bb_os.listdir(fd):
            try:
                info = _bb_os.stat(
                    name, dir_fd=fd, follow_symlinks=False
                )
            except FileNotFoundError:
                continue
            if _bb_stat.S_ISLNK(info.st_mode):
                continue
            entries.append(name)
            if len(entries) > MAX_DIRECTORY_ENTRIES:
                raise ValueError("Directory entry limit অতিক্রম করেছে")
        return sorted(entries)
    finally:
        _bb_os.close(fd)


def _bb_reject_duplicate_json(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"Duplicate JSON key: {key}")
        result[key] = value
    return result


def _bb_reject_json_constant(value):
    raise ValueError(f"Invalid JSON constant: {value}")


def json_parse(source):
    if not isinstance(source, str):
        raise TypeError("JSON input অবশ্যই String হতে হবে")
    if len(source.encode("utf-8")) > MAX_FILE_BYTES:
        raise ValueError("JSON size limit অতিক্রম করেছে")
    return _bb_json.loads(
        source,
        object_pairs_hook=_bb_reject_duplicate_json,
        parse_constant=_bb_reject_json_constant,
    )


def json_stringify(value):
    result = _bb_json.dumps(
        value,
        ensure_ascii=False,
        allow_nan=False,
        separators=(",", ":"),
    )
    if len(result.encode("utf-8")) > MAX_FILE_BYTES:
        raise ValueError("JSON output size limit অতিক্রম করেছে")
    return result


BUILTINS.update({
    "file_read": (1, file_read),
    "ফাইল_পড়ো": (1, file_read),
    "file_write": (2, file_write),
    "ফাইল_লেখো": (2, file_write),
    "file_exists": (1, file_exists),
    "ফাইল_আছে_কি": (1, file_exists),
    "directory_list": (1, directory_list),
    "ডিরেক্টরি_তালিকা": (1, directory_list),
    "json_parse": (1, json_parse),
    "জেসন_পড়ো": (1, json_parse),
    "json_stringify": (1, json_stringify),
    "জেসন_লেখো": (1, json_stringify),
})

# BB_ENV_PATH_V1
# Environment access is restricted to non-secret display/runtime variables.

_BB_ALLOWED_ENV = {"LANG", "TERM", "COLORTERM", "TZ"}

def env_get(name):
    if not isinstance(name, str):
        raise TypeError("Environment name অবশ্যই String হতে হবে")
    if name not in _BB_ALLOWED_ENV:
        raise ValueError("এই Environment Variable পড়ার অনুমতি নেই")
    return _bb_os.environ.get(name, "")

def path_join(base, child):
    if not isinstance(base, str) or not isinstance(child, str):
        raise TypeError("Path arguments অবশ্যই String হতে হবে")
    if not base or not child:
        raise ValueError("Path খালি হতে পারবে না")

    joined = _BBPath(base) / _BBPath(child)
    normalized = joined.as_posix()
    _bb_safe_path(normalized)
    return normalized

def path_name(path):
    return _bb_safe_path(path).name

def path_extension(path):
    return _bb_safe_path(path).suffix

def path_is_dir(path):
    return _bb_safe_path(path).is_dir()

def path_is_file(path):
    return _bb_safe_path(path).is_file()

BUILTINS.update({
    "env_get": (1, env_get),
    "পরিবেশ_পড়ো": (1, env_get),
    "path_join": (2, path_join),
    "পথ_জোড়ো": (2, path_join),
    "path_name": (1, path_name),
    "পথের_নাম": (1, path_name),
    "path_extension": (1, path_extension),
    "পথের_এক্সটেনশন": (1, path_extension),
    "path_is_dir": (1, path_is_dir),
    "পথ_ডিরেক্টরি_কি": (1, path_is_dir),
    "path_is_file": (1, path_is_file),
    "পথ_ফাইল_কি": (1, path_is_file),
})

# BB_SQLITE_API_V1
# SQLite platform adapter. Database paths remain workspace-relative.
import sqlite3 as _bb_sqlite
import stat as _bb_stat

BB_DB_MAX_BYTES = 16 * 1024 * 1024
BB_DB_MAX_SQL_BYTES = 64 * 1024
BB_DB_MAX_PARAMS = 100
BB_DB_MAX_RESULT_ROWS = 1000
BB_DB_MAX_VALUE_BYTES = 1024 * 1024
BB_DB_BUSY_TIMEOUT = 2.0


class _BBDatabase:
    def __init__(self, connection, path):
        self.connection = connection
        self.path = str(path)
        self.closed = False
        self.query_only = False
        self.allow_transaction_control = False
        self.allow_savepoint_control = False
        self.connection.set_authorizer(self._authorize)

    def _authorize(self, action, arg1, arg2, db_name, trigger):
        always_deny = {
            getattr(_bb_sqlite, name)
            for name in (
                "SQLITE_ATTACH",
                "SQLITE_DETACH",
                "SQLITE_PRAGMA",
                "SQLITE_CREATE_VTABLE",
                "SQLITE_DROP_VTABLE",
            )
            if hasattr(_bb_sqlite, name)
        }

        if action in always_deny:
            return _bb_sqlite.SQLITE_DENY

        if action == getattr(_bb_sqlite, "SQLITE_TRANSACTION", -1):
            if not self.allow_transaction_control:
                return _bb_sqlite.SQLITE_DENY

        if action == getattr(_bb_sqlite, "SQLITE_SAVEPOINT", -1):
            if not self.allow_savepoint_control:
                return _bb_sqlite.SQLITE_DENY

        if action == getattr(_bb_sqlite, "SQLITE_FUNCTION", -1):
            function_name = str(arg2 or arg1 or "").lower()
            if function_name == "load_extension":
                return _bb_sqlite.SQLITE_DENY

        if self.query_only:
            write_actions = {
                getattr(_bb_sqlite, name)
                for name in (
                    "SQLITE_INSERT", "SQLITE_UPDATE", "SQLITE_DELETE",
                    "SQLITE_CREATE_INDEX", "SQLITE_CREATE_TABLE",
                    "SQLITE_CREATE_TEMP_INDEX", "SQLITE_CREATE_TEMP_TABLE",
                    "SQLITE_CREATE_TEMP_TRIGGER", "SQLITE_CREATE_TEMP_VIEW",
                    "SQLITE_CREATE_TRIGGER", "SQLITE_CREATE_VIEW",
                    "SQLITE_DROP_INDEX", "SQLITE_DROP_TABLE",
                    "SQLITE_DROP_TEMP_INDEX", "SQLITE_DROP_TEMP_TABLE",
                    "SQLITE_DROP_TEMP_TRIGGER", "SQLITE_DROP_TEMP_VIEW",
                    "SQLITE_DROP_TRIGGER", "SQLITE_DROP_VIEW",
                    "SQLITE_ALTER_TABLE", "SQLITE_REINDEX", "SQLITE_ANALYZE",
                )
                if hasattr(_bb_sqlite, name)
            }
            if action in write_actions:
                return _bb_sqlite.SQLITE_DENY

        return _bb_sqlite.SQLITE_OK


def _bb_db_handle(value):
    if not isinstance(value, _BBDatabase):
        raise TypeError("প্রথম argument একটি Database handle হতে হবে")
    if value.closed:
        raise ValueError("Database connection ইতিমধ্যে বন্ধ")
    return value


def _bb_db_sql(value):
    if not isinstance(value, str) or not value.strip():
        raise TypeError("SQL অবশ্যই non-empty String হতে হবে")
    if len(value.encode("utf-8")) > BB_DB_MAX_SQL_BYTES:
        raise ValueError("SQL statement size limit অতিক্রম করেছে")
    return value


def _bb_db_params(value):
    if not isinstance(value, list):
        raise TypeError("SQL parameters অবশ্যই List হতে হবে")
    if len(value) > BB_DB_MAX_PARAMS:
        raise ValueError("SQL parameter limit অতিক্রম করেছে")

    for item in value:
        if item is None or isinstance(item, (bool, int, float)):
            continue
        if isinstance(item, str):
            size = len(item.encode("utf-8"))
        elif isinstance(item, bytes):
            size = len(item)
        else:
            raise TypeError("শুধু null, Boolean, Number, String ও Bytes parameter অনুমোদিত")
        if size > BB_DB_MAX_VALUE_BYTES:
            raise ValueError("SQL parameter value size limit অতিক্রম করেছে")

    return value


def database_open(path):
    if not isinstance(path, str) or not path:
        raise TypeError("Database path অবশ্যই non-empty String হতে হবে")

    target = _bb_safe_path(path)

    if not target.name or target == target.parent:
        raise ValueError("Database path-এ filename থাকতে হবে")

    try:
        if target.is_symlink():
            raise ValueError("Database symlink অনুমোদিত নয়")

        if target.exists():
            info = target.lstat()
            if not _bb_stat.S_ISREG(info.st_mode):
                raise ValueError("Database path অবশ্যই regular file হতে হবে")
            if info.st_size > BB_DB_MAX_BYTES:
                raise ValueError("Database file size limit অতিক্রম করেছে")

        if not target.parent.is_dir():
            raise ValueError("Database parent directory পাওয়া যায়নি")

        connection = _bb_sqlite.connect(
            str(target),
            timeout=BB_DB_BUSY_TIMEOUT,
            isolation_level="DEFERRED",
        )
        connection.row_factory = _bb_sqlite.Row

        try:
            connection.enable_load_extension(False)

            # Set safe defaults before installing the SQL authorizer.
            connection.execute("PRAGMA trusted_schema=OFF")
            connection.execute("PRAGMA journal_mode=DELETE")

            page_size = connection.execute(
                "PRAGMA page_size"
            ).fetchone()[0]
            page_count = connection.execute(
                "PRAGMA page_count"
            ).fetchone()[0]

            max_pages = BB_DB_MAX_BYTES // page_size
            if page_count > max_pages:
                raise ValueError("Database page limit অতিক্রম করেছে")

            connection.execute(
                f"PRAGMA max_page_count={max_pages}"
            )

            limits = (
                ("SQLITE_LIMIT_LENGTH", BB_DB_MAX_VALUE_BYTES),
                ("SQLITE_LIMIT_SQL_LENGTH", BB_DB_MAX_SQL_BYTES),
                ("SQLITE_LIMIT_COLUMN", 100),
                ("SQLITE_LIMIT_EXPR_DEPTH", 100),
                ("SQLITE_LIMIT_COMPOUND_SELECT", 20),
                ("SQLITE_LIMIT_VDBE_OP", 25000),
                ("SQLITE_LIMIT_FUNCTION_ARG", 32),
                ("SQLITE_LIMIT_ATTACHED", 0),
                ("SQLITE_LIMIT_LIKE_PATTERN_LENGTH", 1000),
                ("SQLITE_LIMIT_VARIABLE_NUMBER", BB_DB_MAX_PARAMS),
            )
            for limit_name, limit_value in limits:
                limit_id = getattr(_bb_sqlite, limit_name, None)
                if limit_id is not None:
                    connection.setlimit(limit_id, limit_value)

            return _BBDatabase(connection, target)

        except Exception:
            connection.close()
            raise

    except (_bb_sqlite.Error, OSError) as error:
        raise ValueError(f"Database open failed: {error}") from None


def database_execute(db, sql, params):
    handle = _bb_db_handle(db)
    statement = _bb_db_sql(sql)
    values = _bb_db_params(params)

    handle.query_only = False
    savepoint_active = False
    cursor = None

    def internal_savepoint(sql_control):
        handle.allow_savepoint_control = True
        try:
            handle.connection.execute(sql_control)
        finally:
            handle.allow_savepoint_control = False

    try:
        if not handle.connection.in_transaction:
            handle.allow_transaction_control = True
            try:
                handle.connection.execute("BEGIN")
            finally:
                handle.allow_transaction_control = False

        internal_savepoint("SAVEPOINT bb_api_statement")
        savepoint_active = True

        try:
            cursor = handle.connection.execute(statement, values)

            if cursor.description is not None:
                raise ValueError(
                    "database_execute row-returning query গ্রহণ করে না; "
                    "database_query ব্যবহার করুন"
                )

            result = {
                "rowcount": cursor.rowcount,
                "lastrowid": cursor.lastrowid,
            }

            # Finalize the statement before releasing its savepoint.
            cursor.close()
            cursor = None

            internal_savepoint("RELEASE SAVEPOINT bb_api_statement")
            savepoint_active = False
            return result

        except Exception:
            # RETURNING statements may remain active until their cursor closes.
            if cursor is not None:
                try:
                    cursor.close()
                except _bb_sqlite.Error:
                    pass
                cursor = None

            if savepoint_active:
                try:
                    internal_savepoint(
                        "ROLLBACK TO SAVEPOINT bb_api_statement"
                    )
                    internal_savepoint(
                        "RELEASE SAVEPOINT bb_api_statement"
                    )
                    savepoint_active = False
                except _bb_sqlite.Error as cleanup_error:
                    raise ValueError(
                        f"Database statement rollback failed: {cleanup_error}"
                    ) from None
            raise

    except _bb_sqlite.Error as error:
        raise ValueError(f"Database execute failed: {error}") from None


def database_query(db, sql, params):
    handle = _bb_db_handle(db)
    statement = _bb_db_sql(sql)
    values = _bb_db_params(params)

    handle.query_only = True
    try:
        cursor = handle.connection.execute(statement, values)
        if cursor.description is None:
            raise ValueError("database_query শুধু row-returning query গ্রহণ করে")

        columns = [item[0] for item in cursor.description]
        if len(columns) != len(set(columns)):
            raise ValueError("Query result-এ duplicate column name অনুমোদিত নয়")

        rows = cursor.fetchmany(BB_DB_MAX_RESULT_ROWS + 1)
        if len(rows) > BB_DB_MAX_RESULT_ROWS:
            raise ValueError("Query result row limit অতিক্রম করেছে")

        return [dict(row) for row in rows]

    except _bb_sqlite.Error as error:
        raise ValueError(f"Database query failed: {error}") from None
    finally:
        handle.query_only = False


def database_commit(db):
    handle = _bb_db_handle(db)
    try:
        handle.allow_transaction_control = True
        try:
            handle.connection.commit()
        finally:
            handle.allow_transaction_control = False
        return True
    except _bb_sqlite.Error as error:
        raise ValueError(f"Database commit failed: {error}") from None


def database_rollback(db):
    handle = _bb_db_handle(db)
    try:
        handle.allow_transaction_control = True
        try:
            handle.connection.rollback()
        finally:
            handle.allow_transaction_control = False
        return True
    except _bb_sqlite.Error as error:
        raise ValueError(f"Database rollback failed: {error}") from None


def database_close(db):
    handle = _bb_db_handle(db)
    try:
        handle.connection.close()
        handle.closed = True
        return True
    except _bb_sqlite.Error as error:
        raise ValueError(f"Database close failed: {error}") from None


BUILTINS.update({
    "database_open": (1, database_open),
    "ডেটাবেস_খোলো": (1, database_open),
    "database_execute": (3, database_execute),
    "ডেটাবেস_চালাও": (3, database_execute),
    "database_query": (3, database_query),
    "ডেটাবেস_জিজ্ঞাসা": (3, database_query),
    "database_commit": (1, database_commit),
    "ডেটাবেস_কমিট": (1, database_commit),
    "database_rollback": (1, database_rollback),
    "ডেটাবেস_রোলব্যাক": (1, database_rollback),
    "database_close": (1, database_close),
    "ডেটাবেস_বন্ধ": (1, database_close),
})
