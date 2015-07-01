__author__ = 'frank'

from stat import S_ISDIR, ST_CTIME, ST_MODE
import os
import re

from jinja2 import Template

REPORT_HEADS = ["Testcase",
                "Description",
                "Result",
                "Screenshots"]



def sort_files(files):
    files = ((os.stat(path), path) for path in files)
    files = ((stat[ST_CTIME], path) for stat, path in files)
    return [file for c_data, file in sorted(files)]


def search_files(root_dir, pattern):
    results = []
    for root, dir, files in os.walk(root_dir):
        for name in files:
            if pattern in name:
                results.append(os.path.join(root, name))
    return results

def get_testcases(test_report_dir):
    testcases = []
    suite_names = (fn for fn in os.listdir(test_report_dir) if os.path.isdir(fn))
    for suite_name in sort_files(suite_names):
        for testcase in sorted(os.listdir(suite_name)):
            testcases.append(("_".join(os.path.split(testcase), testcase)))
    return testcases






# plugins = ["plugin_load_case_name",
#            "plugin_load_case_description",
#            "plugin_load_case_result",
#            "plugin_load_trace_log",
#            "plugin_load_logcat_log",
#            "plugin_load_screen_shot",
#            "plugin_load_calling_log",
#            "plugin_load_error_summary_log",
#            "plugin_load_carrier_name_log"]

#
# def walk_suites(report_dir, f):
#     os.chdir(report_dir)
#     suite_names = (fn for fn in os.listdir(report_dir) if os.path.isdir(fn))
#     output = "<thead><tr>"
#     plugins = load_plugins()
#     for plugin in plugins:
#         output += "<th class=\"{class_name}\">{plugin_name}</th>".format(class_name=globals()[plugin].__doc__,
#                                                                          plugin_name=globals()[plugin].__doc__)
#     output += "</tr></thead>\n"
#     f.write(output)
#     for suite_name in sort_files(suite_names):
#         walk_suite(suite_name, f)
#
#
# def walk_suite(suite_name, f):
#     plugins = load_plugins()
#     f.write("<tbody>")
#     for testcase in sorted(os.listdir(suite_name)):
#         f.write("<tr>")
#         for plugin in plugins:
#             globals()[plugin](os.path.join(suite_name, testcase), f)
#         f.write("</tr>")
#     f.write("</tbody>\n")
#
#
# def load_plugins():
#     #    return [plugin for plugin in globals().keys() if plugin.startswith("plugin_")]
#     return plugins
#
#
# def plugin_load_case_name(testcase, f):
#     """CaseName"""
#     output = "<td>\n"
#     output += "_".join(os.path.split(os.path.relpath(testcase))[-2:])
#     output += "</td>\n"
#     f.write(output)
#
#
# def plugin_load_case_description(testcase, f):
#     """Description"""
#     f.write("<td></td>")
#
#
# def plugin_load_case_result(testcase, f):
#     """Result"""
#     output = "<td class={0}>\n".format("TraceLog")
#     for root, dir, files in os.walk(testcase):
#         for name in files:
#             if name == "report.xml":
#                 output += "<a href=\"{0}\">{1}</a>\n".format(os.path.join(root, name), name)
#                 break
#     output += "</td>\n"
#     f.write(output)
#
#
# def plugin_load_trace_log(testcase, f):
#     """TraceLog"""
#     output = "<td class={0}>\n".format("TraceLog")
#     for root, dir, files in os.walk(testcase):
#         for name in files:
#             if name.startswith("trace_log"):
#                 output += "<a href=\"{0}\">{1}</a>\n".format(os.path.join(root, name), name)
#     output += "</td>\n"
#     f.write(output)
#
#
# def plugin_load_logcat_log(testcase, f):
#     """Logcat"""
#     output = "<td class={0}>\n".format("Logcat")
#     for root, dir, files in os.walk(testcase):
#         for name in files:
#             if name.startswith("logcat"):
#                 output += "<a href=\"{0}\">{1}</a>\n".format(os.path.join(root, name), name)
#     output += "</td>\n"
#     f.write(output)
#
#
# def plugin_load_screen_shot(testcase, f):
#     """Screenshot"""
#     output = "<td>\n"
#     screenshots = []
#     for root, dir, files in os.walk(testcase):
#         for name in files:
#             if name.endswith("png"):
#                 screenshots.append(os.path.join(root, name))
#     for screenshot in sort_files(screenshots):
#         output += "<a href=\"{src}\"><img src=\"{src}\" alt=\"{basename}\"></a>\n".format(src=screenshot,
#                                                                                           basename=os.path.basename(
#                                                                                               screenshot))
#     output += "</td>\n"
#     f.write(output)
#
#
# def plugin_load_calling_log(testcase, f):
#     """CallingLog"""
#     output = "<td>\n"
#     for root, dir, files in os.walk(testcase):
#         for name in files:
#             if name.endswith("png"):
#                 pass
#     output += "</td>\n"
#     f.write(output)
#
#
# def plugin_load_error_summary_log(testcase, f):
#     """ErrorSummary"""
#     output = "<td>\n"
#     for root, dir, files in os.walk(testcase):
#         for name in files:
#             if name.endswith("png"):
#                 pass
#     output += "</td>\n"
#     f.write(output)
#
#
# def plugin_load_carrier_name_log(testcase, f):
#     """CarrierNmae"""
#     output = "<td>\n"
#     for root, dir, files in os.walk(testcase):
#         for name in files:
#             if name.endswith("png"):
#                 pass
#     output += "</td>\n"
#     f.write(output)
#

