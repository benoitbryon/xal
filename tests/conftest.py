"""py.test configuration file."""
import pytest
import xal


@pytest.fixture(scope='session', params=['local', 'fabric'])
def session(request):
    xal_session = None
    if request.param == 'local':
        xal_session = xal.LocalSession()
    elif request.param == 'fabric':
        xal_session = xal.FabricSession()
        xal_session.client.connect('localhost')
    return xal_session
