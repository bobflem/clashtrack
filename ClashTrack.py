import coc
import os

from datetime import datetime

from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS

token = os.environ['INFLUXDB_TOKEN']
org = os.environ['INFLUXDB_ORG']
bucket = os.environ['INFLUXDB_BUCKET']

client = coc.login(os.environ['COCAPI_EMAIL'], os.environ['COCAPI_PASSWORD'])

async def main():
    clan = await client.get_clan(os.environ['CLASH_CLANTAG'])

    with InfluxDBClient(url=os.environ['INFLUXDB_HOST'], token=token, org=org) as influxClient:
        write_api = influxClient.write_api(write_options=SYNCHRONOUS)

        point = Point("clan") \
            .tag("name", clan.name) \
            .field("clanLevel", clan.level) \
            .field("clanType", clan.type) \
            .field("clanDescription", clan.description) \
            .field("clanPoints", clan.points) \
            .field("clanVersusPoints", clan.versus_points) \
            .field("clanWarWinStreak", clan.war_win_streak) \
            .field("clanWarWins", clan.war_wins) \
            .field("clanWarTies", clan.war_ties) \
            .field("clanWarLosses", clan.war_losses) \
            .field("clanWarFrequency", clan.war_frequency) \
            .field("clanMemberCount", clan.member_count) \
            .field("clanRequiredTrophies", clan.required_trophies) \
            .time(datetime.utcnow(), WritePrecision.S)
        write_api.write(bucket, org, point)

        async for player in clan.get_detailed_members():
            point = Point("player") \
                .tag("name", player.name) \
                .field("playerTownHallLevel", player.town_hall) \
                .field("playerExpLevel", player.exp_level) \
                .field("playerTrophies", player.trophies) \
                .field("playerBestTrophies", player.best_trophies) \
                .field("playerWarStars", player.war_stars) \
                .field("playerAttackWins", player.attack_wins) \
                .field("playerDefenseWins", player.defense_wins) \
                .field("playerBuilderHallLevel", player.builder_hall) \
                .field("playerVersusTrophies", player.versus_trophies) \
                .field("playerBestVersusTrophies", player.best_versus_trophies) \
                .field("playerVersusBattleWins", player.versus_attack_wins) \
                .field("playerWarPreference", player.war_opted_in) \
                .field("playerDonations", player.donations) \
                .field("playerDonationsReceived", player.received) \
                .time(datetime.utcnow(), WritePrecision.S)
            write_api.write(bucket, org, point)
    influxClient.close()

client.loop.run_until_complete(main())
client.close()