import unittest
from datetime import datetime, timedelta
from unittest.mock import Mock, patch, AsyncMock

import aiounittest

from common.exceptions import Unauthorized, BadRequest, NotFound
from models.matches import Match, MatchResponse, MatchBase, MatchTournamentResponse
from routers import matches_router

mock_admin = Mock(spec='routers.matches_router.is_admin')
mock_director = Mock(spec='routers.matches_router.is_director')
mock_pages = Mock(spec='routers.matches_router.manage_pages')
matches_router.is_admin = mock_admin
matches_router.is_director = mock_director
matches_router.manage_pages = mock_pages


def fake_match(players: list[str]):
    mock_match = Mock(spec=Match)
    mock_match.participants = [Mock(full_name=name) for name in players]
    return mock_match


class MatchesRouter_Should(unittest.TestCase):
    def setUp(self) -> None:
        mock_pages.reset_mock()
        mock_admin.reset_mock()
        mock_director.reset_mock()

    def test_createMatch_raise_Unauthorized_when_notAdminsNotDirector(self):
        mock_admin.return_value = False
        mock_director.return_value = False
        with self.assertRaises(Unauthorized) as context:
            matches_router.create_match(Mock(), Mock())
        self.assertEqual("User has insufficient privileges", context.exception.detail)
        self.assertEqual(401, context.exception.status_code)

    def test_createMatch_raise_BadRequest_when_notUniqueParticipants(self):
        mock_admin.return_value = True
        mock_match = fake_match(['name', 'name'])
        with self.assertRaises(BadRequest) as context:
            matches_router.create_match(mock_match, Mock())
        self.assertEqual("Participants should be unique!", context.exception.detail)
        self.assertEqual(400, context.exception.status_code)

    def test_createMatch_raise_BadRequest_when_participantsLessThanTwo(self):
        mock_director.return_value = True
        mock_match = fake_match(['name'])
        with self.assertRaises(BadRequest) as context:
            matches_router.create_match(mock_match, Mock())
        self.assertEqual("Participants must be at least 2!", context.exception.detail)
        self.assertEqual(400, context.exception.status_code)

    @patch("routers.matches_router.matches_service")
    def test_createMatch_returns_MatchResponse_when_matchCreated(self, mock_matches_service):
        mock_director.return_value = True
        mock_match = fake_match(['name1', 'name2'])
        date = datetime.utcnow()
        mock_matches_service.create = lambda x: MatchResponse.from_query_result(1, date, 'time')
        result = matches_router.create_match(mock_match, Mock())
        expected = matches_router.MatchResponse(id=1, date=date, format='Time limited', participants=[], score=[])
        self.assertEqual(result, expected)

    def test_updateDate_raise_Unauthorized_when_notAdminsNotDirector(self):
        mock_admin.return_value = False
        mock_director.return_value = False
        with self.assertRaises(Unauthorized) as context:
            matches_router.update_date(1, Mock(), Mock())
        self.assertEqual("User has insufficient privileges", context.exception.detail)
        self.assertEqual(401, context.exception.status_code)

    @patch("routers.matches_router.matches_service")
    def test_updateDate_raise_NotFound_when_notMatch(self, mock_matches_service):
        mock_admin.return_value = True
        mock_director.return_value = False
        mock_matches_service.find = lambda x: None
        with self.assertRaises(NotFound) as context:
            matches_router.update_date(1, Mock(), Mock())
        self.assertEqual("Match 1 does not exist", context.exception.detail)
        self.assertEqual(404, context.exception.status_code)

    @patch("routers.matches_router.matches_service")
    def test_updateDate_raise_BadRequest_when_matchTournament(self, mock_matches_service):
        mock_admin.return_value = False
        mock_director.return_value = True
        mock_matches_service.find = lambda x: Mock(tournaments_id=1)
        with self.assertRaises(BadRequest) as context:
            matches_router.update_date(1, Mock(), Mock())
        self.assertEqual("The date cannot be changed! The match is part of tournament!", context.exception.detail)
        self.assertEqual(400, context.exception.status_code)

    @patch("routers.matches_router.matches_service")
    def test_updateDate_raise_BadRequest_when_dateIsNotFuture(self, mock_matches_service):
        mock_admin.return_value = False
        mock_director.return_value = True
        mock_matches_service.find = lambda x: Mock(tournaments_id=None)
        with self.assertRaises(BadRequest) as context:
            matches_router.update_date(1, Mock(date=(datetime.utcnow() - timedelta(days=1))), Mock())
        self.assertEqual("The new match date should be in the future!", context.exception.detail)
        self.assertEqual(400, context.exception.status_code)

    @patch("routers.matches_router.matches_service")
    def test_updateDate_return_MatchBase_when_newDateIsOldDate(self, mock_matches_service):
        mock_admin.return_value = True
        mock_director.return_value = False
        date = (datetime.utcnow() + timedelta(days=1))
        mock_matches_service.find = lambda x: MatchBase(id=x, date=date, format="time")
        result = matches_router.update_date(1, Mock(date=date), Mock())
        expected = MatchBase(id=1, date=date, format='time')
        self.assertEqual(result, expected)

    @patch("routers.matches_router.matches_service")
    def test_updateDate_return_MatchBase_when_newDate(self, mock_matches_service):
        mock_admin.return_value = False
        mock_director.return_value = True
        date = (datetime.utcnow() + timedelta(days=1))
        mock_matches_service.find = lambda x: MatchBase(id=x, date=date, format="time")
        mock_matches_service.update_date = lambda x, y: MatchBase(id=x.id, date=y.date, format=x.format)
        result = matches_router.update_date(1, Mock(date=(date + timedelta(days=1))), Mock())
        expected = MatchBase(id=1, date=date + timedelta(days=1), format='time')
        self.assertEqual(result, expected)

    def test_updatePlayers_raise_Unauthorized_when_notAdminsNotDirector(self):
        mock_admin.return_value = False
        mock_director.return_value = False
        with self.assertRaises(Unauthorized) as context:
            matches_router.update_players(1, Mock(), Mock())
        self.assertEqual("User has insufficient privileges", context.exception.detail)
        self.assertEqual(401, context.exception.status_code)

    @patch("routers.matches_router.matches_service")
    def test_updatePlayers_raise_NotFound_when_notMatch(self, mock_matches_service):
        mock_admin.return_value = True
        mock_director.return_value = False
        mock_matches_service.find = lambda x: None
        with self.assertRaises(NotFound) as context:
            matches_router.update_players(1, Mock(), Mock())
        self.assertEqual("Match 1 does not exist", context.exception.detail)
        self.assertEqual(404, context.exception.status_code)

    @patch("routers.matches_router.matches_service")
    def test_updatePlayers_raise_BadRequest_when_matchTournament(self, mock_matches_service):
        mock_admin.return_value = False
        mock_director.return_value = True
        mock_matches_service.find = lambda x: Mock(tournaments_id=1)
        with self.assertRaises(BadRequest) as context:
            matches_router.update_players(1, Mock(), Mock())
        self.assertEqual("The participants cannot be changed! The match is part of tournament!",
                         context.exception.detail)
        self.assertEqual(400, context.exception.status_code)

    @patch("routers.matches_router.matches_service")
    def test_updatePlayers_raise_BadRequest_when_newParticipantsNotUnique(self, mock_matches_service):
        mock_admin.return_value = False
        mock_director.return_value = True
        mock_matches_service.find = lambda x: Mock(tournaments_id=None)
        mock_match_players = [Mock(player=1, player_prev=1), Mock(player=1, player_prev=2)]
        with self.assertRaises(BadRequest) as context:
            matches_router.update_players(1, mock_match_players, Mock())
        self.assertEqual("Participants should be unique!", context.exception.detail)
        self.assertEqual(400, context.exception.status_code)

    @patch("routers.matches_router.matches_service")
    def test_updatePlayers_raise_BadRequest_when_oldParticipantsNotUnique(self, mock_matches_service):
        mock_admin.return_value = False
        mock_director.return_value = True
        mock_matches_service.find = lambda x: Mock(tournaments_id=None)
        mock_match_players = [Mock(player=2, player_prev=2), Mock(player=1, player_prev=2)]
        with self.assertRaises(BadRequest) as context:
            matches_router.update_players(1, mock_match_players, Mock())
        self.assertEqual("Participants should be unique!", context.exception.detail)
        self.assertEqual(400, context.exception.status_code)

    @patch("routers.matches_router.matches_service")
    def test_updatePlayers_raise_BadRequest_when_participantsNotNew(self, mock_matches_service):
        mock_admin.return_value = True
        mock_director.return_value = False
        mock_matches_service.find = lambda x: Mock(tournaments_id=None)
        mock_match_players = [Mock(player=1, player_prev=2), Mock(player=3, player_prev=4)]
        mock_matches_service.find_participants = lambda x, y: "test"
        with self.assertRaises(BadRequest) as context:
            matches_router.update_players(1, mock_match_players, Mock())
        self.assertEqual("The participants provided already play in this match!", context.exception.detail)
        self.assertEqual(400, context.exception.status_code)

    @patch("routers.matches_router.matches_service")
    def test_updatePlayers_raise_BadRequest_when_participantsNotInMatch(self, mock_matches_service):
        mock_admin.return_value = True
        mock_director.return_value = False
        mock_matches_service.find = lambda x: Mock(tournaments_id=None)
        mock_match_players = [Mock(player=1, player_prev=2), Mock(player=3, player_prev=4)]
        mock_matches_service.find_participants.side_effect = [None, None]
        with self.assertRaises(BadRequest) as context:
            matches_router.update_players(1, mock_match_players, Mock())
        self.assertEqual("The participants to be updated do not play in this match!", context.exception.detail)
        self.assertEqual(400, context.exception.status_code)

    @patch("routers.matches_router.matches_service")
    def test_updatePlayers_return_MatchResponse_when_participantsUpdated(self, mock_matches_service):
        mock_admin.return_value = True
        mock_director.return_value = False
        mock_matches_service.find = lambda x: Mock(id=x, tournaments_id=None)
        date = datetime.utcnow()
        mock_match_players = [Mock(player=1, player_prev=2), Mock(player=3, player_prev=4)]
        mock_matches_service.find_participants.side_effect = [None, 'test']
        mock_matches_service.update_players = lambda x, y: MatchResponse.from_query_result(x.id, date, "time")
        result = matches_router.update_players(1, mock_match_players, Mock())
        expected = matches_router.MatchResponse(id=1, date=date, format='Time limited', participants=[], score=[])
        self.assertEqual(result, expected)

    @patch("routers.matches_router.matches_service")
    def test_getMatchByid_raise_NotFound_when_notMatch(self, mock_matches_service):
        mock_matches_service.get_by_id = lambda x: None
        with self.assertRaises(NotFound) as context:
            matches_router.get_match_by_id(1)
        self.assertEqual("Match 1 does not exist", context.exception.detail)
        self.assertEqual(404, context.exception.status_code)

    @patch("routers.matches_router.matches_service")
    def test_getMatchByid_return_MatchTournamentResponse_when_match(self, mock_matches_service):
        date = datetime.utcnow()
        mock_matches_service.get_by_id = lambda x: MatchTournamentResponse.from_query_result(x, date, "time", None,
                                                                                             None, None)
        result = matches_router.get_match_by_id(1)
        expected = matches_router.MatchTournamentResponse(id=1, date=date, format='Time limited', score=[])
        self.assertEqual(result, expected)

    @patch("routers.matches_router.matches_service")
    def test_getMatches_return_PaginatedMatch(self, mock_matches_service):
        mock_matches_service.count.return_value = 20
        mock_pages.return_value = ((10,), (1, 2))
        match1 = MatchTournamentResponse(id=1, date=datetime.utcnow(), format='Time limited', score=[])
        match2 = MatchTournamentResponse(id=2, date=datetime.utcnow(), format='Time limited', score=[])
        mock_matches_service.all.return_value = (match1, match2)
        result = matches_router.get_matches(1)
        expected = matches_router.PaginatedMatch(matches=[match1, match2],
                                                 pagination=matches_router.Pagination(page=1, items_per_page=10,
                                                                                      total_pages=2))
        self.assertEqual(result, expected)

    @patch("routers.matches_router.matches_service")
    def test_getMatchesByTournamentId_return_PaginatedMatch(self, mock_matches_service):
        mock_matches_service.count_by_tournament.return_value = 20
        mock_pages.return_value = ((10,), (1, 2))
        match1 = MatchTournamentResponse(id=1, date=datetime.utcnow(), format='Time limited', score=[])
        match2 = MatchTournamentResponse(id=2, date=datetime.utcnow(), format='Time limited', score=[])
        mock_matches_service.get_by_tournament.return_value = (match1, match2)
        result = matches_router.get_matches_by_tournament_id(1, 1)
        expected = matches_router.PaginatedMatch(matches=[match1, match2],
                                                 pagination=matches_router.Pagination(page=1, items_per_page=10,
                                                                                      total_pages=2))
        self.assertEqual(result, expected)


