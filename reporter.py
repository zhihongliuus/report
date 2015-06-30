__author__ = 'frank'

from stat import S_ISDIR, ST_CTIME, ST_MODE
import os
import urlparse

HEAD = """
<!DOCTYPE html>
<html>
<head>
    <style>

        body {
            font:normal 68% verdana,arial,helvetica;
            color:#000000;
        }
        table tr td, table tr th {
            font-size: 68%;
        }
        table.details tr th{
            font-weight: bold;
            text-align:left;
            background:#a6caf0;
        }
        table.details tr td{
            background:#eeeee0;
        }

        p {
            line-height:1.5em;
            margin-top:0.5em; margin-bottom:1.0em;
        }
        h1 {
            margin: 0px 0px 5px; font: 165% verdana,arial,helvetica
        }
        h2 {
            margin-top: 1em; margin-bottom: 0.5em; font: bold 125% verdana,arial,helvetica
        }
        h3 {
            margin-bottom: 0.5em; font: bold 115% verdana,arial,helvetica
        }
        h4 {
            margin-bottom: 0.5em; font: bold 100% verdana,arial,helvetica
        }
        h5 {
            margin-bottom: 0.5em; font: bold 100% verdana,arial,helvetica
        }
        h6 {
            margin-bottom: 0.5em; font: bold 100% verdana,arial,helvetica
        }
        .Error {
            font-weight:bold; color:red;
        }
        .Failure {
            font-weight:bold; color:purple;
        }
        .NotRun {
            font-weight:bold; color:gray;
        }
        .Pass {
              color:black;
        }
        .Properties {
          text-align:right;
        }

        img {
            width:200px;
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


def sort_files(files):
    files = ((os.stat(path), path) for path in files)
    files = ((stat[ST_CTIME], path) for stat, path in files)
    return [file for c_data, file in sorted(files)]


def walk_suites(report_dir, f):
    os.chdir(report_dir)
    suite_names = (fn for fn in os.listdir(report_dir) if os.path.isdir(fn))
    output = "<thead><tr>"
    plugins = load_plugins()
    for plugin in plugins:
        output += "<th class=\"{class_name}\">{plugin_name}</th>".format(class_name=globals()[plugin].__doc__,
                                                                         plugin_name=globals()[plugin].__doc__)
    output += "</tr></thead>\n"
    f.write(output)
    for suite_name in sort_files(suite_names):
        walk_suite(suite_name, f)


def walk_suite(suite_name, f):
    plugins = load_plugins()
    f.write("<tbody>")
    for testcase in sorted(os.listdir(suite_name)):
        f.write("<tr>")
        for plugin in plugins:
            globals()[plugin](os.path.join(suite_name, testcase), f)
        f.write("</tr>")
    f.write("</tbody>\n")


def load_plugins():
    #    return [plugin for plugin in globals().keys() if plugin.startswith("plugin_")]
    return plugins


def plugin_load_case_name(testcase, f):
    """CaseName"""
    output = "<td>\n"
    output += "_".join(os.path.split(os.path.relpath(testcase))[-2:])
    output += "</td>\n"
    f.write(output)


def plugin_load_case_description(testcase, f):
    """Description"""
    f.write("<td></td>")


def plugin_load_case_result(testcase, f):
    """Result"""
    output = "<td class={0}>\n".format("TraceLog")
    for root, dir, files in os.walk(testcase):
        for name in files:
            if name == "report.xml":
                output += "<a href=\"{0}\">{1}</a>\n".format(os.path.join(root, name), name)
                break
    output += "</td>\n"
    f.write(output)


def plugin_load_trace_log(testcase, f):
    """TraceLog"""
    output = "<td class={0}>\n".format("TraceLog")
    for root, dir, files in os.walk(testcase):
        for name in files:
            if name.startswith("trace_log"):
                output += "<a href=\"{0}\">{1}</a>\n".format(os.path.join(root, name), name)
    output += "</td>\n"
    f.write(output)


def plugin_load_logcat_log(testcase, f):
    """Logcat"""
    output = "<td class={0}>\n".format("Logcat")
    for root, dir, files in os.walk(testcase):
        for name in files:
            if name.startswith("logcat"):
                output += "<a href=\"{0}\">{1}</a>\n".format(os.path.join(root, name), name)
    output += "</td>\n"
    f.write(output)


def plugin_load_screen_shot(testcase, f):
    """Screenshot"""
    output = "<td>\n"
    screenshots = []
    for root, dir, files in os.walk(testcase):
        for name in files:
            if name.endswith("png"):
                screenshots.append(os.path.join(root, name))
    for screenshot in sort_files(screenshots):
        output += "<a href=\"{src}\"><img src=\"{src}\" alt=\"{basename}\"></a>\n".format(src=screenshot,
                                                                                          basename=os.path.basename(
                                                                                              screenshot))
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


def plugin_load_error_summary_log(testcase, f):
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
        walk_suites(
            "/home/guest/Automation/repo_main_L/tests/common-baseline/UI-automation/automation-scripts/result-062515-20-43-36",
            f)
        f.write(FOOT)
        f.close()
