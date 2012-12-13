from Products.Five.browser import BrowserView
from Products.CMFCore.utils import getToolByName

try:
    from plone.app.discussion.interfaces import IConversation, IDiscussionLayer
    HAS_PAD = True
except ImportError:
    HAS_PAD = False


class BlogView(BrowserView):
    """
    Listing of blog items. Based on BlogView from collective.blog.view.
    """

    def __init__(self, context, request):
        self.context = context
        self.request = request
        self.portal_discussion = getToolByName(self.context,
                                               'portal_discussion')

    def comment_count(self, obj):
        """
        Returns the number of comments for the given object or False if
        comments are disabled.
        """

        discussion_allowed = self.portal_discussion.isDiscussionAllowedFor(obj)
        if not HAS_PAD and not discussion_allowed:
            return False

        if not HAS_PAD and self.portal_discussion.isDiscussionAllowedFor(obj):
            discussion = self.portal_discussion.getDiscussionFor(obj)
            return discussion.replyCount(obj)

        #HAS_PAD == True
        if IDiscussionLayer.providedBy(self.request):
            conversation = IConversation(obj)
            if conversation.enabled():
                workflow = getToolByName(self.context, 'portal_workflow')
                cvalues = conversation.values()
                return len([c for c in  cvalues \
                    if workflow.getInfoFor(c, 'review_state') == 'published'])

    def content_filter(self):
        """
        Returns a dictionary of criteria to pass to the query method.
        """

        allowed_filters = ['Subject', 'Creator']
        return dict([(f, self.request.form.get(f)) \
            for f in allowed_filters if f in self.request.form])