class AsyncMatchesRouter_Should(aiounittest.AsyncTestCase):
    def setUp(self) -> None:
        mock_pages.reset_mock()
        mock_admin.reset_mock()
        mock_director.reset_mock()

    async def test_updateScore_raise_Unauthorized_when_notAdminsNotDirector(self):
        mock_admin.return_value = False
        mock_director.return_value = False
        with self.assertRaises(Unauthorized) as context:
            await matches_router.update_score(1, Mock(), Mock())
        self.assertEqual("User has insufficient privileges", context.exception.detail)
        self.assertEqual(401, context.exception.status_code)

    @patch("routers.matches_router.matches_service")
    async def test_updateScore_raise_NotFound_when_notMatch(self, mock_matches_service):
        mock_admin.return_value = True
        mock_director.return_value = False
        mock_matches_service.find = lambda x: None
        with self.assertRaises(NotFound) as context:
            await matches_router.update_score(1, Mock(), Mock())
        self.assertEqual("Match 1 does not exist", context.exception.detail)
        self.assertEqual(404, context.exception.status_code)

    @patch("routers.matches_router.matches_service")
    async def test_updateScore_raise_BadRequest_when_matchDateFuture(self, mock_matches_service):
        mock_admin.return_value = True
        mock_director.return_value = False
        mock_matches_service.find = lambda x: Mock(date=(datetime.utcnow() + timedelta(days=1)))
        with self.assertRaises(BadRequest) as context:
            await matches_router.update_score(1, Mock(), Mock())
        self.assertEqual("The match date is in the future!", context.exception.detail)
        self.assertEqual(400, context.exception.status_code)

    @patch("routers.matches_router.matches_service")
    async def test_updateScore_raise_NotFound_when_notParticipants(self, mock_matches_service):
        mock_admin.return_value = True
        mock_director.return_value = False
        mock_matches_service.find = lambda x: Mock(date=(datetime.utcnow() - timedelta(days=1)))
        mock_matches_service.find_participants = lambda x, y: None
        with self.assertRaises(NotFound) as context:
            await matches_router.update_score(1, Mock(), Mock())
        self.assertEqual("The participants provided do not play in this match", context.exception.detail)
        self.assertEqual(404, context.exception.status_code)

    @patch("routers.matches_router.matches_service")
    async def test_updateScore_raise_BadRequest_when_negativeScore(self, mock_matches_service):
        mock_admin.return_value = True
        mock_director.return_value = False
        mock_matches_service.find = lambda x: Mock(date=(datetime.utcnow() - timedelta(days=1)))
        mock_matches_service.find_participants = lambda x, y: Mock()
        with self.assertRaises(BadRequest) as context:
            await matches_router.update_score(1, [Mock(score=-1)], Mock())
        self.assertEqual("Match score cannot be negative!", context.exception.detail)
        self.assertEqual(400, context.exception.status_code)

    @patch("routers.matches_router.matches_service")
    async def test_updateScore_raise_BadRequest_when_notAllParticipants(self, mock_matches_service):
        mock_admin.return_value = True
        mock_director.return_value = False
        mock_matches_service.find = lambda x: Mock(date=(datetime.utcnow() - timedelta(days=1)))
        mock_matches_service.find_participants = lambda x, y: Mock()
        with self.assertRaises(BadRequest) as context:
            await matches_router.update_score(1, [Mock(score=1)], Mock())
        self.assertEqual("Please fill the score for all participants!", context.exception.detail)
        self.assertEqual(400, context.exception.status_code)

    @patch("routers.matches_router.tournaments_service")
    @patch("routers.matches_router.matches_service")
    async def test_updateScore_raise_BadRequest_when_knockoutDraw(self, mock_matches_service, mock_tournaments_service):
        mock_admin.return_value = False
        mock_director.return_value = True
        mock_matches_service.find = lambda x: Mock(date=(datetime.utcnow() - timedelta(days=1)), tournaments_id=1)
        mock_matches_service.find_participants = lambda x, y: Mock()
        mock_tournaments_service.find = lambda x: Mock(format="knockout")
        with self.assertRaises(BadRequest) as context:
            await matches_router.update_score(1, [Mock(score=1), Mock(score=1)], Mock())
        self.assertEqual("There are no draws in knockout tournaments!", context.exception.detail)
        self.assertEqual(400, context.exception.status_code)

    @patch("routers.matches_router.tournaments_service")
    @patch("routers.matches_router.matches_service")
    async def test_updateScore_returns_MatchResponse_when_matchScoreUpdatedAndTournament(self, mock_matches_service,
                                                                                         mock_tournaments_service):
        mock_admin.return_value = False
        mock_director.return_value = True
        date = datetime.utcnow() - timedelta(days=1)
        mock_matches_service.find = lambda x: Mock(id=x, date=date, tournaments_id=1, format='time')
        mock_matches_service.find_participants = lambda x, y: Mock()
        mock_tournaments_service.find = lambda x: Mock(format="knockout", id=x)
        async_mock = AsyncMock()
        async_mock.side_effect = lambda x, y, z: matches_router.MatchResponse.from_query_result(x.id, x.date, x.format)
        with patch("routers.matches_router.matches_service.update_score", async_mock):
            result = await matches_router.update_score(1, [Mock(score=1), Mock(score=2)], Mock())
        expected = matches_router.MatchResponse(id=1, date=date, format='Time limited', participants=[], score=[])
        self.assertEqual(result, expected)

    @patch("routers.matches_router.matches_service")
    async def test_updateScore_returns_MatchResponse_when_matchScoreUpdatedNoTournament(self, mock_matches_service):
        mock_admin.return_value = False
        mock_director.return_value = True
        date = datetime.utcnow() - timedelta(days=1)
        mock_matches_service.find = lambda x: Mock(id=x, date=date, tournaments_id=None, format='time')
        mock_matches_service.find_participants = lambda x, y: Mock()
        async_mock = AsyncMock()
        async_mock.side_effect = lambda x, y: matches_router.MatchResponse.from_query_result(x.id, x.date, x.format)
        with patch("routers.matches_router.matches_service.update_score", async_mock):
            result = await matches_router.update_score(1, [Mock(score=1), Mock(score=2)], Mock())
        expected = matches_router.MatchResponse(id=1, date=date, format='Time limited', participants=[], score=[])
        self.assertEqual(result, expected)
