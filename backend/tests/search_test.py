import unittest
from unittest.mock import Mock, patch
from common.exceptions import InternalServerError
from models.enums import Role, TournamentFormat, MatchFormat, TournamentStatus
from models.players import PlayerProfileImg
from models.tournaments import TournamentWithoutOwner
from models.users import User
from routers import search_router


class SearchRouter_Should(unittest.TestCase):
    @patch("routers.search_router.search_service")
    def test_usersSearch_raise_InternalServerError_when_dbError(self, mock_search_service):
        mock_search_service.get_users.side_effect = Mock(side_effect=Exception('Test'))
        with self.assertRaises(InternalServerError) as context:
            search_router.users_search("test")
        self.assertEqual("Loading users failed", context.exception.detail)
        self.assertEqual(500, context.exception.status_code)

    @patch("routers.search_router.search_service")
    def test_usersSearch_return_listUser_when_usersFound(self, mock_search_service):
        mock_search_service.get_users = lambda x: [User(id=1, username="username", email="email", role=Role.USER),
                                                   User(id=2, username="username2", email="email2", role=Role.USER)]

        result = search_router.users_search("test")
        expected = [search_router.users.User(id=1, username="username", email="email", role=Role.USER),
                    search_router.users.User(id=2, username="username2", email="email2", role=Role.USER)]
        self.assertEqual(result, expected)

    @patch("routers.search_router.search_service")
    def test_playersSearch_raise_InternalServerError_when_dbError(self, mock_search_service):
        mock_search_service.get_players.side_effect = Mock(side_effect=Exception('Test'))
        with self.assertRaises(InternalServerError) as context:
            search_router.players_search("test")
        self.assertEqual("Loading players failed", context.exception.detail)
        self.assertEqual(500, context.exception.status_code)

    @patch("routers.search_router.search_service")
    def test_playersSearch_return_listPlayerProfileImg_when_playersFound(self, mock_search_service):
        mock_search_service.get_players = lambda x: [PlayerProfileImg(id=1, full_name="fullname1"),
                                                     PlayerProfileImg(id=2, full_name="fullname2")]

        result = search_router.players_search("test")
        expected = [search_router.players.PlayerProfileImg(id=1, full_name="fullname1"),
                    search_router.players.PlayerProfileImg(id=2, full_name="fullname2")]
        self.assertEqual(result, expected)

    @patch("routers.search_router.search_service")
    def test_tournamentsSearch_raise_InternalServerError_when_dbError(self, mock_search_service):
        mock_search_service.get_tournaments.side_effect = Mock(side_effect=Exception('Test'))
        with self.assertRaises(InternalServerError) as context:
            search_router.tournaments_search("test")
        self.assertEqual("Loading tournaments failed", context.exception.detail)
        self.assertEqual(500, context.exception.status_code)

    @patch("routers.search_router.search_service")
    def test_tournamentsSearch_return_listTournamentWithoutOwner_when_tournamentsFound(self, mock_search_service):
        mock_search_service.get_tournaments = lambda x: [
            TournamentWithoutOwner(id=1, format=TournamentFormat.KNOCKOUT, match_format=MatchFormat.TIME,
                                   title='title1', rounds=3, third_place=0, status=TournamentStatus.OPEN),
            TournamentWithoutOwner(id=2, format=TournamentFormat.LEAGUE, match_format=MatchFormat.SCORE,
                                   title='title2', rounds=3, third_place=1, status=TournamentStatus.CLOSED)]

        result = search_router.tournaments_search("test")
        expected = [search_router.tournaments.TournamentWithoutOwner(id=1, format=TournamentFormat.KNOCKOUT,
                                                                     match_format=MatchFormat.TIME,
                                                                     title='title1', rounds=3, third_place=0,
                                                                     status=TournamentStatus.OPEN),
                    search_router.tournaments.TournamentWithoutOwner(id=2, format=TournamentFormat.LEAGUE,
                                                                     match_format=MatchFormat.SCORE,
                                                                     title='title2', rounds=3, third_place=1,
                                                                     status=TournamentStatus.CLOSED)]
        self.assertEqual(result, expected)
