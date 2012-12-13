from Products.CMFCore.utils import getToolByName
from plone.browserlayer.utils import registered_layers, unregister_layer
from Products.Scrawl.browser.interfaces import IScrawlLayer


def install(portal, reinstall=False):
    setup_tool = getToolByName(portal, 'portal_setup')
    setup_tool.runAllImportStepsFromProfile('profile-Products.Scrawl:default')


def uninstall(portal, reinstall=False):
    # Run the uninstall profile.
    setup_tool = getToolByName(portal, 'portal_setup')
    profile = 'profile-Products.Scrawl:uninstall'
    setup_tool.runAllImportStepsFromProfile(profile)

    # Remove the browser layer.
    if IScrawlLayer in registered_layers():
        unregister_layer('Products.Scrawl')
