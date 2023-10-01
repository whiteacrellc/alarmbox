import os
import unittest
from alarmbox import AlarmBox  # Import the class containing _read_settings

class TestAlarmBox(unittest.TestCase):


    def setUp(self):

        self.test_file='test_settings.txt'
        file_contents = "KEY1=Value1\nKEY2=Value2\n"
        with open(self.test_file, 'w') as test_file:
            test_file.write(file_contents)
        self.alarmbox = AlarmBox(self.test_file)  # Replace YourClass with the actual class name

    def test_read_settings_valid(self):


        self.alarmbox._read_settings(self.test_file)

        self.assertEqual(self.alarmbox.settings['KEY1'], 'VALUE1')
        self.assertEqual(self.alarmbox.settings['KEY2'], 'VALUE2')

    def test_read_settings_empty_lines(self):
        file_contents = "\n  \nKEY1=Value1\n\nKEY2=Value2\n  \n"
        with open(self.test_file, 'w') as test_file:
            test_file.write(file_contents)

        self.alarmbox._read_settings(self.test_file)

        self.assertEqual(self.alarmbox.settings['KEY1'], 'VALUE1')
        self.assertEqual(self.alarmbox.settings['KEY2'], 'VALUE2')

    def tearDown(self):
        self.alarmbox = None
        # Clean up the test file if needed
        try:
            os.remove(self.test_file)
        except FileNotFoundError:
            pass

if __name__ == '__main__':
    unittest.main()
