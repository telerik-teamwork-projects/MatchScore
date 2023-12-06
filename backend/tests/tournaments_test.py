import unittest
from datetime import datetime, timedelta
from unittest.mock import Mock, patch, AsyncMock

import aiounittest

from common.exceptions import Unauthorized, BadRequest, NotFound, InternalServerError
from models.enums import TournamentFormat, MatchFormat, TournamentStatus
from models.matches import MatchScore
from models.players import PlayerProfileImg
from models.tournaments import Tournament, Owner, TournamentLeagueResponse, TournamentKnockoutResponse, \
    TournamentRoundResponse, TournamentRound, TournamentMatch, TournamentPointsResponse, TournamentPlayerPoints, \
    TournamentMatches, DbTournament
from routers import tournaments_router

mock_admin = Mock(spec='routers.tournaments_router.is_admin')
mock_director = Mock(spec='routers.tournaments_router.is_director')
mock_pages = Mock(spec='routers.tournaments_router.manage_pages')
mock_two = Mock(spec='routers.tournaments_router.is_power_of_two')
tournaments_router.is_admin = mock_admin
tournaments_router.is_director = mock_director
tournaments_router.manage_pages = mock_pages
tournaments_router.is_power_of_two = mock_two


def fake_tournament(id: int):
    mock_tournament = Mock(spec=Tournament)
    mock_tournament.id = id
    mock_tournament.format = TournamentFormat.KNOCKOUT.value
    mock_tournament.title = 'Test Title'
    mock_tournament.match_format = MatchFormat.TIME.value
    mock_tournament.rounds = 3
    mock_tournament.third_place = 0
    mock_tournament.status = TournamentStatus.CLOSED.value
    mock_tournament.owner = Mock(spec=Owner)
    return mock_tournament


