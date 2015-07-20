"""py.test configuration file."""
import os

import pytest
import xal


@pytest.fixture(scope='session', params=['local', 'fabric'])
def session(request):
    # Absolute path to current working directory. This is useful to setup
    # working directory in tests in order to use fixtures.
    here = os.path.abspath(os.getcwd())

    xal_session = None
    if request.param == 'local':
        xal_session = xal.LocalSession()
    elif request.param == 'fabric':
        xal_session = xal.FabricSession()
        xal_session.client.connect('localhost')
    context = xal_session.path.cd(here)
    context.__enter__()
    return xal_session
