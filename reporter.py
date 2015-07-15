# -*- coding: utf-8 -*-
__author__ = 'frank'

from stat import S_ISDIR, ST_CTIME, ST_MODE
import os
import re
from collections import OrderedDict

from flask import Flask
from flask import render_template

import yaml

app = Flask(__name__)
app.debug = True

config = yaml.load(file("config.yaml", 'r'))

class TestSuite:
    def __init__(self, suite_path):
        self.suite_path = suite_path
        self.suite_basename = os.path.basename(suite_path)
        self.suite_dirname = os.path.dirname(suite_path)

    def get_suite_name(self):
        self.suite_name = self.suite_basename

    def get_testcases(self):
        self.testcases = []
        for case_dir in sort_files(self.suite_path):
            tc = TestCase(case_dir)
            tc.build_case()
            self.testcases.append(tc)

    def build_suite(self):
        self.get_suite_name()
        self.get_test_cases()


class TestCase:
    def __init__(self, case_dir):
        self.case_dir = case_dir
        self.case_dirname = os.path.dirname(case_dir)
        self.case_basename = os.path.basename(case_dir)
        self.case_name = "_".join(os.path.basename(self.case_dirname), self.case_basename)

    def build_case(self):
        if search_files(self.case_dir, "report.xml"):
            report_file = search_files(self.case_dir, "report.xml")[0]
        if report_file:
            match = find_val_from_file(report_file, "description=\"(.*)\"")
            if match:
                self.desc = match.group(1)
            match = find_val_from_file(report_file, "result=\"(.*)\"")
            if match:
                self.result = match.group(1)




def find_val_from_file(file, pattern):
    results = []
    with open(file) as f:
        for line in f.readlines():
            if re.search(pattern, line):
                results.append(re.search(pattern, line))
    return results


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
    testcases = OrderedDict()
    suite_names = (fn for fn in os.listdir(test_report_dir) if os.path.isdir(fn))
    for suite_name in sort_files(suite_names):
        for testcase_path in sorted(os.listdir(suite_name)):
            testcase_status = get_case_status(testcase_path)
            testcases["_".join(os.path.split(testcase_path))] = testcase_status
    return testcases


def get_case_status(testcase_path):
    desc = ""
    result = ""
    if search_files(testcase_path, "report.xml"):
        report_file = search_files(testcase_path, "report.xml")[0]
    if report_file:
        match = find_val_from_file(report_file, "description=\"(.*)\"")
        if match:
            desc = match.group(1)
        match = find_val_from_file(report_file, "result=\"(.*)\"")
        if match:
            result = match.group(1)
    return testcase_path, desc, result


@app.route('/')
def index():
    report_dir = os.path.join(config["results_root_dir"]["repo_dir"], config["results_root_dir"]["auto_script_dir"])
    suite_dirs = (os.path.join(report_dir, fn) for fn in os.listdir(report_dir) if os.path.isdir(fn))
    testsuites = []
    for suite_dir in sort_files(suite_dirs):
        ts = TestSuite(suite_dir)
        ts.build_suite()
        testsuites.append()
    return render_template("reporter_template.html", testsuites=testsuites)



@app.route('/suites/<suites>')
def suites(suites):
    report_dir = os.path.join(config["results_root_dir"]["repo_dir"], config["results_root_dir"]["auto_script_dir"], suites)
    suite_dirs = (os.path.join(report_dir, fn) for fn in os.listdir(report_dir) if os.path.isdir(fn))
    testsuites = []
    for suite_dir in sort_files(suite_dirs):
        ts = TestSuite(suite_dir)
        ts.build_suite()
        testsuites.append()
    return render_template("reporter_template.html", testsuites=testsuites)


@app.route('/suites/cases')
def cases():
    return "Cases"


@app.route('/compare')
def compare():
    return "Compare"


@app.route("/test")
def test():
    return "test"

if __name__ == '__main__':
    app.run(host='0.0.0.0')


