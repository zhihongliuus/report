__author__ = 'frank'

from stat import S_ISDIR, ST_CTIME, ST_MODE
import os
import urlparse

OUTPUT = ""

def walk_suites(report_dir):
    suite_names = (os.path.join(report_dir, fn) for fn in os.listdir(report_dir))
    suite_names = ((os.stat(path), path) for path in suite_names)
    suite_names = ((stat[ST_CTIME], path) for stat, path in suite_names if S_ISDIR(stat(ST_MODE)))
    test_results = []
    for c_date, suite_name in sorted(suite_names):
        test_results.append(load_plugins(suite_name))
    pass

def walk_suite(suite_name):
    for testcase in os.listdir(suite_name):
        load_plugins(testcase)

def load_plugins(testcase):
    global OUTPUT
    for plugin in globals().keys():
        if plugin.startswith("plugin_"):
            OUTPUT += globals()[plugin](testcase)

def plugin_load_trace_log(testcase):
    """TraceLog"""
    result = ""
    for root, dir, files in os.walk(testcase):
        for name in files:
            if name.startswith("trace_log"):
                result += urlparse.urljoin(root, name)
    return result

def plugin_load_logcat_log(testcase):
    """Logcat"""
    result = ""
    for root, dir, files in os.walk(testcase):
        for name in files:
            if name.startswith("logcat"):
                result += urlparse.urljoin(root, name)
    return result

def plugin_load_screen_shot(testcase):
    """Screenshot"""
    result = ""
    for root, dir, files in os.walk(testcase):
        for name in files:
            if name.endswith("png"):
                result += urlparse.urljoin(root, name)
    return result

def plugin_load_calling_log(testcase):
    """Calling Log"""
    pass

def plugin_load_error_summary_log(testcase):
    """Error Summary"""
    pass

def plugin_load_carrier_name_log(testcase):
    """Carrier Nmae"""
    pass

if __name__ == "__main__":
    print plugin_load_carrier_name_log.__doc__