class TournamentsRouter_Should(unittest.TestCase):
    def setUp(self) -> None:
        mock_pages.reset_mock()
        mock_admin.reset_mock()
        mock_director.reset_mock()
        mock_two.reset_mock()

    @patch("routers.tournaments_router.tournaments_service")
    def test_getTournaments_return_TournamentPagination_when_tournamentsFound(self, mock_tournaments_service):
        mock_tournaments_service.count.return_value = 20
        mock_pages.return_value = ((20,), (1, 1))
        tournament1 = fake_tournament(1)
        tournament2 = fake_tournament(2)
        mock_tournaments_service.get_all.return_value = (tournament1, tournament2)
        result = tournaments_router.get_tournaments(1)
        expected = tournaments_router.t.TournamentPagination(tournaments=[tournament1, tournament2],
                                                             pagination=tournaments_router.Pagination(page=1,
                                                                                                      items_per_page=20,
                                                                                                      total_pages=1))
        self.assertEqual(result, expected)

    @patch("routers.tournaments_router.tournaments_service")
    def test_getTournaments_raise_InternalServerError_when_dbError(self, mock_tournaments_service):
        mock_tournaments_service.count.return_value = 20
        mock_pages.return_value = ((20,), (1, 1))
        mock_tournaments_service.get_all.side_effect = Mock(side_effect=Exception('Test'))
        with self.assertRaises(InternalServerError) as context:
            tournaments_router.get_tournaments(1)
        self.assertEqual("Retrieving tournaments failed", context.exception.detail)
        self.assertEqual(500, context.exception.status_code)

    @patch("routers.tournaments_router.tournaments_service")
    def test_getTournament_return_Tournament_when_tournamentFound(self, mock_tournaments_service):
        mock_owner = Mock(spec=Owner)
        mock_tournaments_service.get_one = lambda x: Tournament(id=x, format=TournamentFormat.KNOCKOUT.value,
                                                                title='Test Title', match_format=MatchFormat.TIME.value,
                                                                rounds=3, third_place=0,
                                                                status=TournamentStatus.CLOSED.value, owner=mock_owner)
        result = tournaments_router.get_tournament(5)
        expected = tournaments_router.t.Tournament(id=5, format=TournamentFormat.KNOCKOUT.value,
                                                   title='Test Title', match_format=MatchFormat.TIME.value,
                                                   rounds=3, third_place=0,
                                                   status=TournamentStatus.CLOSED.value, owner=mock_owner)
        self.assertEqual(result, expected)

    @patch("routers.tournaments_router.tournaments_service")
    def test_getTournament_raise_InternalServerError_when_dbError(self, mock_tournaments_service):
        mock_tournaments_service.get_one.side_effect = Mock(side_effect=Exception('Test'))
        with self.assertRaises(InternalServerError) as context:
            tournaments_router.get_tournament(1)
        self.assertEqual("Retrieving tournament details failed", context.exception.detail)
        self.assertEqual(500, context.exception.status_code)

    @patch("routers.tournaments_router.tournaments_service")
    def test_viewRounds_raise_NotFound_when_noTournament(self, mock_tournaments_service):
        mock_tournaments_service.find = lambda x: None
        with self.assertRaises(NotFound) as context:
            tournaments_router.view_rounds(2)
        self.assertEqual("Tournament 2 does not exist!", context.exception.detail)
        self.assertEqual(404, context.exception.status_code)

    @patch("routers.tournaments_router.tournaments_service")
    def test_viewRounds_return_TournamentRoundResponse_when_tournamentFound(self, mock_tournaments_service):
        mock_tournaments_service.find = lambda x: Mock(id=x)
        matches = [(1, 3, [(2, 'Name1'), (3, 'Name2')]), (2, 3, [(1, 'Name3'), (4, 'Name4')])]
        rounds = [('Round 1', matches)]
        mock_tournaments_service.view_tournament = lambda x: TournamentRoundResponse.from_query_result(x.id, rounds)
        result = tournaments_router.view_rounds(2)
        expected = TournamentRoundResponse(id=2, rounds=[
            TournamentRound(round='Round 1',
                            matches=[TournamentMatch(match_id=1, next_match=3,
                                                     participants=[MatchScore.from_query_result(2, 'Name1'),
                                                                   MatchScore.from_query_result(3, 'Name2')]),
                                     TournamentMatch(match_id=2, next_match=3,
                                                     participants=[MatchScore.from_query_result(1, 'Name3'),
                                                                   MatchScore.from_query_result(4, 'Name4')])])])
        self.assertEqual(result, expected)

    @patch("routers.tournaments_router.tournaments_service")
    def test_viewPoints_raise_NotFound_when_noTournament(self, mock_tournaments_service):
        mock_tournaments_service.find = lambda x: None
        with self.assertRaises(NotFound) as context:
            tournaments_router.view_points(2)
        self.assertEqual("Tournament 2 does not exist!", context.exception.detail)
        self.assertEqual(404, context.exception.status_code)

    @patch("routers.tournaments_router.tournaments_service")
    def test_viewPoints_raise_BadRequest_when_tournamentKnockout(self, mock_tournaments_service):
        mock_tournaments_service.find = lambda x: Mock(id=x, format=TournamentFormat.KNOCKOUT.value)
        with self.assertRaises(BadRequest) as context:
            tournaments_router.view_points(2)
        self.assertEqual("Tournament 2 is not league!", context.exception.detail)
        self.assertEqual(400, context.exception.status_code)

    @patch("routers.tournaments_router.tournaments_service")
    def test_viewPoints_return_TournamentPointsResponse_when_tournamentFound(self, mock_tournaments_service):
        mock_tournaments_service.find = lambda x: Mock(id=x, format=TournamentFormat.LEAGUE.value)
        players = [(1, "Name1", 4, 2, 1, 1, 2, 5), (2, "Name2", 4, 1, 1, 2, -2, 3)]
        mock_tournaments_service.view_points = lambda x: TournamentPointsResponse.from_query_result(x.id, players)
        result = tournaments_router.view_points(2)
        expected = TournamentPointsResponse(id=2, players=[
            TournamentPlayerPoints(player_id=1, full_name='Name1', matches_played=4, wins=2, draws=1, losses=1,
                                   score_diff=2, points=5),
            TournamentPlayerPoints(player_id=2, full_name='Name2', matches_played=4, wins=1, draws=1, losses=2,
                                   score_diff=-2, points=3)])
        self.assertEqual(result, expected)

    @patch("routers.tournaments_router.tournaments_service")
    def test_viewMatches_raise_NotFound_when_noTournament(self, mock_tournaments_service):
        mock_tournaments_service.find = lambda x: None
        with self.assertRaises(NotFound) as context:
            tournaments_router.view_matches(2)
        self.assertEqual("Tournament 2 does not exist!", context.exception.detail)
        self.assertEqual(404, context.exception.status_code)

    @patch("routers.tournaments_router.tournaments_service")
    def test_viewMatches_return_TournamentMatches_when_tournamentFound(self, mock_tournaments_service):
        mock_tournaments_service.find = lambda x: Mock(id=x)
        matches = [(1, 3, [(2, 'Name1'), (3, 'Name2')]), (2, 3, [(1, 'Name3'), (4, 'Name4')])]
        mock_tournaments_service.view_matches = lambda x: TournamentMatches.from_query_result(x, matches)
        result = tournaments_router.view_matches(2)
        expected = TournamentMatches(id=2, matches=[TournamentMatch(match_id=1, next_match=3,
                                                                    participants=[
                                                                        MatchScore.from_query_result(2, 'Name1'),
                                                                        MatchScore.from_query_result(3, 'Name2')]),
                                                    TournamentMatch(match_id=2, next_match=3,
                                                                    participants=[
                                                                        MatchScore.from_query_result(1, 'Name3'),
                                                                        MatchScore.from_query_result(4, 'Name4')])])
        self.assertEqual(result, expected)

    def test_updateDate_raise_Unauthorized_when_notAdminsNotDirector(self):
        mock_admin.return_value = False
        mock_director.return_value = False
        with self.assertRaises(Unauthorized) as context:
            tournaments_router.update_date(1, Mock(), Mock())
        self.assertEqual("User has insufficient privileges", context.exception.detail)
        self.assertEqual(401, context.exception.status_code)

    @patch("routers.tournaments_router.tournaments_service")
    def test_updateDate_raise_NotFound_when_noTournament(self, mock_tournaments_service):
        mock_admin.return_value = True
        mock_director.return_value = False
        mock_tournaments_service.find = lambda x: None
        with self.assertRaises(NotFound) as context:
            tournaments_router.update_date(2, Mock(), Mock())
        self.assertEqual("Tournament 2 does not exist!", context.exception.detail)
        self.assertEqual(404, context.exception.status_code)

    @patch("routers.tournaments_router.tournaments_service")
    def test_updateDate_raise_BadRequest_when_tournamentStarted(self, mock_tournaments_service):
        mock_admin.return_value = False
        mock_director.return_value = True
        mock_tournaments_service.find = lambda x: Mock(start_date=(datetime.utcnow() - timedelta(days=1)))
        with self.assertRaises(BadRequest) as context:
            tournaments_router.update_date(1, Mock(), Mock())
        self.assertEqual("The tournament has already started!", context.exception.detail)
        self.assertEqual(400, context.exception.status_code)

    @patch("routers.tournaments_router.tournaments_service")
    def test_updateDate_raise_BadRequest_when_dateIsNotFuture(self, mock_tournaments_service):
        mock_admin.return_value = True
        mock_director.return_value = False
        mock_tournaments_service.find = lambda x: Mock(start_date=(datetime.utcnow() + timedelta(days=1)))
        with self.assertRaises(BadRequest) as context:
            tournaments_router.update_date(1, Mock(date=(datetime.utcnow() - timedelta(days=1))), Mock())
        self.assertEqual("The new tournament start date should be in the future!", context.exception.detail)
        self.assertEqual(400, context.exception.status_code)

    @patch("routers.tournaments_router.tournaments_service")
    def test_updateDate_raise_BadRequest_when_tournamentStatusOpen(self, mock_tournaments_service):
        mock_admin.return_value = True
        mock_director.return_value = False
        mock_tournaments_service.find = lambda x: Mock(start_date=(datetime.utcnow() + timedelta(days=1)),
                                                       status=TournamentStatus.OPEN.value)
        with self.assertRaises(BadRequest) as context:
            tournaments_router.update_date(1, Mock(date=(datetime.utcnow() + timedelta(days=1))), Mock())
        self.assertEqual("Tournament status should be Closed", context.exception.detail)
        self.assertEqual(400, context.exception.status_code)

    @patch("routers.tournaments_router.tournaments_service")
    def test_updateDate_return_DbTournament_when_newDateIsOldDate(self, mock_tournaments_service):
        mock_admin.return_value = True
        mock_director.return_value = False
        date = (datetime.utcnow() + timedelta(days=1))
        mock_tournaments_service.find = lambda x: DbTournament(id=x, format='test', title='test', match_format='test',
                                                               rounds=3, third_place=0, owner_id=2,
                                                               status=TournamentStatus.CLOSED.value, start_date=date)
        result = tournaments_router.update_date(2, Mock(date=date), Mock())
        expected = DbTournament(id=2, format='test', title='test', match_format='test', rounds=3, third_place=0,
                                owner_id=2, status=TournamentStatus.CLOSED.value, start_date=date)
        self.assertEqual(result, expected)

    @patch("routers.tournaments_router.tournaments_service")
    def test_updateDate_return_DbTournament_when_newDate(self, mock_tournaments_service):
        mock_admin.return_value = False
        mock_director.return_value = True
        date = datetime.utcnow() + timedelta(days=1)
        new_date = datetime.utcnow() + timedelta(days=2)
        mock_tournaments_service.find = lambda x: DbTournament(id=x, format='test', title='test', match_format='test',
                                                               rounds=3, third_place=0, owner_id=2,
                                                               status=TournamentStatus.CLOSED.value, start_date=date)
        mock_tournaments_service.update_date = lambda x, y: DbTournament(id=x.id, format=x.format, title=x.title,
                                                                         match_format=x.match_format, rounds=x.rounds,
                                                                         third_place=x.third_place, owner_id=x.owner_id,
                                                                         status=x.status, start_date=y.date)
        result = tournaments_router.update_date(2, Mock(date=new_date), Mock())
        expected = DbTournament(id=2, format='test', title='test', match_format='test', rounds=3, third_place=0,
                                owner_id=2, status=TournamentStatus.CLOSED.value, start_date=new_date)
        self.assertEqual(result, expected)

    def test_getPlayersByTournamentId_raise_Unauthorized_when_notAdminsNotDirector(self):
        mock_admin.return_value = False
        mock_director.return_value = False
        with self.assertRaises(Unauthorized) as context:
            tournaments_router.get_players_by_tournament_id(1, Mock())
        self.assertEqual("User has insufficient privileges", context.exception.detail)
        self.assertEqual(401, context.exception.status_code)

    @patch("routers.tournaments_router.tournaments_service")
    def test_getPlayersByTournamentId_raise_InternalServerError_when_dbError(self, mock_tournaments_service):
        mock_admin.return_value = False
        mock_director.return_value = True
        mock_tournaments_service.get_players_by_tournament_id.side_effect = Mock(side_effect=Exception('Test'))
        with self.assertRaises(InternalServerError) as context:
            tournaments_router.get_players_by_tournament_id(1, Mock())
        self.assertEqual("Retrieving players failed", context.exception.detail)
        self.assertEqual(500, context.exception.status_code)

    @patch("routers.tournaments_router.tournaments_service")
    def test_getPlayersByTournamentId_return_ListPlayerProfileImg_when_playersFound(self, mock_tournaments_service):
        mock_admin.return_value = False
        mock_director.return_value = True
        mock_tournaments_service.get_players_by_tournament_id = lambda x: [PlayerProfileImg(id=1, full_name='Test')]
        result = tournaments_router.get_players_by_tournament_id(1, Mock())
        expected = [PlayerProfileImg(id=1, full_name='Test')]
        self.assertEqual(result, expected)


