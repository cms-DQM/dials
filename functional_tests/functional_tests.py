from selenium import webdriver
import unittest


class NewVisitorTest(unittest.TestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        print("Living browser")
        self.browser.quit()

    def test_can_start_browser(self):
        self.browser.get("http://localhost:8000")
        print("Localhost successfully opened")

        self.assertIn("Home", self.browser.title)

        self.fail("Finish the test!")

if __name__ == '__main__':
    unittest.main(warnings='ignore')

