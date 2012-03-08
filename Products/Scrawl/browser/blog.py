from Products.CMFCore.utils import getToolByName
from Products.Five import BrowserView
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
        self.portal_discussion = getToolByName(self.context, 'portal_discussion')
        
    def comment_count(self, obj):
        """
        Returns the number of comments for the given object or False if
        comments are disabled.
        """
        
        if HAS_PAD:
            if IDiscussionLayer.providedBy(self.request):
                conversation = IConversation(obj)
                if conversation.enabled():
                    workflow = getToolByName(self.context, 'portal_workflow')
                    return len([c for c in conversation.values() \
                        if workflow.getInfoFor(c, 'review_state') == 'published'])
        if self.portal_discussion.isDiscussionAllowedFor(obj):
            discussion = self.portal_discussion.getDiscussionFor(obj)
            return discussion.replyCount(obj)
        return False
        
    def content_filter(self):
        """
        Returns a dictionary of criteria to pass to the query method.
        """
        
        allowed_filters = ['Subject', 'Creator']
        return dict([(f, self.request.form.get(f)) \
            for f in allowed_filters if f in self.request.form])
