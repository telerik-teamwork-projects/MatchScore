import unittest
from unittest.mock import Mock, patch
from common.exceptions import Unauthorized, BadRequest, NotFound, InternalServerError
from models.players import PlayerProfileImg

from routers import players_router

mock_admin = Mock(spec='routers.players_router.is_admin')
mock_director = Mock(spec='routers.players_router.is_director')
mock_pages = Mock(spec='routers.players_router.manage_pages')
players_router.is_admin = mock_admin
players_router.is_director = mock_director
players_router.manage_pages = mock_pages


class PlayersRouter_Should(unittest.TestCase):
    def setUp(self) -> None:
        mock_pages.reset_mock()
        mock_admin.reset_mock()
        mock_director.reset_mock()

    @patch("routers.players_router.players_service")
    def test_getPlayers_return_PaginatedPlayers(self, mock_players_service):
        mock_players_service.count_by_tournament.return_value = 10
        mock_pages.return_value = ((10,), (1, 1))
        player1 = PlayerProfileImg(id=1, full_name='Test 1')
        player2 = PlayerProfileImg(id=2, full_name='Test 2')
        mock_players_service.all.return_value = (player1, player2)
        result = players_router.get_players(1)
        expected = players_router.PaginatedPlayers(players=[player1, player2],
                                                   pagination=players_router.Pagination(page=1,
                                                                                        items_per_page=10,
                                                                                        total_pages=1))
        self.assertEqual(result, expected)

    @patch("routers.players_router.players_service")
    def test_getPlayerById_raise_NotFound_when_notPlayer(self, mock_players_service):
        mock_players_service.get_by_id = lambda x: None
        with self.assertRaises(NotFound) as context:
            players_router.get_player_by_id(1)
        self.assertEqual("Player 1 does not exist", context.exception.detail)
        self.assertEqual(404, context.exception.status_code)

    @patch("routers.players_router.players_service")
    def test_getPlayerById_return_PlayerProfileImg_when_player(self, mock_players_service):
        mock_players_service.get_by_id = lambda x: PlayerProfileImg(id=x, full_name='Test 1')
        result = players_router.get_player_by_id(2)
        expected = players_router.PlayerProfileImg(id=2, full_name='Test 1')
        self.assertEqual(result, expected)

    @patch("routers.players_router.players_service")
    def test_getAchievementsById_raise_NotFound_when_notPlayer(self, mock_players_service):
        mock_players_service.get_achievements = lambda x: None
        with self.assertRaises(NotFound) as context:
            players_router.get_achievements_by_id(1)
        self.assertEqual("Player 1 does not exist", context.exception.detail)
        self.assertEqual(404, context.exception.status_code)

    @patch("routers.players_router.players_service")
    def test_getAchievementsById_return_PlayerProfileImg_when_player(self, mock_players_service):
        mock_players_service.get_achievements = lambda x: PlayerProfileImg(id=x, full_name='Test 1')
        result = players_router.get_achievements_by_id(2)
        expected = players_router.PlayerProfileImg(id=2, full_name='Test 1')
        self.assertEqual(result, expected)

    @patch("routers.players_router.players_service")
    def test_playerUpdate_raise_NotFound_when_notPlayer(self, mock_players_service):
        mock_players_service.get_by_id = lambda x: None
        with self.assertRaises(NotFound) as context:
            players_router.player_update(1, 'test', 'test', 'test', 'test', Mock())
        self.assertEqual("Player with id 1 doesn't exist", context.exception.detail)
        self.assertEqual(404, context.exception.status_code)

    @patch("routers.players_router.players_service")
    def test_playerUpdate_raise_Unauthorized_when_notAuthorized(self, mock_players_service):
        mock_players_service.get_by_id = lambda x: Mock(id=x, user_id=1)
        mock_admin.return_value = False
        mock_director.return_value = False
        with self.assertRaises(Unauthorized) as context:
            players_router.player_update(2, 'test', 'test', 'test', 'test', Mock(id=5))
        self.assertEqual("You are not authorized", context.exception.detail)
        self.assertEqual(401, context.exception.status_code)

    @patch("routers.players_router.players_service")
    def test_playerUpdate_raise_BadRequest_when_newPlayerFullNameExists(self, mock_players_service):
        mock_players_service.get_by_id = lambda x: Mock(id=x, user_id=1, full_name='OldName')
        mock_admin.return_value = True
        mock_director.return_value = False
        mock_players_service.get_player_by_full_name = lambda x: Mock()
        with self.assertRaises(BadRequest) as context:
            players_router.player_update(2, 'NewName', 'test', 'test', 'test', Mock(id=5))
        self.assertEqual("Player with this full name already exists", context.exception.detail)
        self.assertEqual(400, context.exception.status_code)

    @patch("routers.players_router.players_service")
    def test_playerUpdate_return_PlayerProfileImg_when_playerUpdatedSuccessfully(self, mock_players_service):
        mock_players_service.get_by_id = lambda x: Mock(id=x, user_id=None, full_name='OldName')
        mock_admin.return_value = False
        mock_director.return_value = True
        mock_players_service.get_player_by_full_name = lambda x: None
        mock_players_service.handle_profile_image = lambda x: "Test path"
        mock_players_service.update = lambda a, b, c, d, e: PlayerProfileImg(id=a.id, full_name=b, country=c,
                                                                             sports_club=d, profile_img=e)
        result = players_router.player_update(2, 'NewName', 'test', 'test', 'test', Mock(id=5))
        expected = players_router.PlayerProfileImg(id=2, full_name='NewName', country='test', sports_club='test',
                                                   profile_img='Test path')
        self.assertEqual(result, expected)

    @patch("routers.players_router.players_service")
    def test_playerUpdate_raise_InternalServerError_when_dbError(self, mock_players_service):
        mock_players_service.get_by_id = lambda x: Mock(id=x, user_id=1, full_name='OldName')
        mock_admin.return_value = True
        mock_director.return_value = False
        mock_players_service.get_player_by_full_name = lambda x: None
        mock_players_service.handle_profile_image = lambda x: "Test path"
        mock_players_service.update.side_effect = Mock(side_effect=Exception('Test'))
        with self.assertRaises(InternalServerError) as context:
            players_router.player_update(2, 'NewName', 'test', 'test', 'test', Mock(id=5))
        self.assertEqual("Updating user failed", context.exception.detail)
        self.assertEqual(500, context.exception.status_code)
