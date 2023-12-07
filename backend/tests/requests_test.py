import unittest
from datetime import datetime, timedelta
from unittest.mock import Mock, patch, AsyncMock

import aiounittest

from common.exceptions import Unauthorized, BadRequest, NotFound, InternalServerError
from common.responses import RequestCreate
from models.enums import Role, Request
from models.players import PlayerRequest
from models.requests import DirectorRequest, LinkToPlayerRequest, TournamentRequest
from routers import requests_router


class RequestsRouter_Should(unittest.TestCase):
    def test_sendDirectorRequest_raise_BadRequest_when_userAdmin(self):
        with self.assertRaises(BadRequest) as context:
            requests_router.send_director_request(Mock(role=Role.ADMIN))
        self.assertEqual("Admins cannot send a director request", context.exception.detail)
        self.assertEqual(400, context.exception.status_code)

    def test_sendDirectorRequest_raise_BadRequest_when_userDirector(self):
        with self.assertRaises(BadRequest) as context:
            requests_router.send_director_request(Mock(role=Role.DIRECTOR))
        self.assertEqual("User is already a director", context.exception.detail)
        self.assertEqual(400, context.exception.status_code)

    @patch("routers.requests_router.requests_service")
    def test_sendDirectorRequest_return_RequestOK_when_successfulRequest(self, mock_requests_service):
        mock_requests_service.send_director_request = lambda x: None
        result = requests_router.send_director_request(Mock(role=Role.USER))
        self.assertEqual("Successfully sent a director request", result.body.decode())
        self.assertEqual(200, result.status_code)

    def test_getDirectorRequests_raise_Unauthorized_when_notAdmin(self):
        with self.assertRaises(Unauthorized) as context:
            requests_router.get_director_requests(Mock(role=Role.USER))
        self.assertEqual(context.exception.detail, "You are not authorized")
        self.assertEqual(context.exception.status_code, 401)

    @patch("routers.requests_router.requests_service")
    def test_getDirectorRequests_return_listDirectorRequest_when_requestsFound(self, mock_requests_service):
        date1 = datetime.utcnow() - timedelta(days=1)
        date2 = datetime.utcnow() - timedelta(days=2)
        mock_requests_service.get_director_requests = lambda: [
            DirectorRequest(id=1, user_id=2, email="email", status=Request.PENDING, created_at=date1),
            DirectorRequest(id=2, user_id=3, email="email", status=Request.ACCEPTED, created_at=date2)]
        result = requests_router.get_director_requests(Mock(role=Role.ADMIN))
        expected = [requests_router.requests.DirectorRequest(id=1, user_id=2, email="email", status=Request.PENDING,
                                                             created_at=date1),
                    requests_router.requests.DirectorRequest(id=2, user_id=3, email="email", status=Request.ACCEPTED,
                                                             created_at=date2)]
        self.assertEqual(expected, result)

    def test_rejectDirectorRequest_raise_Unauthorized_when_notAdmin(self):
        with self.assertRaises(Unauthorized) as context:
            requests_router.reject_director_request(1, Mock(role=Role.USER))
        self.assertEqual(context.exception.detail, "You are not authorized")
        self.assertEqual(context.exception.status_code, 401)

    @patch("routers.requests_router.requests_service")
    def test_rejectDirectorRequest_returns_RequestOK_when_requestRejected(self, mock_requests_service):
        mock_requests_service.reject_director_request = lambda x: None
        result = requests_router.reject_director_request(1, Mock(role=Role.ADMIN))
        self.assertEqual(result.body.decode(), "Director request rejected")
        self.assertEqual(result.status_code, 200)

    @patch("routers.requests_router.requests_service")
    def test_sendLinkToPlayerRequest_returns_RequestOK_when_requestSend(self, mock_requests_service):
        mock_requests_service.send_link_to_player_request = lambda x, y: None
        result = requests_router.send_link_to_player_request(Mock(full_name='test'), Mock())
        self.assertEqual(result.body.decode(), "Link to player request sent successfully")
        self.assertEqual(result.status_code, 200)

    def test_getLinkRequests_raise_Unauthorized_when_notAdmin(self):
        with self.assertRaises(Unauthorized) as context:
            requests_router.get_link_requests(Mock(role=Role.USER))
        self.assertEqual(context.exception.detail, "You are not authorized")
        self.assertEqual(context.exception.status_code, 401)

    @patch("routers.requests_router.requests_service")
    def test_getLinkRequests_returns_listLinkToPlayerRequest_when_requestsFound(self, mock_requests_service):
        date1 = datetime.utcnow() - timedelta(days=1)
        date2 = datetime.utcnow() - timedelta(days=2)
        mock_requests_service.get_link_requests = lambda: [
            LinkToPlayerRequest(id=1, user_id=2, username="username", requested_full_name="ful_name",
                                status=Request.PENDING, created_at=date1),
            LinkToPlayerRequest(id=2, user_id=3, username="username", requested_full_name="full_name",
                                status=Request.ACCEPTED, created_at=date2)]
        result = requests_router.get_link_requests(Mock(role=Role.ADMIN))
        expected = [requests_router.requests.LinkToPlayerRequest(id=1, user_id=2, username="username",
                                                                 requested_full_name="ful_name",
                                                                 status=Request.PENDING, created_at=date1),
                    requests_router.requests.LinkToPlayerRequest(id=2, user_id=3, username="username",
                                                                 requested_full_name="full_name",
                                                                 status=Request.ACCEPTED, created_at=date2)]
        self.assertEqual(expected, result)

    def test_rejectLinkPlayerRequest_raise_Unauthorized_when_notAdmin(self):
        with self.assertRaises(Unauthorized) as context:
            requests_router.reject_link_player_request(1, Mock(role=Role.USER))
        self.assertEqual(context.exception.detail, "You are not authorized")
        self.assertEqual(context.exception.status_code, 401)

    @patch("routers.requests_router.requests_service")
    def test_rejectLinkPlayerRequest_returns_RequestOK_when_requestRejected(self, mock_requests_service):
        mock_requests_service.reject_link_player_request = lambda x: None
        result = requests_router.reject_link_player_request(1, Mock(role=Role.ADMIN))
        self.assertEqual(result.body.decode(), "Link player request rejected")
        self.assertEqual(result.status_code, 200)

    @patch("routers.requests_router.players_service")
    def test_sendPlayerRequest_returns_RequestCreate_when_requestSend(self, mock_players_service):
        mock_players_service.send_player_request = lambda x, y: RequestCreate("Join request sent successfully")
        result = requests_router.send_player_request(1, Mock())
        self.assertEqual(result.body.decode(), "Join request sent successfully")
        self.assertEqual(result.status_code, 201)

    def test_getPlayerRequests_raise_Unauthorized_when_notAdmin(self):
        with self.assertRaises(Unauthorized) as context:
            requests_router.get_player_requests(Mock(role=Role.USER))
        self.assertEqual(context.exception.detail, "You are not authorized")
        self.assertEqual(context.exception.status_code, 401)

    @patch("routers.requests_router.players_service")
    def test_getPlayerRequests_returns_listPlayerRequest_when_requestsFound(self, mock_players_service):
        mock_players_service.get_all_player_requests = lambda: [
            PlayerRequest(id=1, requester_id=2, full_name="full_name", country='country', sports_club='sports_club',
                          status=Request.PENDING),
            PlayerRequest(id=2, requester_id=3, full_name="full_name", country='country', sports_club='sports_club',
                          status=Request.ACCEPTED)]
        result = requests_router.get_player_requests(Mock(role=Role.ADMIN))
        expected = [requests_router.players.PlayerRequest(id=1, requester_id=2, full_name="full_name",
                                                          country='country', sports_club='sports_club',
                                                          status=Request.PENDING),
                    requests_router.players.PlayerRequest(id=2, requester_id=3, full_name="full_name",
                                                          country='country', sports_club='sports_club',
                                                          status=Request.ACCEPTED)]
        self.assertEqual(expected, result)

    def test_rejectPlayerRequest_raise_Unauthorized_when_notAdmin(self):
        with self.assertRaises(Unauthorized) as context:
            requests_router.reject_player_request(1, Mock(role=Role.USER))
        self.assertEqual(context.exception.detail, "You are not authorized")
        self.assertEqual(context.exception.status_code, 401)

    @patch("routers.requests_router.players_service")
    def test_rejectPlayerRequest_returns_RequestOK_when_requestRejected(self, mock_players_service):
        mock_players_service.reject_player_request = lambda x: None
        result = requests_router.reject_player_request(1, Mock(role=Role.ADMIN))
        self.assertEqual(result.body.decode(), "Player request rejected")
        self.assertEqual(result.status_code, 200)

    @patch("routers.requests_router.players_service")
    def test_sendTournamentRequestNoPlayer_raise_BadRequest_when_userIsPlayer(self, mock_players_service):
        mock_players_service.get_player_by_user_id = lambda x: Mock()
        with self.assertRaises(BadRequest) as context:
            requests_router.send_tournament_request_no_player(1, Mock(), Mock())
        self.assertEqual(context.exception.detail, "User already have a player profile")
        self.assertEqual(context.exception.status_code, 400)

    @patch("routers.requests_router.players_service")
    def test_sendTournamentRequestNoPlayer_raise_InternalServerError_when_dbError(self, mock_players_service):
        mock_players_service.get_player_by_user_id = lambda x: None
        mock_players_service.create_tournament_join_request_no_player.side_effect = Mock(side_effect=Exception('Test'))
        with self.assertRaises(InternalServerError) as context:
            requests_router.send_tournament_request_no_player(1, Mock(), Mock())
        self.assertEqual(context.exception.detail, "Sending tournament request failed")
        self.assertEqual(context.exception.status_code, 500)

    @patch("routers.requests_router.players_service")
    def test_sendTournamentRequestNoPlayer_return_RequestOK_when_successfulRequest(self, mock_players_service):
        mock_players_service.get_player_by_user_id = lambda x: None
        mock_players_service.create_tournament_join_request_no_player = lambda x, y, z: None
        result = requests_router.send_tournament_request_no_player(1, Mock(), Mock())
        self.assertEqual(result.body.decode(), "Tournament request sent successfully")
        self.assertEqual(result.status_code, 200)

    @patch("routers.requests_router.players_service")
    def test_sendTournamentRequestWithPlayer_raise_BadRequest_when_userIsNotPlayer(self, mock_players_service):
        mock_players_service.get_player_by_user_id = lambda x: None
        with self.assertRaises(BadRequest) as context:
            requests_router.send_tournament_request_with_player(1, Mock())
        self.assertEqual(context.exception.detail, "User does not have a player profile")
        self.assertEqual(context.exception.status_code, 400)

    @patch("routers.requests_router.players_service")
    def test_sendTournamentRequestWithPlayer_raise_InternalServerError_when_dbError(self, mock_players_service):
        mock_players_service.get_player_by_user_id = lambda x: Mock()
        mock_players_service.create_tournament_join_request_with_player.side_effect = Mock(side_effect=Exception())
        with self.assertRaises(InternalServerError) as context:
            requests_router.send_tournament_request_with_player(1, Mock())
        self.assertEqual(context.exception.detail, "Sending tournament request failed")
        self.assertEqual(context.exception.status_code, 500)

    @patch("routers.requests_router.players_service")
    def test_sendTournamentRequestWithPlayer_return_RequestOK_when_successfulRequest(self, mock_players_service):
        mock_players_service.get_player_by_user_id = lambda x: Mock()
        mock_players_service.create_tournament_join_request_with_player = lambda x, y: None
        result = requests_router.send_tournament_request_with_player(1, Mock())
        self.assertEqual(result.body.decode(), "Tournament request sent successfully")
        self.assertEqual(result.status_code, 200)

    @patch("routers.requests_router.tournaments_service")
    def test_getTournamentRequests_raise_NotFound_when_noTournament(self, mock_tournaments_service):
        mock_tournaments_service.get_tournament_by_id = lambda x: None
        with self.assertRaises(NotFound) as context:
            requests_router.get_tournament_requests(1)
        self.assertEqual(context.exception.detail, "Tournament not found")
        self.assertEqual(context.exception.status_code, 404)

    @patch("routers.requests_router.tournaments_service")
    def test_getTournamentRequests_raise_InternalServerError_when_dbError(self, mock_tournaments_service):
        mock_tournaments_service.get_tournament_by_id = lambda x: Mock()
        mock_tournaments_service.get_tournament_requests.side_effect = Mock(side_effect=Exception('Test'))
        with self.assertRaises(InternalServerError) as context:
            requests_router.get_tournament_requests(1)
        self.assertEqual(context.exception.detail, "Retrieving requests failed")
        self.assertEqual(context.exception.status_code, 500)

    @patch("routers.requests_router.tournaments_service")
    def test_getTournamentRequests_returns_listTournamentRequest_when_requestsFound(self, mock_tournaments_service):
        mock_tournaments_service.get_tournament_by_id = lambda x: Mock()
        date1 = datetime.utcnow() - timedelta(days=1)
        date2 = datetime.utcnow() - timedelta(days=2)
        mock_tournaments_service.get_tournament_requests = lambda x: [
            TournamentRequest(id=1, player_id=2, tournament_id=x, user_id=5, full_name='full_name', country='country',
                              sports_club='sports_club', status=Request.PENDING, created_at=date1),
            TournamentRequest(id=2, player_id=3, tournament_id=x, user_id=6, full_name='full_name', country='country',
                              sports_club='sports_club', status=Request.ACCEPTED, created_at=date2)]
        result = requests_router.get_tournament_requests(7)
        expected = [requests_router.requests.TournamentRequest(id=1, player_id=2, tournament_id=7, user_id=5,
                                                               full_name='full_name', country='country',
                                                               sports_club='sports_club', status=Request.PENDING,
                                                               created_at=date1),
                    requests_router.requests.TournamentRequest(id=2, player_id=3, tournament_id=7, user_id=6,
                                                               full_name='full_name', country='country',
                                                               sports_club='sports_club', status=Request.ACCEPTED,
                                                               created_at=date2)]
        self.assertEqual(expected, result)

    def test_rejectTournamentRequets_raise_Unauthorized_when_notAdminNotDirector(self):
        with self.assertRaises(Unauthorized) as context:
            requests_router.reject_tournament_requets(1, Mock(role=Role.USER))
        self.assertEqual("You are not authorized", context.exception.detail)
        self.assertEqual(401, context.exception.status_code)

    @patch("routers.requests_router.tournaments_service")
    def test_rejectTournamentRequets_returns_RequestOK_when_requestRejected(self, mock_tournaments_service):
        mock_tournaments_service.reject_player_from_tournament = lambda x: None
        result = requests_router.reject_tournament_requets(1, Mock(role=Role.ADMIN))
        self.assertEqual("Player rejected from entering tournaments", result.body.decode())
        self.assertEqual(200, result.status_code)


