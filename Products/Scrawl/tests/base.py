from Testing import ZopeTestCase as ztc
from Products.PloneTestCase import PloneTestCase

ztc.installProduct('Scrawl')
PloneTestCase.setupPloneSite(products=['Scrawl'])


class ScrawlTestCase(PloneTestCase.PloneTestCase):
    """Base class for integration tests.
    """


class ScrawlFunctionalTestCase(PloneTestCase.FunctionalTestCase):
    """Base class for functional tests.
    """
