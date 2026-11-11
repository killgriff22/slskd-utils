"""Main slskd-utils CLI entrypoint"""

from time import sleep
from os import getenv
import slskd_api
from slskd_utils.logo import LOGO
import click
host = "http://192.168.1.191:5030"
api_key = getenv('SLSKD_KEY') or ""
slskd = slskd_api.SlskdClient(host, api_key)


@click.group()
def cli():
    """Soulseek daemon utilities"""
    click.echo(LOGO)


@cli.group()
def rooms():
    """Room operations"""


@rooms.group("list")
def list_rooms():
    """Gets lists of rooms"""

@rooms.group("join", invoke_without_command=False)
@click.option('-n', '--name')
def join_rooms(name):
    """Joins rooms"""
    # room = slskd.rooms.join(name)
    # click.echo(f"Joined room {room['name']}")


@list_rooms.command("joined")
def joined_rooms():
    """Show currently joined rooms"""
    click.echo("Currently joined rooms:\n")
    for room_name in slskd.rooms.get_all_joined():
        click.echo(click.style(f"• {room_name}", bold=True, fg="cyan"))


@list_rooms.command("all")
def list_all_rooms():
    """Show all rooms"""
    click.echo("All rooms:\n")
    for room in slskd.rooms.get_all():
        room_users = room['userCount']
        room_name = room['name']
        click.echo(
            click.style(
                f"• {room_name}, {room_users} user{'s' if room_users != 1 else ''}",
                bold=True,
                fg="green",
            )
        )

@join_rooms.command("busy")
@click.option("-c", "--count", default=10, help="Number of busiest rooms to join")
def join_busiest(count: int):
    """Joins the busiest rooms"""
    all_rooms = slskd.rooms.get_all()
    top_rooms = sorted(all_rooms, key=lambda d: d['userCount'], reverse=True)
    click.echo(f"Joining top {count} busiest room{"s" if count != 1 else ""}...")
    for i in range(min(count, len(all_rooms))):
        room = top_rooms[i]
        click.echo(f"Joining room {room['name']} with {room['userCount']} users")
        _ = slskd.rooms.join(room["name"])




@cli.group()
def search():
    """Search operations"""

@search.command()
def list_searches():
    """List all known searches"""
    click.echo("Past searches:")


@search.command()
@click.option("-t", "--terms", default="", help="The terms of your search")
def query(terms:str):
    """Search for songs, albums, or artists. The first result of """
    click.echo(f"Searching for: {terms}")
    promise = slskd.searches.search_text(terms)
    promise_id = promise['id']
    #print(promise_id)
    sleep(5)
    results = slskd.searches.search_responses(promise_id)
    files_to_dl = []
    for result in results:
        for f in result['files']:
            if f['extension'] not in ['flac', 'lrc']:
                continue
            files_to_dl.append(f)
        if len(files_to_dl) > 0:
            slskd.transfers.enqueue(result['username'], files_to_dl)
            #print(files_to_dl)
            files_to_dl = []
            break
#search list
#search query str

    
