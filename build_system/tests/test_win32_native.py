import unittest

from runner.test_asserts import *

import build_system.constants as c
import build_system.build_executor as bex


class TestWin32Native(unittest.TestCase):

    def with_x64_defaults(self, params):
        x64_defaults = {
            "target": c.target_win32,
            "arch": c.arch_x64,
            "redirect_stdout": True,  # important for test-logging
        }
        params.update(x64_defaults)
        return params

    @expectOutput(
        r"\[WARNING\] Tests run: 9, Failures: 0, Errors: 0, Skipped: 9, Time elapsed: \d+.\d+ s - in com\.eclipsesource\.v8\.NodeJSTest")
    def test_x64_node_disabled(self):
        params = self.with_x64_defaults(
            {
                "buildsteps": ["j2v8", "test"],
                "j2v8test": "-Dtest=NodeJSTest",
            })

        bex.execute_build(params)

    @expectOutput(
        r"\[INFO\] Tests run: 9, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: \d+.\d+ s - in com\.eclipsesource\.v8\.NodeJSTest")
    def test_x64_node_enabled(self):
        params = self.with_x64_defaults(
            {
                "node_enabled": True,
                "buildsteps": ["j2v8", "test"],
                "j2v8test": "-Dtest=NodeJSTest",
            })

        bex.execute_build(params)
