"""
"""

from pyramid.view import view_config
import pyramid.httpexceptions as exc

from detectoid.twitch import Twitch
from detectoid.utils import group_by_date


@view_config(route_name='stream', renderer='json')
def stream(request):
    """
    /{stream}

    - stream: stream name

    Returns basic stream info (viewers, chatters, followers, etc)
    """
    name = request.matchdict["stream"].lower()
    info = Twitch().stream(name)

    if info is None:
        raise exc.HTTPInternalServerError("Error while loading stream details {}".format(name))

    if info is False:
        raise exc.HTTPNotFound("Offline stream".format(name))

    return {
        'stream': info,
    }

@view_config(route_name='distribution', renderer='json')
def distribution(request):
    """
    /{stream}

    - stream: stream name

    Returns a list of chatters with their registration date and a daily
    count of users registrations
    """
    channel = request.matchdict["stream"].lower()
    users = Twitch().chatters(channel)

    if users is None:
        raise exc.HTTPInternalServerError("Error while loading channel details {}".format(channel))

    groups = group_by_date(users)

    return {
        'chatters': users,
        'distribution': [{
                'date': date,
                'count': count,
            }
            for date, count in groups.items()
        ],
    }