class AsyncRequestsRouter_Should(aiounittest.AsyncTestCase):
    async def test_acceptDirectorRequest_raise_Unauthorized_when_notAdmin(self):
        with self.assertRaises(Unauthorized) as context:
            await requests_router.accept_director_request(1, Mock(role=Role.USER))
        self.assertEqual("You are not authorized", context.exception.detail)
        self.assertEqual(401, context.exception.status_code)

    async def test_acceptDirectorRequest_returns_RequestOK_when_requestAccepted(self):
        async_mock = AsyncMock()
        async_mock.side_effect = lambda x: None
        with patch("routers.requests_router.requests_service.accept_director_request", async_mock):
            result = await requests_router.accept_director_request(1, Mock(role=Role.ADMIN))
        self.assertEqual("Director request accepted", result.body.decode())
        self.assertEqual(200, result.status_code)

    async def test_acceptLinkPlayerRequest_raise_Unauthorized_when_notAdmin(self):
        with self.assertRaises(Unauthorized) as context:
            await requests_router.accept_link_player_request(1, Mock(role=Role.USER))
        self.assertEqual("You are not authorized", context.exception.detail)
        self.assertEqual(401, context.exception.status_code)

    async def test_acceptLinkPlayerRequest_returns_RequestOK_when_requestAccepted(self):
        async_mock = AsyncMock()
        async_mock.side_effect = lambda x, y: None
        with patch("routers.requests_router.requests_service.accept_link_player_request", async_mock):
            result = await requests_router.accept_link_player_request(1, Mock(role=Role.ADMIN))
        self.assertEqual("Link player request accepted", result.body.decode())
        self.assertEqual(200, result.status_code)

    async def test_acceptPlayerRequest_raise_Unauthorized_when_notAdmin(self):
        with self.assertRaises(Unauthorized) as context:
            await requests_router.accept_player_request(1, Mock(role=Role.USER))
        self.assertEqual("You are not authorized", context.exception.detail)
        self.assertEqual(401, context.exception.status_code)

    async def test_acceptPlayerRequest_returns_RequestOK_when_requestAccepted(self):
        async_mock = AsyncMock()
        async_mock.side_effect = lambda x: None
        with patch("routers.requests_router.players_service.accept_player_request", async_mock):
            result = await requests_router.accept_player_request(1, Mock(role=Role.ADMIN))
        self.assertEqual("Player request accepted", result.body.decode())
        self.assertEqual(200, result.status_code)

    async def test_acceptTournamentRequest_raise_Unauthorized_when_notAdminNotDirector(self):
        with self.assertRaises(Unauthorized) as context:
            await requests_router.accept_tournament_request(1, Mock(role=Role.USER))
        self.assertEqual("You are not authorized", context.exception.detail)
        self.assertEqual(401, context.exception.status_code)

    async def test_acceptTournamentRequest_returns_RequestOK_when_requestAccepted(self):
        async_mock = AsyncMock()
        async_mock.side_effect = lambda x: None
        with patch("routers.requests_router.tournaments_service.accept_player_to_tournament", async_mock):
            result = await requests_router.accept_tournament_request(1, Mock(role=Role.ADMIN))
        self.assertEqual("Player accepted in tournament", result.body.decode())
        self.assertEqual(200, result.status_code)