class AsyncTournamentRouter_Should(aiounittest.AsyncTestCase):
    def setUp(self) -> None:
        mock_pages.reset_mock()
        mock_admin.reset_mock()
        mock_director.reset_mock()
        mock_two.reset_mock()

    async def test_createLeagueTournament_raise_Unauthorized_when_notAdminsNotDirector(self):
        mock_admin.return_value = False
        mock_director.return_value = False
        with self.assertRaises(Unauthorized) as context:
            await tournaments_router.create_league_tournament(Mock(), Mock())
        self.assertEqual("User has insufficient privileges", context.exception.detail)
        self.assertEqual(401, context.exception.status_code)

    async def test_createLeagueTournament_raise_BadRequest_when_notUniqueParticipants(self):
        mock_admin.return_value = False
        mock_director.return_value = True
        mock_tournament = Mock(participants=[Mock(full_name='Test'), Mock(full_name='Test')])
        with self.assertRaises(BadRequest) as context:
            await tournaments_router.create_league_tournament(mock_tournament, Mock())
        self.assertEqual("Participants should be unique!", context.exception.detail)
        self.assertEqual(400, context.exception.status_code)

    async def test_createLeagueTournament_raise_BadRequest_when_participantsLessThanMin(self):
        mock_admin.return_value = False
        mock_director.return_value = True
        mock_tournament = Mock(participants=[Mock(full_name='Test 1'), Mock(full_name='Test 2')])
        with self.assertRaises(BadRequest) as context:
            await tournaments_router.create_league_tournament(mock_tournament, Mock())
        self.assertEqual(
            f'Participants must be between {tournaments_router.MIN_PARTICIPANTS} and {tournaments_router.MAX_PARTICIPANTS}!',
            context.exception.detail)
        self.assertEqual(400, context.exception.status_code)

    async def test_createLeagueTournament_raise_BadRequest_when_participantsMoreThanMax(self):
        mock_admin.return_value = False
        mock_director.return_value = True
        mock_participants = [Mock(full_name=f'Test {i}') for i in range(1, 18)]
        mock_tournament = Mock(participants=mock_participants)
        with self.assertRaises(BadRequest) as context:
            await tournaments_router.create_league_tournament(mock_tournament, Mock())
        self.assertEqual(
            f'Participants must be between {tournaments_router.MIN_PARTICIPANTS} and {tournaments_router.MAX_PARTICIPANTS}!',
            context.exception.detail)
        self.assertEqual(400, context.exception.status_code)

    async def test_createLeagueTournament_raise_BadRequest_when_participantsNotEven(self):
        mock_admin.return_value = False
        mock_director.return_value = True
        mock_participants = [Mock(full_name=f'Test {i}') for i in range(1, 6)]
        mock_tournament = Mock(participants=mock_participants)
        with self.assertRaises(BadRequest) as context:
            await tournaments_router.create_league_tournament(mock_tournament, Mock())
        self.assertEqual('Participants should be even number!', context.exception.detail)
        self.assertEqual(400, context.exception.status_code)

    async def test_createLeagueTournament_raise_BadRequest_when_startDateNotInFuture(self):
        mock_admin.return_value = True
        mock_director.return_value = False
        mock_participants = [Mock(full_name=f'Test {i}') for i in range(1, 5)]
        mock_tournament = Mock(participants=mock_participants, start_date=(datetime.utcnow() - timedelta(days=1)))
        with self.assertRaises(BadRequest) as context:
            await tournaments_router.create_league_tournament(mock_tournament, Mock())
        self.assertEqual('Tournament start date should be in the future!', context.exception.detail)
        self.assertEqual(400, context.exception.status_code)

    async def test_createLeagueTournament_returns_TournamentLeagueResponse_when_leagueCreated(self):
        mock_admin.return_value = True
        mock_director.return_value = False
        start_date = datetime.utcnow() + timedelta(days=1)
        end_date = datetime.utcnow() + timedelta(days=3)
        mock_participants = [Mock(full_name=f'Test {i}') for i in range(1, 5)]
        mock_tournament = Mock(participants=mock_participants, start_date=start_date, title='Title',
                               match_format=MatchFormat.TIME.value)
        async_mock = AsyncMock()
        async_mock.side_effect = lambda x, y: TournamentLeagueResponse.from_query_result(1,
                                                                                         TournamentFormat.LEAGUE.value,
                                                                                         x.title, None, x.match_format,
                                                                                         3, None, x.start_date,
                                                                                         end_date, (2, "admin", None))
        with patch("routers.tournaments_router.tournaments_service.create_league", async_mock):
            result = await tournaments_router.create_league_tournament(mock_tournament, Mock())
        expected = TournamentLeagueResponse.from_query_result(1,
                                                              TournamentFormat.LEAGUE.value,
                                                              'Title', None, MatchFormat.TIME.value,
                                                              3, None, start_date,
                                                              end_date, (2, "admin", None))
        self.assertEqual(result, expected)

    async def test_createKnockoutTournament_raise_Unauthorized_when_notAdminsNotDirector(self):
        mock_admin.return_value = False
        mock_director.return_value = False
        with self.assertRaises(Unauthorized) as context:
            await tournaments_router.create_knockout_tournament(Mock(), Mock())
        self.assertEqual("User has insufficient privileges", context.exception.detail)
        self.assertEqual(401, context.exception.status_code)

    async def test_createKnockoutTournament_raise_BadRequest_when_notUniqueParticipants(self):
        mock_admin.return_value = False
        mock_director.return_value = True
        mock_tournament = Mock(participants=[Mock(full_name='Test'), Mock(full_name='Test')])
        with self.assertRaises(BadRequest) as context:
            await tournaments_router.create_knockout_tournament(mock_tournament, Mock())
        self.assertEqual("Participants should be unique!", context.exception.detail)
        self.assertEqual(400, context.exception.status_code)

    async def test_createKnockoutTournament_raise_BadRequest_when_startDateNotInFuture(self):
        mock_admin.return_value = True
        mock_director.return_value = False
        mock_participants = [Mock(full_name=f'Test {i}') for i in range(1, 5)]
        mock_tournament = Mock(participants=mock_participants, start_date=(datetime.utcnow() - timedelta(days=1)))
        with self.assertRaises(BadRequest) as context:
            await tournaments_router.create_knockout_tournament(mock_tournament, Mock())
        self.assertEqual('Tournament start date should be in the future!', context.exception.detail)
        self.assertEqual(400, context.exception.status_code)

    async def test_createKnockoutTournament_returns_TournamentKnockoutResponse_when_knockoutOpenCreated(self):
        mock_admin.return_value = True
        mock_director.return_value = False
        start_date = datetime.utcnow() + timedelta(days=1)
        end_date = datetime.utcnow() + timedelta(days=3)
        mock_participants = [Mock(full_name=f'Test {i}') for i in range(1, 5)]
        mock_tournament = Mock(participants=mock_participants, start_date=start_date, title='Title',
                               match_format=MatchFormat.TIME.value, status=TournamentStatus.OPEN)
        async_mock = AsyncMock()
        async_mock.side_effect = lambda x, y: TournamentKnockoutResponse.from_query_result(1,
                                                                                           TournamentFormat.KNOCKOUT.value,
                                                                                           x.title, None,
                                                                                           x.match_format,
                                                                                           3, 0, None, x.start_date,
                                                                                           end_date, (2, "admin", None))
        with patch("routers.tournaments_router.tournaments_service.create_knockout", async_mock):
            result = await tournaments_router.create_knockout_tournament(mock_tournament, Mock())
        expected = TournamentKnockoutResponse.from_query_result(1,
                                                                TournamentFormat.KNOCKOUT.value,
                                                                'Title', None, MatchFormat.TIME.value,
                                                                3, 0, None, start_date,
                                                                end_date, (2, "admin", None))
        self.assertEqual(result, expected)

    async def test_createKnockoutTournament_raise_BadRequest_when_participantsLessThanMin_statusClosed(self):
        mock_admin.return_value = False
        mock_director.return_value = True
        mock_participants = [Mock(full_name=f'Test {i}') for i in range(1, 3)]
        start_date = datetime.utcnow() + timedelta(days=1)
        mock_tournament = Mock(participants=mock_participants, start_date=start_date, title='Title',
                               match_format=MatchFormat.TIME.value, status=TournamentStatus.CLOSED)
        with self.assertRaises(BadRequest) as context:
            await tournaments_router.create_knockout_tournament(mock_tournament, Mock())
        self.assertEqual(
            f'Participants must be between {tournaments_router.MIN_PARTICIPANTS} and {tournaments_router.MAX_PARTICIPANTS}!',
            context.exception.detail)
        self.assertEqual(400, context.exception.status_code)

    async def test_createKnockoutTournament_raise_BadRequest_when_participantsMoreThanMax_statusClosed(self):
        mock_admin.return_value = True
        mock_director.return_value = False
        mock_participants = [Mock(full_name=f'Test {i}') for i in range(1, 18)]
        start_date = datetime.utcnow() + timedelta(days=1)
        mock_tournament = Mock(participants=mock_participants, start_date=start_date, title='Title',
                               match_format=MatchFormat.TIME.value, status=TournamentStatus.CLOSED)
        with self.assertRaises(BadRequest) as context:
            await tournaments_router.create_knockout_tournament(mock_tournament, Mock())
        self.assertEqual(
            f'Participants must be between {tournaments_router.MIN_PARTICIPANTS} and {tournaments_router.MAX_PARTICIPANTS}!',
            context.exception.detail)
        self.assertEqual(400, context.exception.status_code)

    async def test_createKnockoutTournament_raise_BadRequest_when_participantsNotPowerOfTwo_statusClosed(self):
        mock_admin.return_value = False
        mock_director.return_value = True
        mock_two.return_value = False
        mock_participants = [Mock(full_name=f'Test {i}') for i in range(1, 6)]
        start_date = datetime.utcnow() + timedelta(days=1)
        mock_tournament = Mock(participants=mock_participants, start_date=start_date, title='Title',
                               match_format=MatchFormat.TIME.value, status=TournamentStatus.CLOSED)
        with self.assertRaises(BadRequest) as context:
            await tournaments_router.create_knockout_tournament(mock_tournament, Mock())
        self.assertEqual('Number of participants for knockout tournament is not correct!', context.exception.detail)
        self.assertEqual(400, context.exception.status_code)

    async def test_createKnockoutTournament_returns_TournamentKnockoutResponse_when_knockoutClosedCreated(self):
        mock_admin.return_value = True
        mock_director.return_value = False
        mock_two.return_value = True
        start_date = datetime.utcnow() + timedelta(days=1)
        end_date = datetime.utcnow() + timedelta(days=3)
        mock_participants = [Mock(full_name=f'Test {i}') for i in range(1, 5)]
        mock_tournament = Mock(participants=mock_participants, start_date=start_date, title='Title',
                               match_format=MatchFormat.TIME.value, status=TournamentStatus.CLOSED)
        async_mock = AsyncMock()
        async_mock.side_effect = lambda x, y: TournamentKnockoutResponse.from_query_result(1,
                                                                                           TournamentFormat.KNOCKOUT.value,
                                                                                           x.title, None,
                                                                                           x.match_format,
                                                                                           3, 0, None, x.start_date,
                                                                                           end_date, (2, "admin", None))
        with patch("routers.tournaments_router.tournaments_service.create_knockout", async_mock):
            result = await tournaments_router.create_knockout_tournament(mock_tournament, Mock())
        expected = TournamentKnockoutResponse.from_query_result(1,
                                                                TournamentFormat.KNOCKOUT.value,
                                                                'Title', None, MatchFormat.TIME.value,
                                                                3, 0, None, start_date,
                                                                end_date, (2, "admin", None))
        self.assertEqual(result, expected)

    async def test_updatePlayers_raise_Unauthorized_when_notAdminsNotDirector(self):
        mock_admin.return_value = False
        mock_director.return_value = False
        with self.assertRaises(Unauthorized) as context:
            await tournaments_router.update_players(1, Mock(), Mock())
        self.assertEqual("User has insufficient privileges", context.exception.detail)
        self.assertEqual(401, context.exception.status_code)

    @patch("routers.tournaments_router.tournaments_service")
    async def test_updatePlayers_raise_NotFound_when_noTournament(self, mock_tournaments_service):
        mock_admin.return_value = True
        mock_director.return_value = False
        mock_tournaments_service.find = lambda x: None
        with self.assertRaises(NotFound) as context:
            await tournaments_router.update_players(2, Mock(), Mock())
        self.assertEqual("Tournament 2 does not exist!", context.exception.detail)
        self.assertEqual(404, context.exception.status_code)

    @patch("routers.tournaments_router.tournaments_service")
    async def test_updatePlayers_raise_BadRequest_when_tournamentStarted(self, mock_tournaments_service):
        mock_admin.return_value = False
        mock_director.return_value = True
        mock_tournaments_service.find = lambda x: Mock(start_date=(datetime.utcnow() - timedelta(days=1)))
        with self.assertRaises(BadRequest) as context:
            await tournaments_router.update_players(1, Mock(), Mock())
        self.assertEqual("The tournament has already started!", context.exception.detail)
        self.assertEqual(400, context.exception.status_code)

    @patch("routers.tournaments_router.tournaments_service")
    async def test_updatePlayers_raise_BadRequest_when_notUniqueOldPlayers(self, mock_tournaments_service):
        mock_admin.return_value = True
        mock_director.return_value = False
        mock_tournaments_service.find = lambda x: Mock(start_date=(datetime.utcnow() + timedelta(days=1)))
        players = [Mock(player='Test1', player_prev='Test'), Mock(player='Test2', player_prev='Test')]
        with self.assertRaises(BadRequest) as context:
            await tournaments_router.update_players(1, players, Mock())
        self.assertEqual("Participants should be unique!", context.exception.detail)
        self.assertEqual(400, context.exception.status_code)

    @patch("routers.tournaments_router.tournaments_service")
    async def test_updatePlayers_raise_BadRequest_when_notUniqueNewPlayers(self, mock_tournaments_service):
        mock_admin.return_value = True
        mock_director.return_value = False
        mock_tournaments_service.find = lambda x: Mock(start_date=(datetime.utcnow() + timedelta(days=1)))
        players = [Mock(player='Test', player_prev='Test1'), Mock(player='Test', player_prev='Test2')]
        with self.assertRaises(BadRequest) as context:
            await tournaments_router.update_players(1, players, Mock())
        self.assertEqual("Participants should be unique!", context.exception.detail)
        self.assertEqual(400, context.exception.status_code)

    @patch("routers.tournaments_router.tournaments_service")
    async def test_updatePlayers_raise_BadRequest_when_newPlayersAlreadyInTournament(self, mock_tournaments_service):
        mock_admin.return_value = True
        mock_director.return_value = False
        mock_tournaments_service.find = lambda x: Mock(start_date=(datetime.utcnow() + timedelta(days=1)))
        players = [Mock(player='Test3', player_prev='Test1'), Mock(player='Test4', player_prev='Test2')]
        mock_tournaments_service.check_participants = lambda x, y: Mock()
        with self.assertRaises(BadRequest) as context:
            await tournaments_router.update_players(1, players, Mock())
        self.assertEqual("The participants provided already play in this tournament!", context.exception.detail)
        self.assertEqual(400, context.exception.status_code)

    @patch("routers.tournaments_router.tournaments_service")
    async def test_updatePlayers_raise_BadRequest_when_oldPlayersNotInTournament(self, mock_tournaments_service):
        mock_admin.return_value = True
        mock_director.return_value = False
        mock_tournaments_service.find = lambda x: Mock(start_date=(datetime.utcnow() + timedelta(days=1)))
        players = [Mock(player='Test3', player_prev='Test1'), Mock(player='Test4', player_prev='Test2')]
        mock_tournaments_service.check_participants.side_effect = [None, None]
        with self.assertRaises(BadRequest) as context:
            await tournaments_router.update_players(1, players, Mock())
        self.assertEqual("The participants to be updated do not play in this tournament!", context.exception.detail)
        self.assertEqual(400, context.exception.status_code)

    @patch("routers.tournaments_router.tournaments_service")
    async def test_updatePlayers_raise_BadRequest_when_tournamentStatusOpen(self, mock_tournaments_service):
        mock_admin.return_value = True
        mock_director.return_value = False
        mock_tournaments_service.find = lambda x: Mock(start_date=(datetime.utcnow() + timedelta(days=1)),
                                                       status=TournamentStatus.OPEN.value)
        players = [Mock(player='Test3', player_prev='Test1'), Mock(player='Test4', player_prev='Test2')]
        mock_tournaments_service.check_participants.side_effect = [None, Mock()]
        with self.assertRaises(BadRequest) as context:
            await tournaments_router.update_players(1, players, Mock())
        self.assertEqual("Tournament status should be Closed", context.exception.detail)
        self.assertEqual(400, context.exception.status_code)

    @patch("routers.tournaments_router.tournaments_service")
    async def test_updatePlayers_return_TournamentRoundResponse_when_updatePlayers(self, mock_tournaments_service):
        mock_admin.return_value = True
        mock_director.return_value = False
        mock_tournaments_service.find = lambda x: Mock(id=x, start_date=(datetime.utcnow() + timedelta(days=1)),
                                                       status=TournamentStatus.CLOSED.value)
        players = [Mock(player='Test3', player_prev='Test1'), Mock(player='Test4', player_prev='Test2')]
        mock_tournaments_service.check_participants.side_effect = [None, Mock()]
        matches = [(1, 3, [(2, 'Name1'), (3, 'Name2')]), (2, 3, [(1, 'Name3'), (4, 'Name4')])]
        rounds = [('Round 1', matches)]
        async_mock = AsyncMock()
        async_mock.side_effect = lambda x, y: TournamentRoundResponse.from_query_result(x.id, rounds)
        with patch("routers.tournaments_router.tournaments_service.update_players", async_mock):
            result = await tournaments_router.update_players(2, players, Mock())
        expected = TournamentRoundResponse(id=2, rounds=[
            TournamentRound(round='Round 1',
                            matches=[TournamentMatch(match_id=1, next_match=3,
                                                     participants=[MatchScore.from_query_result(2, 'Name1'),
                                                                   MatchScore.from_query_result(3, 'Name2')]),
                                     TournamentMatch(match_id=2, next_match=3,
                                                     participants=[MatchScore.from_query_result(1, 'Name3'),
                                                                   MatchScore.from_query_result(4, 'Name4')])])])
        self.assertEqual(result, expected)

    async def test_startKnockoutTournament_raise_Unauthorized_when_notAdminsNotDirector(self):
        mock_admin.return_value = False
        mock_director.return_value = False
        with self.assertRaises(Unauthorized) as context:
            await tournaments_router.start_knockout_tournament(2, Mock(), Mock())
        self.assertEqual("User has insufficient privileges", context.exception.detail)
        self.assertEqual(401, context.exception.status_code)

    @patch("routers.tournaments_router.tournaments_service")
    async def test_startKnockoutTournament_raise_NotFound_when_noTournament(self, mock_tournaments_service):
        mock_admin.return_value = True
        mock_director.return_value = False
        mock_tournaments_service.find = lambda x: None
        with self.assertRaises(NotFound) as context:
            await tournaments_router.start_knockout_tournament(2, Mock(), Mock())
        self.assertEqual("Tournament 2 does not exist!", context.exception.detail)
        self.assertEqual(404, context.exception.status_code)

    @patch("routers.tournaments_router.tournaments_service")
    async def test_startKnockoutTournament_raise_BadRequest_when_tournamentClosed(self, mock_tournaments_service):
        mock_admin.return_value = True
        mock_director.return_value = False
        mock_tournaments_service.find = lambda x: Mock(status=TournamentStatus.CLOSED.value)
        with self.assertRaises(BadRequest) as context:
            await tournaments_router.start_knockout_tournament(2, Mock(), Mock())
        self.assertEqual("The tournament has already started!", context.exception.detail)
        self.assertEqual(400, context.exception.status_code)

    @patch("routers.tournaments_router.tournaments_service")
    async def test_startKnockoutTournament_raise_BadRequest_when_participantsLessThanMin(self,
                                                                                         mock_tournaments_service):
        mock_admin.return_value = True
        mock_director.return_value = False
        mock_tournaments_service.find = lambda x: Mock(status=TournamentStatus.OPEN.value)
        mock_tournaments_service.find_participants = lambda x: [1, 2]
        with self.assertRaises(BadRequest) as context:
            await tournaments_router.start_knockout_tournament(2, Mock(), Mock())
        self.assertEqual(
            f'Participants must be between {tournaments_router.MIN_PARTICIPANTS} and {tournaments_router.MAX_PARTICIPANTS}!',
            context.exception.detail)
        self.assertEqual(400, context.exception.status_code)

    @patch("routers.tournaments_router.tournaments_service")
    async def test_startKnockoutTournament_raise_BadRequest_when_participantsMoreThanMax(self,
                                                                                         mock_tournaments_service):
        mock_admin.return_value = True
        mock_director.return_value = False
        mock_tournaments_service.find = lambda x: Mock(status=TournamentStatus.OPEN.value)
        mock_tournaments_service.find_participants = lambda x: [i for i in range(1, 20)]
        with self.assertRaises(BadRequest) as context:
            await tournaments_router.start_knockout_tournament(2, Mock(), Mock())
        self.assertEqual(
            f'Participants must be between {tournaments_router.MIN_PARTICIPANTS} and {tournaments_router.MAX_PARTICIPANTS}!',
            context.exception.detail)
        self.assertEqual(400, context.exception.status_code)

    @patch("routers.tournaments_router.tournaments_service")
    async def test_startKnockoutTournament_raise_BadRequest_when_participantsNotPowerOfTwo(self,
                                                                                           mock_tournaments_service):
        mock_admin.return_value = True
        mock_director.return_value = False
        mock_two.return_value = False
        mock_tournaments_service.find = lambda x: Mock(status=TournamentStatus.OPEN.value)
        mock_tournaments_service.find_participants = lambda x: [i for i in range(1, 6)]
        with self.assertRaises(BadRequest) as context:
            await tournaments_router.start_knockout_tournament(2, Mock(), Mock())
        self.assertEqual("Number of participants for knockout tournament is not correct!", context.exception.detail)
        self.assertEqual(400, context.exception.status_code)

    @patch("routers.tournaments_router.tournaments_service")
    async def test_startKnockoutTournament_raise_BadRequest_when_startDateNotInFuture(self, mock_tournaments_service):
        mock_admin.return_value = True
        mock_director.return_value = False
        mock_two.return_value = True
        mock_tournaments_service.find = lambda x: Mock(status=TournamentStatus.OPEN.value)
        mock_tournaments_service.find_participants = lambda x: [i for i in range(1, 6)]
        with self.assertRaises(BadRequest) as context:
            await tournaments_router.start_knockout_tournament(2, Mock(date=(datetime.utcnow() - timedelta(days=1))),
                                                               Mock())
        self.assertEqual("Tournament start date should be in the future!", context.exception.detail)
        self.assertEqual(400, context.exception.status_code)

    @patch("routers.tournaments_router.tournaments_service")
    async def test_startKnockoutTournament_returns_TournamentKnockoutResponse_when_knockoutStarted(self,
                                                                                                   mock_tournaments_service):
        mock_admin.return_value = False
        mock_director.return_value = True
        mock_two.return_value = True
        start_date = datetime.utcnow() + timedelta(days=1)
        end_date = datetime.utcnow() + timedelta(days=3)
        mock_tournaments_service.find = lambda x: Mock(id=x, start_date=start_date, title='Title',
                                                       match_format=MatchFormat.TIME.value,
                                                       status=TournamentStatus.OPEN.value)
        mock_tournaments_service.find_participants = lambda x: [i for i in range(1, 6)]
        async_mock = AsyncMock()
        async_mock.side_effect = lambda x, y, z: TournamentKnockoutResponse.from_query_result(x.id,
                                                                                              TournamentFormat.KNOCKOUT.value,
                                                                                              x.title, None,
                                                                                              x.match_format,
                                                                                              3, 0, None, x.start_date,
                                                                                              end_date,
                                                                                              (2, "admin", None))
        with patch("routers.tournaments_router.tournaments_service.start_knockout", async_mock):
            result = await tournaments_router.start_knockout_tournament(2, Mock(date=start_date), Mock())
        expected = TournamentKnockoutResponse.from_query_result(2,
                                                                TournamentFormat.KNOCKOUT.value,
                                                                'Title', None, MatchFormat.TIME.value,
                                                                3, 0, None, start_date,
                                                                end_date, (2, "admin", None))
        self.assertEqual(result, expected)
