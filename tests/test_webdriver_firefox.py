# -*- coding: utf-8 -*-
import os

try:
    import unittest2 as unittest
except ImportError:
    import unittest

from splinter.browser import Browser
from fake_webapp import EXAMPLE_APP
from base import WebDriverTests
from tests import Namespace

ns = Namespace()


def setUpModule():
    ns.browser = Browser('firefox')


def tearDownModule():
    ns.browser.quit()


class FirefoxBrowserTest(WebDriverTests, unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.browser = ns.browser

    def setUp(self):
        self.browser.visit(EXAMPLE_APP)

    def test_attach_file(self):
        "should provide a way to change file field value"
        file_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'mockfile.txt')
        self.browser.attach_file('file', file_path)
        self.browser.find_by_name('upload').first.click()

        html = self.browser.html
        assert 'text/plain' in html
        assert open(file_path).read() in html

    def test_mouse_over(self):
        "Firefox should not support mouseover"
        with self.assertRaises(NotImplementedError):
            self.browser.find_by_id('visible').first.mouse_over()

    def test_mouse_out(self):
        "Firefox should not support mouseout"
        with self.assertRaises(NotImplementedError):
            self.browser.find_by_id('visible').first.mouse_out()

    def test_double_click(self):
        "Firefox should not support double_click"
        with self.assertRaises(NotImplementedError):
            self.browser.find_by_id('visible').double_click()

    def test_right_click(self):
        "Firefox should not support right_click"
        with self.assertRaises(NotImplementedError):
            self.browser.find_by_id('visible').right_click()

    def test_drag_and_drop(self):
        "Firefox should not support drag_and_drop"
        with self.assertRaises(NotImplementedError):
            droppable = self.browser.find_by_css('.droppable')
            self.browser.find_by_css('.draggable').drag_and_drop(droppable)

    def test_mouseover_should_be_an_alias_to_mouse_over_and_be_deprecated(self):
        "Firefox should not support mouseover"
        with self.assertRaises(NotImplementedError):
            self.browser.find_by_id('visible').mouseover()

    def test_mouseout_should_be_an_alias_to_mouse_out_and_be_deprecated(self):
        "Firefox should not support mouseout"
        with self.assertRaises(NotImplementedError):
            self.browser.find_by_id('visible').mouseout()


class FirefoxWithExtensionTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        extension_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'firebug.xpi')
        cls.browser = Browser('firefox', extensions=[extension_path])

    def test_create_a_firefox_instance_with_extension(self):
        "should be able to load an extension"
        self.assertIn('firebug@software.joehewitt.com', os.listdir(self.browser.driver.profile.extensionsDir))

    @classmethod
    def tearDownClass(cls):
        cls.browser.quit()
