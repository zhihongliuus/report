__author__ = 'frank'

from stat import S_ISDIR, ST_CTIME, ST_MODE
import os
import urlparse

HEAD = """
<!DOCTYPE html>
<html>
<head>
<style>
table {
  border-collapse: collapse;
}

td, th {
  border: 1px solid #999;
  padding: 0.5rem;
  text-align: left;
}
</style>
</head>
<body>
<table>
"""

FOOT = """</table>
</body>
</html>
"""

plugins = ["plugin_load_case_name",
#           "plugin_load_case_description",
           "plugin_load_case_result",
           "plugin_load_trace_log",
           "plugin_load_logcat_log",
           "plugin_load_screen_shot",
           "plugin_load_calling_log",
           "plugin_load_error_summary_log",
           "plugin_load_carrier_name_log"]

def walk_suites(report_dir, f):
    suite_names = (os.path.join(report_dir, fn) for fn in os.listdir(report_dir))
    suite_names = ((os.stat(path), path) for path in suite_names)
    suite_names = ((stat[ST_CTIME], path) for stat, path in suite_names if S_ISDIR(stat[ST_MODE]))
    output = "<thead><tr>"
    plugins = load_plugins()
    for plugin in plugins:
        output += "<th class=\"{class_name}\">{plugin_name}</th>".format(class_name=globals()[plugin].__doc__, plugin_name=globals()[plugin].__doc__)
    output += "</tr></thead>\n"
    f.write(output)
    for c_date, suite_name in sorted(suite_names):
        walk_suite(suite_name, f)

def walk_suite(suite_name, f):
    plugins = load_plugins()
    output = "<tbody><tr>"
    for testcase in os.listdir(suite_name):
        for plugin in plugins:
            globals()[plugin](os.path.join(suite_name, testcase), f)
    output += "</tr></tbody>\n"
    f.write(output)

def load_plugins():
#    return [plugin for plugin in globals().keys() if plugin.startswith("plugin_")]
    return plugins

def plugin_load_case_name(testcase, f):
    """CaseName"""
    pass

def plugin_load_case_description(testcase, f):
    """Description"""
    pass

def plugin_load_case_result(tescase, f):
    """Result"""
    pass

def plugin_load_trace_log(testcase, f):
    """TraceLog"""
    output = "<td class={0}>\n".format("TraceLog")
    for root, dir, files in os.walk(testcase):
        for name in files:
            if name.startswith("trace_log"):
                output += "<a href=\"{0}\">{1}</a>".format(urlparse.urljoin(root, name), name)
    output += "</td>\n"
    f.write(output)

def plugin_load_logcat_log(testcase, f):
    """Logcat"""
    output = "<td class={0}>\n".format("Logcat")
    for root, dir, files in os.walk(testcase):
        for name in files:
            if name.startswith("logcat"):
                output += "<a href=\"{0}\">{1}</a>".format(urlparse.urljoin(root, name), name)
    output += "</td>\n"
    f.write(output)

def plugin_load_screen_shot(testcase,f):
    """Screenshot"""
    output = "<td>\n"
    for root, dir, files in os.walk(testcase):
        for name in files:
            if name.endswith("png"):
                output += "<a href=\"{0}\">{1}</a>".format(urlparse.urljoin(root, name), name)
    output += "</td>\n"
    f.write(output)

def plugin_load_calling_log(testcase, f):
    """CallingLog"""
    output = "<td>\n"
    for root, dir, files in os.walk(testcase):
        for name in files:
            if name.endswith("png"):
                pass
    output += "</td>\n"
    f.write(output)

def plugin_load_error_summary_log(testcase,f):
    """ErrorSummary"""
    output = "<td>\n"
    for root, dir, files in os.walk(testcase):
        for name in files:
            if name.endswith("png"):
                pass
    output += "</td>\n"
    f.write(output)

def plugin_load_carrier_name_log(testcase, f):
    """CarrierNmae"""
    output = "<td>\n"
    for root, dir, files in os.walk(testcase):
        for name in files:
            if name.endswith("png"):
                pass
    output += "</td>\n"
    f.write(output)




if __name__ == "__main__":


    reporter_file_name = "enhanced_report.html"

    with open(reporter_file_name, 'w') as f:
        f.write(HEAD)
        walk_suites("/home/guest/Automation/repo_main_L/tests/common-baseline/UI-automation/automation-scripts/result-062515-20-43-36", f)
        f.write(FOOT)
        f.close()