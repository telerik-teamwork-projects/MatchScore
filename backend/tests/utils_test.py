import unittest
from unittest.mock import Mock, patch, mock_open
import common.utils as utils
from models.enums import Role


class Utils_Should(unittest.TestCase):

    def test_isAdmin_returns_True_when_admin(self):
        self.assertTrue(utils.is_admin(Mock(role=Role.ADMIN)))

    def test_isAdmin_returns_False_when_notAdmin(self):
        self.assertFalse(utils.is_admin(Mock(role=Role.USER)))

    def test_isDirector_returns_True_when_director(self):
        self.assertTrue(utils.is_director(Mock(role=Role.DIRECTOR)))

    def test_isADirector_returns_False_when_notDirector(self):
        self.assertFalse(utils.is_director(Mock(role=Role.USER)))

    def test_isPowerOfTwo_returns_True_when_isValid(self):
        self.assertTrue(utils.is_power_of_two(8))

    def test_isPowerOfTwo_returns_False_when_notValid(self):
        self.assertFalse(utils.is_power_of_two(7))

    def test_isPowerOfTwo_returns_False_when_lessThanTwo(self):
        self.assertFalse(utils.is_power_of_two(1))

    def test_managePages_returns_correctPageParameters_when_validInput(self):
        result = utils.manage_pages(2, 20)
        expected = ((10, 10), (2, 2))
        self.assertEqual(expected, result)

    def test_managePages_returns_correctPageParameters_when_invalidInput_pageGreaterThanTotal(self):
        result = utils.manage_pages(4, 5)
        expected = ((0, 10), (1, 1))
        self.assertEqual(expected, result)

    def test_managePages_returns_correctPageParameters_when_invalidInput_pageLessThanOne(self):
        result = utils.manage_pages(0, 5)
        expected = ((0, 10), (1, 1))
        self.assertEqual(expected, result)

    def test_managePages_returns_correctPageParameters_when_matchLimit(self):
        result = utils.manage_pages(2, 20, match_limit=True)
        expected = ((0, 40), (1, 1))
        self.assertEqual(expected, result)

    def test_managePages_returns_correctPageParameters_when_matchTournamentLimit(self):
        result = utils.manage_pages(2, 20, match_tournament_limit=True)
        expected = ((0, 20), (1, 1))
        self.assertEqual(expected, result)

    def test_saveImage_returns_emptyString_when_fileNone(self):
        result = utils.save_image(None, "folder")
        self.assertEqual("", result)

    @patch("common.utils.os", autospec=True)
    def test_saveImage_returns_correctPath_when_fileNotNone(self, mock_os):
        open_mock = mock_open()
        mock_os.path.join.return_value = 'media/folder/filename'
        mock_os.makedirs.return_value = None
        with patch("common.utils.open", open_mock, create=True):
            result = utils.save_image(Mock(filename='filename'), "folder")
            _, main_dir, folder, file_name = result.split('/')
            _, file_name = file_name.split("_")
            self.assertEqual('media/folder/filename', f'{main_dir}/{folder}/{file_name}')

        open_mock.assert_called_with('media/folder/filename', "wb")
